"""Local RVM matting using ONNX Runtime. Original footage is opened read-only."""
from pathlib import Path
import argparse,collections,hashlib,json,shutil,subprocess,time
import cv2
import numpy as np
import onnxruntime as ort

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',required=True,type=Path)
    parser.add_argument('--output',required=True,type=Path,help='New directory; existing directories are not overwritten.')
    parser.add_argument('--model',type=Path,default=Path('models/rvm_mobilenetv3_fp32.onnx'))
    parser.add_argument('--ffmpeg',default='ffmpeg')
    parser.add_argument('--provider',choices=['auto','dml','cpu'],default='auto')
    parser.add_argument('--layout',choices=['camera','obs-side-by-side'],default='camera')
    parser.add_argument('--seconds',type=float,default=12)
    parser.add_argument('--width',type=int,help='Optional output width; aspect ratio is preserved.')
    parser.add_argument('--ratio',type=float,default=0.25)
    args=parser.parse_args()
    if not args.input.is_file() or not args.model.is_file():parser.error('Input video and model must exist.')
    if args.output.exists():parser.error('Output directory already exists. Choose a new one.')
    if args.seconds<0 or not 0<args.ratio<=1:parser.error('Seconds must be nonnegative and ratio must be in (0, 1].')
    if args.width is not None and args.width<256:parser.error('Width must be at least 256.')
    ffmpeg=shutil.which(args.ffmpeg)
    if not ffmpeg:parser.error('FFmpeg not found. Install it or pass --ffmpeg with its executable path.')
    available=ort.get_available_providers()
    gpu=args.provider=='dml' or (args.provider=='auto' and 'DmlExecutionProvider' in available)
    if gpu and 'DmlExecutionProvider' not in available:parser.error('DirectML is unavailable; no GPU execution was performed.')
    provider='DmlExecutionProvider' if gpu else 'CPUExecutionProvider'
    video=cv2.VideoCapture(str(args.input))
    if not video.isOpened():parser.error('Unable to open input video.')
    sw=int(video.get(cv2.CAP_PROP_FRAME_WIDTH));sh=int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps=float(video.get(cv2.CAP_PROP_FPS))
    if fps<=0 or sw<=0 or sh<=0:parser.error('Invalid video geometry or frame rate.')
    if args.layout=='obs-side-by-side' and (sw,sh)!=(3840,1080):parser.error('OBS side-by-side expects exactly 3840x1080.')
    source_width=sw//2 if args.layout=='obs-side-by-side' else sw
    width=(args.width or source_width)//2*2
    height=round(sh*width/source_width/2)*2
    options=ort.SessionOptions();options.enable_mem_pattern=False
    options.execution_mode=ort.ExecutionMode.ORT_SEQUENTIAL
    options.intra_op_num_threads=2;options.inter_op_num_threads=1
    options.log_severity_level=3;options.enable_profiling=True
    args.output.mkdir(parents=True,exist_ok=False)
    options.profile_file_prefix=str(args.output/'runtime-profile')
    providers=[('DmlExecutionProvider',{'device_id':'0'}),'CPUExecutionProvider'] if gpu else ['CPUExecutionProvider']
    session=ort.InferenceSession(str(args.model),sess_options=options,providers=providers)
    print('Runtime backend: '+provider,flush=True)
    def writer(name,pixels,lossless=False):
        log=(args.output/(name+'.log')).open('w',encoding='utf-8')
        command=[ffmpeg,'-hide_banner','-v','warning','-f','rawvideo','-pix_fmt',pixels,'-s',f'{width}x{height}','-r',str(fps),'-i','pipe:0','-an']
        command+=['-c:v','ffv1','-level','3','-threads','2'] if lossless else ['-c:v','libx264','-preset','veryfast','-crf','18','-threads','2','-pix_fmt','yuv420p','-movflags','+faststart']
        command.append(str(args.output/name))
        return subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,stderr=log),log
    writers=[]
    states=[np.zeros((1,1,1,1),np.float32) for _ in range(4)]
    ratio=np.array([args.ratio],np.float32)
    limit=max(1,round(args.seconds*fps)) if args.seconds else None
    count=0;timings=[];profile=None;started=time.perf_counter()
    try:
        writers=[writer('foreground.mp4','rgb24'),writer('alpha.mkv','gray',True),writer('preview-white.mp4','rgb24')]
        while limit is None or count<limit:
            ok,frame=video.read()
            if not ok:break
            if args.layout=='obs-side-by-side':frame=frame[:,sw//2:]
            if (frame.shape[1],frame.shape[0])!=(width,height):frame=cv2.resize(frame,(width,height),interpolation=cv2.INTER_AREA)
            rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            source=np.ascontiguousarray(rgb.transpose(2,0,1)[None],dtype=np.float32)/255.
            feed={'src':source,'downsample_ratio':ratio,**{f'r{i+1}i':state for i,state in enumerate(states)}}
            tick=time.perf_counter();foreground,alpha,*states=session.run(None,feed);timings.append(time.perf_counter()-tick)
            foreground=np.clip(foreground[0].transpose(1,2,0),0,1)
            alpha=np.clip(alpha[0,0],0,1)
            preview=foreground*alpha[...,None]+1-alpha[...,None]
            for (process,_),array in zip(writers,[foreground,alpha,preview]):
                process.stdin.write(np.rint(array*255).astype(np.uint8).tobytes())
            count+=1
            if count==3:profile=Path(session.end_profiling())
            if count==1 or count%30==0:print(f'Frames processed: {count}',flush=True)
    finally:
        video.release()
        failures=[]
        for process,log in writers:
            if process.stdin:process.stdin.close()
            process.wait(timeout=60);log.close()
            if process.returncode:failures.append(process.returncode)
        if failures:raise RuntimeError('An encoder failed; inspect output logs.')
    elapsed=time.perf_counter()-started
    if not count:raise RuntimeError('No video frames were decoded.')
    if profile is None:profile=Path(session.end_profiling())
    events=json.loads(profile.read_text(encoding='utf-8'))
    backends=collections.Counter(event.get('args',{}).get('provider') for event in events if event.get('args',{}).get('provider'))
    proven=backends.get('DmlExecutionProvider',0)>0
    if gpu and not proven:raise RuntimeError('GPU execution was requested but not confirmed in the runtime profile.')
    result={'model_sha256':hashlib.sha256(args.model.read_bytes()).hexdigest(),'source_size':[sw,sh],'layout':args.layout,'output_size':[width,height],'fps':fps,'frames':count,'video_seconds':count/fps,'processing_seconds':elapsed,'processing_fps':count/elapsed,'median_inference_ms_excluding_first':float(np.median(timings[1:] or timings)*1000),'requested_backend':provider,'observed_backend_events':dict(backends),'profile_sample_frames':min(count,3),'gpu_execution_confirmed':proven,'runtime_version':ort.__version__,'downsample_ratio':args.ratio,'recurrent_states_preserved':True,'audio_included':False}
    # Portable result metadata deliberately omits source names and absolute paths.
    (args.output/'result.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2),flush=True)

if __name__=='__main__':main()

"""Download the official RVM MobileNetV3 FP32 model; do not bundle weights in Git."""
from pathlib import Path
import argparse, hashlib, json, urllib.request

MODEL_URL='https://github.com/PeterL1n/RobustVideoMatting/releases/download/v1.0.0/rvm_mobilenetv3_fp32.onnx'
MODEL_SHA256='88d4531297118f595bf2fd60f6f566aec2e559393802d1f436c380f0cbbd2828'
LICENSE_URL='https://raw.githubusercontent.com/PeterL1n/RobustVideoMatting/master/LICENSE'

def download(url):
    request=urllib.request.Request(url,headers={'User-Agent':'Botelho-Video-Editor'})
    with urllib.request.urlopen(request,timeout=120) as response:return response.read()

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory',type=Path,default=Path('models'))
    args=parser.parse_args()
    args.directory.mkdir(parents=True,exist_ok=True)
    destination=args.directory/'rvm_mobilenetv3_fp32.onnx'
    content=destination.read_bytes() if destination.is_file() else download(MODEL_URL)
    digest=hashlib.sha256(content).hexdigest()
    if digest!=MODEL_SHA256:raise SystemExit('Model SHA-256 mismatch; the file was not installed.')
    if not destination.exists():destination.write_bytes(content)
    license_file=args.directory/'RVM-LICENSE.txt'
    if not license_file.exists():license_file.write_bytes(download(LICENSE_URL))
    manifest={'model':destination.name,'release':'v1.0.0','sha256':digest,'source':MODEL_URL,'license':'GPL-3.0','license_file':license_file.name}
    (args.directory/'model-source.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print('Official model verified and available in '+str(args.directory))

if __name__=='__main__':main()

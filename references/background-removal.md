# Robust Video Matting e cenários personalizados

Use o [Robust Video Matting](https://github.com/PeterL1n/RobustVideoMatting) como etapa de pós-processamento. Ele estima primeiro plano e máscara ao longo do vídeo, com estados recorrentes entre frames. Aceleração por GPU não garante uma máscara perfeita; confira os resultados no take real.

## Instalação opcional

Requer Python 3.10+, FFmpeg e um ambiente virtual. No Windows, o arquivo de dependências instala ONNX Runtime DirectML. Em outras plataformas, instala o runtime CPU; o script também aceita o provider CPU explicitamente. Não instala plugins do OBS nem modifica drivers.

```bash
python -m venv .venv
# Ative o ambiente virtual conforme seu sistema.
python -m pip install -r requirements-rvm.txt
python scripts/download_rvm.py
```

O download usa o modelo oficial MobileNetV3 FP32 da release `v1.0.0`, verifica SHA-256 e guarda a licença original junto do modelo. Os pesos não fazem parte do repositório. Leia os termos do RVM antes de redistribuir os modelos.

## Primeiro teste

```bash
python scripts/rvm_matte.py --input camera.mp4 --output output/teste --seconds 12
```

Se FFmpeg não estiver no PATH, passe `--ffmpeg /caminho/ffmpeg`. Para um bruto OBS que realmente use tela esquerda e câmera direita em 3840×1080, acrescente `--layout obs-side-by-side`.

O padrão é processar até 12 segundos. Use `--seconds 0` para o take completo depois de avaliar a amostra. A entrada deve ser vídeo CFR; normalize fontes de frame rate variável antes de usar esse fluxo. O script preserva o FPS nominal e o original e não altera a velocidade da fala.

O provider `--provider auto` usa DirectML quando disponível; o console e `result.json` informam a escolha e se a execução GPU foi comprovada pelo perfil. `--provider dml` falha se esse backend não estiver disponível, em vez de apresentar CPU como teste GPU. DirectML requer Windows e dispositivo DirectX 12 compatível; consulte a [documentação atual](https://onnxruntime.ai/docs/execution-providers/DirectML-ExecutionProvider.html).

## Arquivos de saída

| Arquivo | Conteúdo |
| --- | --- |
| `foreground.mp4` | Cores estimadas do primeiro plano |
| `alpha.mkv` | Máscara de cinza com FFV1 sem perdas |
| `preview-white.mp4` | Prévia composta sobre branco |
| `result.json` | Parâmetros, contagem de frames, tempo e backend observado |

Esses vídeos não incluem áudio. Mantenha a faixa original sincronizada na montagem. Os MP4s não contêm alfa; para trocar o fundo use foreground + máscara ou produza um derivado com transparência real, como WebM com alfa, validando o decoder do projeto.

## Composição e conferência

Componha `foreground × alpha + fundo × (1 − alpha)`. Use o cenário fornecido pelo criador, respeitando proporção e área segura. Ajuste enquadramento, escala e cor da pessoa conforme a cena, preservando cabeça e rosto.

Observe cabelo, orelhas, mãos, cadeira e bordas do corpo no início, meio e fim e em movimentos maiores. Confira vazamentos, halos e pulsação da máscara em reprodução. Reinicie os estados recorrentes em uma nova tomada; não trate frames isolados como uma sequência temporal válida.

Execute o matting uma vez por fonte/trecho com os parâmetros escolhidos e reutilize os derivados na prévia e no render. Refaça se a fonte, o crop, o modelo ou os parâmetros mudarem. Evite executar o modelo a cada seek do HyperFrames.

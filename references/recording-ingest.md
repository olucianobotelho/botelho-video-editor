# Entrada de gravação e separação das fontes

Prefira receber tela, câmera e microfone independentes. Assim a câmera não cobre um controle importante da demonstração e pode ser reenquadrada sem recuperar um PiP pequeno já gravado na tela.

## Layout opcional em um único arquivo

Um layout possível de OBS é **3840×1080, 30 fps**: tela na metade esquerda e câmera inteira na direita. O vídeo final pode continuar 1920×1080. As duas fontes compartilham o mesmo relógio.

| Fonte | Área | Filtro FFmpeg |
| --- | --- | --- |
| Tela | x0, y0, 1920×1080 | `crop=1920:1080:0:0` |
| Câmera | x1920, y0, 1920×1080 | `crop=1920:1080:1920:0` |

Esse mapa só vale quando o arquivo realmente usa esse arranjo. Verifique frames e dimensões antes de separar. Ampliação de monitor não cria detalhes que não existiam na captura nativa.

Guarde a câmera com cabeça inteira, sem máscara ou removedor de fundo gravado. O tratamento e o cenário entram na pós. Os scripts desta skill não configuram nem controlam o OBS.

## Áudio

Um arranjo útil tem três faixas: referência (voz + computador), microfone isolado e computador isolado. Confirme a ordem com ffprobe. Não some a referência com as isoladas, pois duplicaria o áudio.

Preserve a taxa original, preferencialmente 48 kHz quando suportada pelo equipamento. Use proteção de pico conservadora e evite empilhar filtros de limpeza na captura sem testar a fala. Compare uma amostra antes do take longo; o tratamento da edição não recupera informação já removida por um filtro agressivo.

## Durante o take

Fale frases completas e deixe pequenos respiros. Se errar, pause e repita a frase inteira. Mostre o botão e o clique citados e espere a interface responder. Marcas de capítulo podem ajudar a localizar retomadas e demonstrações.

Grave em velocidade normal e deixe música, CTA e explicações gráficas para a edição. Use fones para evitar que o som do computador retorne pelo microfone.

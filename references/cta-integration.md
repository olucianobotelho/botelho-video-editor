# CTA pixelado configurável

Modelo: [../assets/pixel-engagement.template.html](../assets/pixel-engagement.template.html). Transparent canvas 1920 × 1080, duração 8,3 s, área útil x90–1240 / y833–994, preservando a coluna de câmera à direita. Tem entrada, curtir em 1,70 s, inscrição em 3,25 s, sino em 4,80 s, estados confirmados, brilho discreto até a saída 7,82–8,30 s.

## Integração em um projeto Hyperframes

1. Copie `assets/sfx/cta-soft-click.wav` e `assets/sfx/cta-soft-bell.wav` desta skill para a mesma pasta relativa do projeto.
2. O template usa `assets/fonts/DepartureMono.woff2`. A fonte não está embutida nesta skill. Obtenha-a da [origem oficial](https://departuremono.com/) e preserve a licença correspondente. O [repositório oficial](https://github.com/rektdeckard/departure-mono) identifica a fonte sob SIL OFL; não confundir com a licença MIT do código do site. Se alterar a fonte, revalide o texto dentro dos botões.
3. Substitua **todas** as ocorrências de `__CTA_ID__` por um ID único e grave em `compositions/frames/engagement-1.html`. Os caminhos `../../assets/...` são relativos a essa localização.
4. O pai precisa carregar `assets/gsap.min.js`. Monte a instância como subcomposição, por exemplo:

```html
<div id="engagement-1"
     data-composition-id="engagement-1"
     data-composition-src="compositions/frames/engagement-1.html"
     data-start="120" data-duration="8.3"
     data-width="1920" data-height="1080"
     data-track-index="20"
     style="position:absolute;inset:0;z-index:30"></div>
```

5. Mantenha o host com o canvas completo e sobre os gráficos. O ID do host, o ID da composição interna e a chave em `window.__timelines` devem ser idênticos. O template registra uma timeline pausada; não a aninhe manualmente na principal.
6. Substitua `__CHANNEL_NAME__` pelo nome do canal, escapando caracteres especiais de HTML. Remova as instâncias antigas de CTA/chromakey e seus sons. Os três `<audio>` internos já possuem tempos locais, IDs únicos e `data-volume="0.4"`; não os duplique no pai.
7. Se mudar o tamanho ou a posição, transforme a área `.engagement-content` e confira a distância da câmera, textos e safe area. Se mudar a duração, retime explicitamente saída, ciclos e tempos de áudio; não basta ampliar `data-duration`.

## Som e checagem

SFX originais sintetizados localmente, sem ruído ou áudio de terceiros, PCM mono 48 kHz / 16 bit. Clique de 0,12 s com pico de arquivo próximo de −18 dBFS; sino de 0,65 s com pico próximo de −21 dBFS. Após o ganho 0,4, os picos efetivos ficam em −25,96 e −28,95 dBFS. O som deve ser discreto e perceptível na mixagem; não normalizar para pico cheio. Os três sons usam pistas internas separadas e tempos explicitamente locais.

Confira parser JS, estados inicial/parcial/confirmado, geometria e retorno no tempo. Execute as checagens da versão instalada do HyperFrames e a inspeção visual/sonora no novo projeto. Apresente apenas a prévia até o usuário aprovar explicitamente a exportação da revisão.

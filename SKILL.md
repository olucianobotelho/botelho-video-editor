---
name: botelho-video-editor
description: "Edite tutoriais e vídeos com apresentador usando HyperFrames, explicações brancas e azuis, detalhes pixelados, câmera lateral, Robust Video Matting e fundos personalizados. Use para roteiro de edição, montagem, revisão, CTA e tela final com som discreto."
---

# Botelho Video Editor

Direção de edição para vídeos com apresentador e demonstração de software: fala clara, explicações visuais construídas ao vivo, câmera bem enquadrada e som discreto. Adapte ao briefing de cada criador.

## Ferramentas e início do trabalho

Use HyperFrames para composição, animação e prévia. Se a skill `hyperframes` estiver instalada, leia-a como entrada técnica; caso contrário, consulte a [documentação oficial](https://hyperframes.heygen.com/introduction) e os exemplos da versão instalada. Esta skill complementa o framework, sem substituir o contrato técnico dele.

Antes de editar, localize o bruto, a transcrição, as referências, o projeto existente e os assets licenciados. Preserve o original. Transcreva e revise nomes e números; apresente um plano com trechos, cortes, imagens, explicações, câmera e climas musicais antes da implementação quando houver um ciclo de aprovação de roteiro.

Continue a implementação já autorizada. Quando o criador estiver validando a prévia, exporte o vídeo final após a aprovação dessa revisão. Um pedido explícito de exportação da versão atual já autoriza essa etapa; não peça a mesma confirmação novamente. Derivados locais de mídia e checagens da prévia fazem parte da preparação da edição.

## Roteiro e ritmo

- Nos primeiros três segundos, apresente uma fala compreensível, promessa ou prova real. Avalie os primeiros 30 segundos como uma sequência; evite começar com branco vazio ou um título desconectado do assunto.
- Preserve frases completas, contexto, preparação das piadas e pequenas pausas de reação. Microcortes não devem remover a conclusão ou tornar a fala confusa.
- Quando acelerar a fala, use uma mudança moderada, como 1,1–1,2×, se isso couber no briefing. Preserve o tom e retime vídeo, áudio, legendas e deixas juntos. Não acelere música ou SFX automaticamente nem aplique a velocidade duas vezes.
- Use números e períodos confirmados. Se a tela mostrar relatórios antigos, alinhe os destaques à informação atual fornecida pelo criador e contextualize o material visual.
- Transforme perguntas relevantes em uma batida visual antes da resposta: pergunta grande, câmera lateral e construção progressiva do raciocínio. Mostre o clique real quando a fala aponta um botão; não invente uma ação que o bruto não registra.

## Direção visual e movimento

Nas explicações, use branco, azul vivo e texto escuro. Uma base possível é `#ffffff`, `#2455f5` e `#13223b`. Use tipografia pixelada em detalhes e uma fonte de leitura no texto principal. A identidade do criador e o briefing têm prioridade sobre esse preset.

- Uma ideia visual por vez, hierarquia clara e espaço generoso. Evite uma sequência de cartões grandes arredondados com aparência de dashboard genérico.
- Construa linhas, fluxos e texto progressivamente, sincronizados à fala. A digitação e os traços precisam parecer uma explicação acontecendo, com tempo de leitura.
- Mantenha movimento sutil até o fim da cena: onda de áudio, cursor ou indicador ativo. Não repita a animação de entrada para sustentar uma explicação contínua.
- Use uma timeline pausada, determinística e buscável. Limite ciclos à duração da cena; evite relógios independentes, timers e efeitos aleatórios não controlados.
- Um brilho pequeno pode percorrer a moldura da câmera sem iluminar o rosto ou cobrir o conteúdo.
- Use setas legíveis e separadas de texto, ícones e coluna da câmera. Prefira logotipos oficiais a imitações pixeladas de marcas.
- Se houver barra decorativa de progresso, mantenha-a contínua e monótona e termine apenas no último quadro. Ela não altera duração, timestamps ou controles do player.

## Câmera, recorte e fundo

Posicione a câmera ao lado das explicações, geralmente à direita, preservando o espaço de leitura. Centralize o rosto dentro do quadro, mantenha a cabeça inteira e algum respiro. Acompanhe deslocamentos suavemente ou reenquadre por trecho.

Para substituir o cenário, use Robust Video Matting na pós e componha a pessoa sobre o fundo personalizado fornecido pelo criador. Enquanto esse arquivo não estiver disponível, use uma base neutra na prévia. Preserve câmera original, primeiro plano e máscara separados.

Leia [references/background-removal.md](references/background-removal.md) para o fluxo portátil de RVM e a composição com alfa. Leia [references/recording-ingest.md](references/recording-ingest.md) quando receber captura de tela e câmera separadas. Confira o layout real antes de aplicar qualquer crop; coordenadas de um projeto não são regra para todos os vídeos.

Evite câmera duplicada, cabeça cortada, rosto colado à borda, vazamento do cenário original e uma moldura mostrando apenas o fundo. Confira cabelo, orelhas, mãos e resíduos de objetos durante o movimento, inclusive nas trocas de modo e nos minutos finais.

## Voz, música e sonoplastia

Use o microfone original em sua taxa de amostragem, preservando um proxy separado para transcrição. Limpe com moderação: rumble, excesso de médios graves, presença e compressão suave conforme a amostra. Não aplique denoise ou gate agressivos sem evidência de ruído.

A voz conduz. Cubra o vídeo com música de fundo coerente com os blocos, mudanças de clima e crossfades. Verifique início, meio e fim; uma trilha mais densa na segunda metade também precisa ficar abaixo da fala. Defina ganho ouvindo a mixagem, sem normalizar todos os arquivos ao mesmo pico.

Use digitação macia, pequenos ticks, cliques curtos e um sino discreto, sincronizados às ações. Prefira timbres satisfatórios e pouco invasivos a chiado, glitch, graves de impacto ou whooshes agressivos. Áudio pixelado não precisa soar estridente.

O CTA inclui dois SFX sintetizados sem gravação de voz: clique e sino. Os ganhos do modelo são pontos de partida, não metas universais. Não duplique os eventos de áudio no pai da composição.

## Componentes reutilizáveis

- [CTA pixelado](references/cta-integration.md): curtir, inscrição e sino, com confirmações, cursor e som. Troque `__CHANNEL_NAME__` pela marca do projeto.
- [Tela final](references/end-screen-integration.md): base branca, marca configurável e dois espaços fixos 16:9 para vídeos sugeridos; duração padrão de dez segundos.

Mantenha os espaços da tela final vazios para posicionar os elementos reais no YouTube. O template não cria links clicáveis. Revalide texto, geometria, fontes, duração e som em cada integração.

## Conferência da revisão

Assista ao gancho como sequência, confira frases completas e mostre as ações explicadas. Inspecione início, meio e fim das cenas longas, mudanças de câmera e movimentos maiores. Busque a timeline para frente e para trás e confirme resultado consistente.

Verifique texto dentro dos limites, setas espaçadas, rosto centralizado, recorte estável e câmera única. Escute voz, música e SFX juntos em volume normal. Rode as checagens nativas da versão instalada do HyperFrames e apresente a prévia com as mudanças e limitações observadas.

# Botelho Video Editor

Skill de edição para agentes de IA: vídeos com apresentador, tutoriais de software, explicações animadas com HyperFrames, identidade branca/azul/pixelada, recorte com Robust Video Matting e fundos personalizados.

## O que ela orienta

- Transcrição revisada e plano de edição antes da montagem, quando houver aprovação de roteiro.
- Ganchos claros, frases completas e ritmo dinâmico sem microcortes confusos.
- Textos, linhas e diagramas construídos em sincronia com a fala.
- Câmera lateral, rosto centralizado e cabeça inteira.
- Recorte do cenário na pós, mantendo o original e uma máscara reutilizável.
- Música abaixo da voz, mudanças de clima e sonoplastia suave.
- CTA pixelado de curtir, inscrever e ativar o sino, com dois SFX sintetizados incluídos.
- Tela final de dez segundos com dois espaços fixos 16:9.
- Prévia, conferência visual/sonora e exportação conforme a autorização do projeto.

## Instalação da skill

Com uma ferramenta compatível com o formato Agent Skills, instale este repositório como `botelho-video-editor`. Uma opção é o instalador `skills`:

```bash
npx skills add https://github.com/OWNER/botelho-video-editor
```

Substitua `OWNER` pelo proprietário mostrado na URL deste repositório. Também é possível clonar o repositório na pasta de skills do seu agente. No Codex, essa pasta é `$CODEX_HOME/skills` ou `~/.codex/skills` quando não houver configuração personalizada. Evite sobrescrever outra skill pessoal com o mesmo nome.

Instale HyperFrames separadamente, seguindo as [instruções oficiais](https://github.com/heygen-com/hyperframes). Esta skill fornece direção editorial e componentes, não inclui o runtime de renderização.

## Como pedir uma edição

> Use $botelho-video-editor para transcrever este tutorial e preparar um plano por trecho. Quero explicações brancas e azuis, câmera lateral com meu fundo personalizado, animações construídas durante a fala e música discreta. Apresente a prévia antes da exportação final.

Forneça ao agente os arquivos locais, o objetivo, o público, as referências e o cenário personalizado quando houver. O briefing pode mudar paleta, idioma, ritmo e composição.

## Arquivos incluídos

```text
SKILL.md
agents/openai.yaml
assets/
  pixel-engagement.template.html
  pixel-end-screen.template.html
  sfx/cta-soft-click.wav
  sfx/cta-soft-bell.wav
references/
  cta-integration.md
  end-screen-integration.md
  recording-ingest.md
  background-removal.md
scripts/
  download_rvm.py
  rvm_matte.py
requirements-rvm.txt
```

Os HTMLs são templates para integrar em um projeto HyperFrames; não são vídeos prontos nem composições autossuficientes. Substitua os IDs e `__CHANNEL_NAME__`, configure as fontes e revalide o layout. Não há fontes, biblioteca GSAP, músicas ou runtime do HyperFrames embutidos.

- [Integrar CTA](references/cta-integration.md)
- [Integrar tela final](references/end-screen-integration.md)
- [Preparar tela, câmera e áudio](references/recording-ingest.md)
- [Instalar e usar o RVM opcional](references/background-removal.md)

## Recorte opcional de fundo

O script RVM roda localmente e preserva o bruto. Ele grava primeiro plano, máscara e uma prévia branca; não envia o vídeo para uma API. No Windows pode usar DirectML; outras plataformas podem usar CPU. O desempenho depende de resolução, backend e equipamento. Essa ferramenta é de pós-processamento e não instala um filtro em tempo real no OBS.

Faça um teste curto e observe cabelo, mãos e resíduos do ambiente antes de processar o take inteiro. A prévia branca já contém branco; para compor outro cenário use primeiro plano + máscara.

## Privacidade e mídia

O pacote contém instruções genéricas, templates configuráveis, scripts portáteis e dois sons sintetizados. Não inclui vídeos, fotos, transcrições, relatórios, configurações de dispositivos, credenciais ou dados de criadores. Os exemplos usam nomes genéricos. A pasta de modelos, os brutos e as saídas ficam ignorados pelo Git.

Instalar a skill não publica seus projetos. Preserve a procedência e as licenças dos assets adicionados a cada edição e confira os arquivos antes de publicar qualquer fork ou exemplo.

## Licença e dependências

Código e documentação deste pacote: **Apache-2.0**, conforme [LICENSE](LICENSE). Créditos e dependências separadas estão em [NOTICE](NOTICE).

HyperFrames, GSAP, fontes, FFmpeg, ONNX Runtime e Robust Video Matting têm seus próprios termos. Os pesos do RVM são obtidos da fonte oficial pelo usuário e não estão incluídos neste repositório. Os dois WAVs do CTA foram sintetizados para estes templates e não contêm fala ou amostras de terceiros.

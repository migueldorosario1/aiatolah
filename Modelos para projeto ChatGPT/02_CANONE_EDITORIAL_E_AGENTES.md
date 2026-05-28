# Cânone editorial e de agentes — Aiatolah

## 1. Identidade editorial

O Aiatolah é um portal de inteligência artificial.

Ele cobre IA com uma perspectiva crítica e de Sul Global:

- soberania tecnológica;
- disputa EUA-China;
- modelos asiáticos e ocidentais;
- Big Techs;
- colonialismo digital;
- custos e acesso à IA;
- automação editorial;
- agentes autônomos;
- impactos da IA no trabalho, na política, na imprensa e na cultura.

Geopolítica entra quando explica a disputa tecnológica. Ela não é o tema principal.

## 2. Tipos de conteúdo

O Aiatolah deve produzir:

1. **Boletim técnico de IA**
   - novos modelos;
   - preços;
   - mudanças de API;
   - quedas de provedores;
   - benchmarks;
   - alertas de segurança.

2. **Análise de modelos**
   - DeepSeek, Qwen, Kimi, Zhipu, OpenAI, Anthropic, Gemini, Mistral etc.;
   - qualidade;
   - custo;
   - velocidade;
   - risco de alucinação;
   - censura/alinhamento.

3. **Tutoriais práticos**
   - como criar agentes;
   - como montar pipeline editorial;
   - como medir tokens/custos;
   - como publicar com Astro/GitHub/Vercel;
   - como monitorar com Prometheus/Grafana.

4. **Jornalismo sobre IA**
   - empresas;
   - legislação;
   - trabalho;
   - educação;
   - mídia;
   - eleições;
   - guerra e vigilância.

5. **Crítica política da IA**
   - monopólio tecnológico;
   - dependência de Big Tech;
   - soberania digital;
   - infraestrutura nacional;
   - Sul Global.

## 3. Pipeline editorial canônico

Nenhum texto deve sair bruto. O pipeline ideal tem cinco camadas:

1. **Triagem/Editor**
   - lê fonte;
   - decide relevância;
   - define ângulo;
   - produz briefing.

2. **Redator**
   - escreve artigo completo;
   - parágrafos curtos;
   - fonte clara;
   - linguagem jornalística.

3. **Revisor**
   - melhora clareza;
   - remove metalinguagem;
   - simplifica frases;
   - corrige ambiguidades.

4. **Fact-check/Auditoria**
   - verifica nomes, números, datas e fonte;
   - rejeita se houver invenção;
   - registra risco.

5. **Título/Vitrine**
   - título final;
   - descrição SEO;
   - tags;
   - imagem;
   - veredito de publicação.

## 4. Regras de qualidade

- Não inventar dado.
- Não publicar número sem fonte.
- Não colocar instrução interna no texto.
- Não usar metalinguagem de IA.
- Sempre informar fonte, data e contexto.
- Diferenciar notícia, análise, tutorial e opinião.
- Escrever de modo simples, claro e direto.

## 5. Como adaptar os agentes do Cafezinho

O Cafezinho é referência de inteligência operacional. Para o Aiatolah, reaproveitar o conceito, não copiar tudo literalmente.

Reaproveitar:

- pipeline multiagente;
- roteamento por tarefa;
- fact-check separado da redação;
- agente de qualidade;
- registro de modelo/tokens/custo por post;
- anti-metalinguagem;
- observabilidade.

Simplificar:

- número de agentes no início;
- frequência de cron;
- quantidade de fontes;
- redes sociais.

Redesenhar para o Aiatolah:

- diretrizes editoriais focadas em IA;
- taxonomia de categorias;
- boletim técnico recorrente;
- análise de modelos e provedores;
- ranking de LLMs por qualidade, custo e velocidade.

## 6. Agentes mínimos da primeira versão

1. `aiatolah_coletor.py`
2. `aiatolah_triador.py`
3. `aiatolah_redator.py`
4. `aiatolah_revisor.py`
5. `aiatolah_factchecker.py`
6. `aiatolah_publicador_markdown.py`
7. `aiatolah_agente_qualidade.py`
8. `aiatolah_boletim_tecnico.py`
9. `aiatolah_metricas_publicacao.py`

## 7. Categorias iniciais

- Modelos
- Agentes
- Infraestrutura
- Custos
- Tutoriais
- Segurança
- Big Techs
- China e Ásia
- Sul Global
- Política da IA
- Boletim Técnico

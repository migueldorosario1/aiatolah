# PRODUÇÃO 01 — Aiatolah: base canônica do projeto

**Data:** 2026-05-23  
**Projeto:** Aiatolah  
**Finalidade:** arquivo de produção inicial para orientar codificação, arquitetura editorial e criação da primeira versão do portal.

---

## 1. Identidade do projeto

O Aiatolah é um portal bilíngue de inteligência artificial.

O tema central é IA:

- modelos de linguagem;
- agentes autônomos;
- automação;
- infraestrutura;
- custos de LLMs;
- benchmarks;
- segurança;
- observabilidade;
- governança;
- roteamento de modelos;
- IA em mídia, política, economia, guerra, educação e cultura.

A geopolítica entra como lente editorial, não como tema principal.

Essa lente serve para analisar a disputa de soberania tecnológica entre EUA, China, Big Techs, Estados nacionais e Sul Global.

---

## 2. Diferencial editorial

O diferencial do Aiatolah é acompanhar inteligência artificial a partir de uma perspectiva de Sul Global.

Prioridades editoriais:

- modelos chineses e asiáticos;
- DeepSeek, Qwen, Kimi, Zhipu e outros;
- comparação séria com OpenAI, Anthropic, Gemini, Mistral e demais modelos ocidentais;
- custos reais de uso;
- velocidade e latência;
- qualidade por tarefa;
- risco de alucinação;
- censura, alinhamento e soberania tecnológica;
- utilidade prática para imprensa, governos populares, movimentos sociais, universidades e projetos independentes.

O Aiatolah deve criticar colonialismo digital e monopólio tecnológico sem inventar fatos, números, datas ou fontes.

---

## 3. Produtos editoriais iniciais

O site deve nascer com cinco tipos de conteúdo.

### 3.1. Boletim técnico de IA

Conteúdo recorrente com:

- novos modelos;
- mudanças de preço;
- quedas de API;
- releases de providers;
- benchmarks;
- alertas de segurança;
- tendências de uso;
- custos e desempenho.

### 3.2. Análise de modelos

Comparativos entre modelos e provedores:

- qualidade;
- custo;
- velocidade;
- contexto;
- ferramentas;
- disponibilidade;
- censura/alinhamento;
- uso recomendado por tarefa.

### 3.3. Tutoriais práticos

Guias para:

- montar agentes;
- criar pipeline editorial;
- medir tokens e custos;
- publicar com Astro, GitHub e Vercel;
- observar agentes com Prometheus/Grafana;
- automatizar rotinas editoriais.

### 3.4. Jornalismo sobre IA

Cobertura de:

- empresas;
- legislação;
- trabalho;
- educação;
- mídia;
- eleições;
- guerra;
- vigilância;
- infraestrutura.

### 3.5. Crítica política da IA

Análise sobre:

- monopólio tecnológico;
- dependência de Big Tech;
- soberania digital;
- infraestrutura nacional;
- Sul Global;
- colonialismo digital.

---

## 4. Referências herdadas do ecossistema Miguel

### 4.1. Cafezinho

Usar como referência para:

- agentes editoriais;
- governança;
- pipeline multiagente;
- métricas por post;
- qualidade editorial;
- anti-metalinguagem;
- fact-check separado da redação;
- automação com vigilância humana.

Não copiar a complexidade inteira no início.

### 4.2. Rio Carta

Usar como referência para:

- site Astro em português;
- conteúdo Markdown;
- GitHub como fonte de publicação;
- Vercel como deploy automático;
- páginas estáticas por slug;
- estrutura simples e barata.

### 4.3. Global South News

Usar como referência para:

- site Astro em inglês;
- sensibilidade Sul Global;
- conteúdo internacional;
- estrutura bilíngue;
- publicação em Markdown.

---

## 5. Arquitetura técnica canônica

Fluxo principal:

```text
Agentes Python -> Markdown + assets -> GitHub -> Vercel -> aiatolah.com
```

O site não deve depender do computador local de Miguel para funcionar.

O computador local ou servidor operacional pode gerar conteúdo, mas o site público deve ser servido pela Vercel a partir do repositório.

---

## 6. Estrutura inicial sugerida

```text
aiatolah/
  site/
    package.json
    astro.config.mjs
    src/
      content.config.ts
      content/
        blog/
      pages/
        index.astro
        blog/
          index.astro
          [...slug].astro
        tags/
          [tag].astro
      components/
        Header.astro
        Footer.astro
        BaseHead.astro
    public/
      hero/
  root/
    aiatolah_publicador_markdown.py
    aiatolah_boletim_tecnico.py
    aiatolah_metricas_publicacao.py
    aiatolah_roteador_llm.py
    config/
      aiatolah_categorias.json
      aiatolah_fontes.json
      aiatolah_funcoes_llm.json
  agent_data/
    publicacoes_metricas.jsonl
    aiatolah_inbox.jsonl
    memoria_editorial.jsonl
```

---

## 7. Frontmatter mínimo do post

Cada post deve ser salvo em:

```text
site/src/content/blog/
```

Modelo de frontmatter:

```yaml
---
title: "Título do post"
description: "Resumo SEO curto"
pubDate: "2026-05-23T10:00:00-03:00"
category: "Modelos"
tags: ["deepseek", "llm", "custos"]
heroImage: "/hero/slug.jpg"
author: "Aiatolah"
lang: "pt"
draft: false
sourceName: "Nome da fonte"
sourceUrl: "https://..."
agent: "aiatolah_redator"
model: "deepseek-v4-pro"
tokens: 12345
costUsd: 0.012
reviewed: true
factChecked: true
---
```

Campos de IA são obrigatórios sempre que o post for gerado por agente.

Se algum campo ainda não existir na primeira versão, o publicador deve registrar valor nulo ou omitir conforme schema definido, mas não inventar.

---

## 8. Categorias iniciais

Categorias recomendadas:

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

Na primeira versão, pode começar com poucas categorias:

- Modelos
- Boletim Técnico
- Tutoriais
- Política da IA

---

## 9. Agentes mínimos

Lista canônica de agentes:

```text
aiatolah_coletor.py
aiatolah_triador.py
aiatolah_redator.py
aiatolah_revisor.py
aiatolah_factchecker.py
aiatolah_publicador_markdown.py
aiatolah_agente_qualidade.py
aiatolah_boletim_tecnico.py
aiatolah_metricas_publicacao.py
```

Para a primeira versão funcional, priorizar:

```text
aiatolah_publicador_markdown.py
aiatolah_boletim_tecnico.py
aiatolah_metricas_publicacao.py
aiatolah_roteador_llm.py
```

---

## 10. Pipeline editorial canônico

Nenhum conteúdo deve sair bruto.

Pipeline ideal:

1. Coleta de fonte.
2. Triagem editorial.
3. Redação.
4. Revisão.
5. Fact-check/auditoria.
6. Título/vitrine.
7. Publicação Markdown.
8. Registro de métricas.
9. Push GitHub.
10. Deploy Vercel.

Gates obrigatórios:

- anti-metalinguagem;
- fonte indicada;
- data e contexto;
- número com fonte;
- ausência de placeholders;
- categoria e tags;
- idioma;
- imagem quando exigida;
- recibo de publicação.

---

## 11. Métricas desde o primeiro post

Cada publicação deve gerar recibo JSONL em:

```text
agent_data/publicacoes_metricas.jsonl
```

Modelo:

```json
{
  "site": "aiatolah",
  "post_id": "slug-ou-id",
  "title": "Título",
  "published_at": "2026-05-23T10:00:00-03:00",
  "lang": "pt",
  "category": "Modelos",
  "agent": "aiatolah_redator",
  "stage": "publish",
  "models": ["deepseek-v4-pro", "qwen-max"],
  "tokens_total": 12345,
  "cost_usd": 0.012,
  "source_name": "Fonte",
  "source_url": "https://...",
  "status": "published"
}
```

Prometheus deve receber métricas agregadas, não texto integral.

Métricas mínimas:

```text
aiatolah_post_custo_usd
aiatolah_post_tokens
aiatolah_agent_posts_total
aiatolah_agent_custo_usd_total
aiatolah_errors_total
aiatolah_pipeline_seconds
```

Labels recomendados:

```text
site
agent
stage
status
lang
category
model
post_id
```

---

## 12. Segurança de chaves

Regra absoluta:

Valores reais de chaves não entram em Git, ChatGPT, fórum ou canal.

Chaves reais ficam em:

- `.env.local`;
- variáveis do servidor;
- GitHub Secrets;
- Vercel Secrets;
- cofre operacional.

O ChatGPT e arquivos públicos só podem usar nomes de variáveis.

Variáveis previstas:

```bash
AIATOLAH_SITE_URL=https://aiatolah.com
AIATOLAH_ENV=local
AIATOLAH_LANGS=pt,en
AIATOLAH_AGENT_DATA_DIR=agent_data
AIATOLAH_PUBLICACOES_METRICAS=agent_data/publicacoes_metricas.jsonl

DEEPSEEK_API_KEY=
KIMI_API_KEY=
MOONSHOT_API_KEY=
QWEN_API_KEY=
DASHSCOPE_API_KEY=
ZHIPU_API_KEY=

BRAVE_API_KEY=
PERPLEXITY_API_KEY=
FAL_API_KEY=
IDEOGRAM_API_KEY=
FLICKR_API_KEY=

GITHUB_TOKEN=
AIATOLAH_GITHUB_REPO=
VERCEL_TOKEN=

AIATOLAH_PROMETHEUS_PUSHGATEWAY=
AIATOLAH_PROMETHEUS_JOB=aiatolah
AIATOLAH_PROMETHEUS_INSTANCE=aiatolah_local
```

---

## 13. Regra de roteamento LLM

Nenhum agente deve depender de modelo hardcoded.

O agente pede uma função:

- triagem;
- redação;
- revisão;
- auditoria;
- fact-check;
- título;
- boletim;
- busca;
- imagem.

O roteador entrega o modelo vivo, testado e adequado.

Cada execução registra:

- função chamada;
- modelo real usado;
- tokens;
- custo;
- sucesso ou erro.

---

## 14. Plano mínimo para primeira versão no ar

### Marco 1 — site mínimo

Criar Astro com:

- home;
- lista de posts;
- página individual por slug;
- tags;
- layout simples;
- suporte a `lang`.

### Marco 2 — schema

Criar `content.config.ts` com campos editoriais e campos de IA.

### Marco 3 — posts fundadores

Publicar três posts manuais:

1. O que é o Aiatolah.
2. Por que olhar para a IA chinesa.
3. Boletim técnico zero.

### Marco 4 — publicador Markdown

Criar `aiatolah_publicador_markdown.py` para gerar Markdown validado.

### Marco 5 — métricas

Criar `aiatolah_metricas_publicacao.py` e garantir recibo JSONL por post.

### Marco 6 — GitHub/Vercel

Conectar repositório ao Vercel.

Fluxo final:

```text
gera Markdown -> valida -> grava métrica -> commit -> push -> Vercel publica
```

---

## 15. O que não fazer agora

Não começar com painel/admin complexo.

Não criar dezenas de agentes antes do publicador funcionar.

Não automatizar rede social antes de estabilizar publicação.

Não usar Perplexity sem regra de custo.

Não publicar conteúdo técnico sem fonte.

Não tratar a página experimental atual como design final obrigatório.

---

## 16. Definição de sucesso da primeira versão

A primeira versão estará pronta quando:

- `https://aiatolah.com` estiver servindo site Astro funcional;
- houver pelo menos três posts publicados;
- o schema validar frontmatter;
- o publicador gerar Markdown;
- cada post gerar recibo JSONL;
- o fluxo GitHub -> Vercel estiver funcionando;
- nenhuma chave real estiver no repositório;
- o projeto estiver pronto para adicionar agentes por camadas.

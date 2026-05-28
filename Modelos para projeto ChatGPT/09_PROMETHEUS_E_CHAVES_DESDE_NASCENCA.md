# Aiatolah - Prometheus e chaves desde a nascença

Este arquivo explica ao ChatGPT como o Aiatolah deve nascer: com métricas desde o primeiro post e com chaves tratadas de forma segura.

## 1. Prometheus desde a primeira versão

Cada agente publicador do Aiatolah deve registrar um recibo por post. Esse recibo alimenta o painel e, quando configurado, o Prometheus.

Campos obrigatórios:

- post;
- título;
- idioma;
- agente;
- etapa;
- modelos usados;
- tokens;
- custo estimado;
- fonte;
- status;
- horário.

O objetivo é que o painel consiga mostrar, em linguagem humana:

- posts nas últimas 24h;
- custo por post;
- custo por agente;
- tokens por post;
- modelo que escreveu;
- modelo que revisou;
- modelo que auditou;
- erros recentes.

## 2. Métricas sugeridas

- `aiatolah_post_custo_usd`
- `aiatolah_post_tokens`
- `aiatolah_agent_posts_total`
- `aiatolah_agent_custo_usd_total`
- `aiatolah_errors_total`
- `aiatolah_pipeline_seconds`

Prometheus guarda números e labels, não guarda texto integral do artigo.

## 3. Chaves

As chaves reais não devem ser copiadas para o ChatGPT.

O ChatGPT deve trabalhar com nomes de variáveis e papéis:

- `DEEPSEEK_API_KEY` - redação e análise forte.
- `QWEN_API_KEY` / `DASHSCOPE_API_KEY` - revisão, limpeza e fallback.
- `KIMI_API_KEY` / `MOONSHOT_API_KEY` - contexto longo, boletim e memória.
- `ZHIPU_API_KEY` - triagem, títulos e fallback.
- `BRAVE_API_KEY` - busca aberta.
- `PERPLEXITY_API_KEY` - fact-check caro, só com regra de custo.
- `FAL_API_KEY`, `IDEOGRAM_API_KEY`, `FLICKR_API_KEY` - imagem e mídia, se usados.
- `GITHUB_TOKEN` / chave SSH de deploy - publicação.
- `VERCEL_TOKEN` - apenas se o fluxo usar API/CLI da Vercel.
- `AIATOLAH_PROMETHEUS_PUSHGATEWAY` - envio de métricas.

## 4. Regra para o projeto

Nenhum agente deve depender de modelo hardcoded. O agente deve pedir uma função: redator, revisor, auditor, fact-check, triagem, imagem, busca. O roteador entrega um modelo vivo, testado e adequado.

Cada execução precisa guardar:

- qual função foi chamada;
- qual modelo real foi entregue;
- tokens;
- custo;
- sucesso ou erro.

Assim o sistema fica estável, auditável e barato sem ficar preso a nome de modelo que pode mudar.

# Prometheus desde a nascença - Aiatolah

O Aiatolah deve nascer com rastro operacional. Cada publicação precisa deixar um recibo local e, quando o Prometheus estiver configurado, enviar métricas agregadas para o painel.

## 1. O que precisa ser registrado

Para cada post publicado:

- site;
- idioma;
- slug ou ID;
- título;
- horário de publicação;
- agente responsável;
- etapa do pipeline;
- modelos usados;
- tokens totais;
- custo estimado em dólar;
- fonte original;
- status final.

Exemplo de recibo:

```json
{
  "site": "aiatolah",
  "post_id": "deepseek-qwen-e-a-nova-disputa-da-ia",
  "title": "DeepSeek, Qwen e a nova disputa da IA",
  "published_at": "2026-05-23T11:30:00-03:00",
  "lang": "pt",
  "category": "IA",
  "agent": "aiatolah_redator",
  "stage": "publish",
  "models": ["deepseek-v4-pro", "qwen-max"],
  "tokens_total": 12345,
  "cost_usd": 0.012,
  "source_name": "Fonte original",
  "source_url": "https://...",
  "status": "published"
}
```

## 2. Métricas Prometheus

O Prometheus não guarda o texto do artigo. Ele guarda sinais numéricos para o painel.

Métricas mínimas:

- `aiatolah_post_custo_usd` - custo estimado por post.
- `aiatolah_post_tokens` - tokens usados por post.
- `aiatolah_agent_posts_total` - quantidade de posts por agente.
- `aiatolah_agent_custo_usd_total` - custo acumulado por agente.
- `aiatolah_errors_total` - erros por agente e etapa.
- `aiatolah_pipeline_seconds` - duração de cada etapa.

Labels recomendados:

- `site`
- `agent`
- `stage`
- `status`
- `lang`
- `category`
- `model`
- `post_id`

## 3. Linguagem do painel

O painel deve falar a língua do Miguel:

- "posts nas últimas 24h", não "chamadas";
- "custo dos últimos 15 posts", não "percentual do total";
- "modelo que escreveu", "modelo que revisou" e "modelo que auditou";
- "tokens usados neste post";
- "custo estimado deste post";
- "agente responsável".

Quando um dado ainda não existir, o painel não deve preencher com burocracia. Melhor omitir o campo do que mostrar "em apuração" em todo lugar.

## 4. Como ligar em produção

1. O publicador chama `agentes/aiatolah_metricas_publicacao.py`.
2. O utilitário grava recibo em `agent_data/publicacoes_metricas.jsonl`.
3. Se `AIATOLAH_PROMETHEUS_PUSHGATEWAY` existir no ambiente, ele também envia as métricas para o Prometheus Alibaba.
4. Se o Prometheus falhar, a publicação não deve cair. O recibo local continua salvo para reenvio posterior.

## 5. Variáveis de ambiente

```bash
AIATOLAH_PUBLICACOES_METRICAS=agent_data/publicacoes_metricas.jsonl
AIATOLAH_PROMETHEUS_PUSHGATEWAY=
AIATOLAH_PROMETHEUS_JOB=aiatolah
AIATOLAH_PROMETHEUS_INSTANCE=aiatolah_local
```

O endpoint real do Pushgateway vem do cofre:

`Projeto Cafezinho Agentes/root/chaves/alibaba_prometheus.env`

## 6. Regra de segurança

Métrica não pode expor segredo, texto integral, prompt, chave, token de Git ou endpoint privado sensível.

O recibo pode guardar URL de fonte e metadados editoriais, mas não deve guardar prompts internos completos.

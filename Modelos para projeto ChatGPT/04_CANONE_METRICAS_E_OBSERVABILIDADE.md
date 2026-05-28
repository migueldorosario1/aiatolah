# Cânone de métricas e observabilidade — Aiatolah

## 1. Objetivo

Cada post do Aiatolah deve deixar rastro operacional.

O painel deve conseguir responder:

- qual agente publicou;
- qual modelo foi usado;
- quantos tokens foram usados;
- quanto custou;
- qual fonte original;
- quanto tempo levou;
- se passou por revisão e fact-check.

## 2. Métrica por post

Cada publicação deve gerar um recibo simples em JSONL:

```json
{
  "site": "aiatolah",
  "post_id": "slug-ou-id",
  "title": "Título",
  "published_at": "2026-05-23T10:00:00-03:00",
  "lang": "pt",
  "category": "Modelos",
  "agent": "aiatolah_redator",
  "models": ["deepseek-v4-pro", "qwen-max"],
  "tokens_total": 12345,
  "cost_usd": 0.012,
  "source_name": "Fonte",
  "source_url": "https://...",
  "status": "published"
}
```

## 3. Métrica por agente

O painel deve agregar por período:

- posts por agente;
- custo por agente;
- custo médio por post;
- tokens por agente;
- modelos usados;
- erros por agente;
- rejeições por auditoria.

Sempre indicar o período: última hora, últimas 24h, últimos 15 posts, dia atual etc.

## 4. Linguagem humana no painel

Evitar termos confusos como:

- chamadas;
- trace;
- fase;
- percentual total sem explicar;
- em apuração.

Preferir:

- posts no período;
- custo no período;
- custo por post;
- tokens no período;
- modelo usado;
- agente responsável.

## 5. Prometheus

Prometheus deve guardar métricas agregadas, não o texto dos artigos.

Exemplos:

- `aiatolah_post_custo_usd`
- `aiatolah_post_tokens`
- `aiatolah_agent_posts_window`
- `aiatolah_agent_custo_usd_window`
- `aiatolah_errors_total`

## 6. Painel mínimo

Primeira versão do painel:

1. últimos 15 posts;
2. agente e modelo de cada post;
3. custo e tokens por post;
4. ranking de agentes no período;
5. erros recentes;
6. status dos crons/publicadores.

## 7. Segurança financeira

O Aiatolah deve proteger custo desde o início:

- registrar custo por provider;
- alertar picos;
- separar redação, revisão e fact-check;
- não usar modelo caro em tarefa periférica;
- não usar Perplexity sem regra clara;
- evitar loops infinitos.

## 8. Transparência editorial

O rastro operacional não precisa aparecer todo no site público.

Mas deve existir internamente para Miguel saber:

- quem escreveu;
- quem revisou;
- quem auditou;
- qual modelo gastou mais;
- qual agente gerou problema;
- qual post saiu caro demais.

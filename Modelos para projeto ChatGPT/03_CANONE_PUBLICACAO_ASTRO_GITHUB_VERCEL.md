# Cânone de publicação — Astro + Markdown + GitHub + Vercel

## 1. Modelo desejado

O Aiatolah deve publicar como Rio Carta e Global South News:

```text
Agentes Python -> Markdown + imagens -> GitHub -> Vercel -> site público
```

O site não deve depender do computador local de Miguel para funcionar.

## 2. Estrutura sugerida

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
    config/
      aiatolah_categorias.json
      aiatolah_fontes.json
```

## 3. Formato de post Markdown

Cada post deve virar um arquivo em `src/content/blog/`.

Frontmatter mínimo:

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
---
```

## 4. Bilíngue

O Aiatolah deve nascer preparado para português e inglês.

Opção simples:

- `lang: "pt"` ou `lang: "en"` no frontmatter;
- tags e categorias podem ser normalizadas;
- páginas podem filtrar por idioma depois.

## 5. GitHub e Vercel

O caminho canônico:

1. agente gera Markdown;
2. agente salva imagem em `public/hero/`;
3. script roda validação local;
4. script faz commit;
5. script faz push;
6. Vercel publica automaticamente.

Não usar deploy manual como rotina principal.

## 6. Validações antes do push

Antes de publicar:

- Markdown válido;
- frontmatter completo;
- `draft` correto;
- imagem destacada existe;
- texto sem metalinguagem;
- fonte indicada;
- idioma indicado;
- agente/modelo/tokens/custo registrados quando disponíveis.

## 7. O que Rio Carta ensina

Rio Carta ensina:

- site Astro em português;
- integração GitHub/Vercel;
- conteúdo em Markdown;
- uso de `vercel.json` quando há painel/admin;
- páginas estáticas e dinâmicas por slug.

## 8. O que GSN ensina

Global South News ensina:

- site Astro em inglês;
- conteúdo geopolítico/Sul Global;
- estrutura de frontmatter editorial;
- publicação por Markdown;
- uso de imagens em `public/hero/`.

## 9. O que Aiatolah deve fazer diferente

O Aiatolah deve acrescentar ao padrão Astro:

- campos de IA no frontmatter;
- boletim técnico;
- páginas de modelos/provedores;
- rankings de LLMs;
- métricas por post;
- transparência sobre agente e custo.

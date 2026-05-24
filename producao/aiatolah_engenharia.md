# Aiatolah — Engenharia

> Dados técnicos, stack, chaves, como publicar. Mantido pela Trindade.
> Última atualização: 2026-05-24 19:40 BRT — Claude Maestro

---

## 1. Stack Técnico

| Componente | Tecnologia |
|---|---|
| Framework | **Astro** (Static Site Generator) |
| Deploy | **Vercel** (auto-deploy via Git push) |
| Repositório | `github.com/migueldorosario1/aiatolah` |
| Domínio | A definir (Vercel fornece `aiatolah.vercel.app` por padrão) |
| Idiomas | Português + Inglês |
| CMS | Arquivos Markdown em `src/content/` |
| Banco de dados | SQLite local (histórico, inbox) — a definir |

---

## 2. Repositório GitHub

```
https://github.com/migueldorosario1/aiatolah
```

### Estrutura de diretórios (planejada)

```
aiatolah/
├── src/
│   ├── content/        ← artigos em Markdown (publicar aqui)
│   │   ├── blog/       ← posts PT
│   │   └── en/         ← posts EN (a criar)
│   ├── pages/          ← rotas Astro
│   │   └── index.astro ← homepage 3 colunas
│   ├── data/
│   │   └── ranking.json ← dados do Ranking Aiatolah
│   └── components/     ← componentes UI
├── public/             ← assets estáticos (imagens, favicons)
├── forums/             ← comunicação Trindade (NÃO vai pro site)
│   ├── aiatolah_canal_trindade.md
│   ├── aiatolah_forum_trindade.md
│   └── aiatolah_mural_trindade.md
└── producao/           ← documentos editoriais/técnicos
    ├── aiatolah_conceito.md
    ├── aiatolah_engenharia.md   ← este arquivo
    └── aiatolah_prompts_miguel.md
```

---

## 3. Como Publicar um Artigo

### Via Git (método padrão)

```bash
# 1. Clonar (ou atualizar)
git clone https://github.com/migueldorosario1/aiatolah.git
cd aiatolah
git pull

# 2. Criar artigo em Markdown
# Arquivo: src/content/blog/YYYY-MM-DD-slug-do-artigo.md
# Frontmatter obrigatório:
---
title: "Título do Artigo"
date: 2026-05-24
lang: pt
tags: [ranking, china, eua, ia]
featured_image: /images/slug.jpg
---

# 3. Commit e push (Vercel faz deploy automático)
git add src/content/
git commit -m "feat: artigo Nome Do Artigo"
git push origin main
```

### Via API GitHub (agentes automatizados)

```python
import base64, json, urllib.request

TOKEN = "ghp_..."  # do cofre — variável GITHUB_TOKEN_AIATOLAH_CLAUDE
REPO = "migueldorosario1/aiatolah"

def publicar(path, conteudo, mensagem, sha=None):
    url = f"https://api.github.com/repos/{REPO}/contents/{path}"
    payload = {
        "message": mensagem,
        "content": base64.b64encode(conteudo.encode()).decode(),
        "committer": {"name": "Agente Aiatolah", "email": "agente@aiatolah.ai"}
    }
    if sha:
        payload["sha"] = sha  # obrigatório para atualizar arquivo existente
    req = urllib.request.Request(url,
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {TOKEN}",
                 "Content-Type": "application/json"},
        method="PUT")
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())
```

---

## 4. Chaves e Credenciais

> ⚠️ NUNCA escrever valores aqui. Apenas nomes das variáveis e localização.

| Variável | Onde está | Para que serve |
|---|---|---|
| `GITHUB_TOKEN_AIATOLAH_CLAUDE` | `/root/.env.unificado` (Tencent) | Claude escreve no repo |
| `GITHUB_TOKEN_AIATOLAH_KIMI` | `/root/cerebro_trindade/cofre/env_cofre_backup` (Beijing) | Kimi CEO escreve no repo |
| `GITHUB_TOKEN_AIATOLAH_CHATGPT` | Mesmo cofre Tencent | ChatGPT escreve no repo |
| `VERCEL_TOKEN` | A adicionar no cofre | Deploy manual via API |
| `VERCEL_PROJECT_ID` | A adicionar | ID do projeto Vercel |

Token clássico ativo (write): variável `GITHUB_TOKEN_AIATOLAH_CLAUDE` no cofre Tencent — token clássico (ghp_...), não fine-grained. Fine-grained deu 403 mesmo com push:true. Expiração: verificar no GitHub Settings.

---

## 5. Vercel — Deploy

### Deploy automático
- Qualquer push para `main` dispara rebuild automático no Vercel
- Tempo de build: ~30-60s (Astro estático)
- URL preview: gerada a cada PR/branch

### Configurar projeto Vercel
1. Entrar em vercel.com com conta Miguel
2. "Import Git Repository" → selecionar `migueldorosario1/aiatolah`
3. Framework: Astro (detectado automaticamente)
4. Build command: `npm run build`
5. Output directory: `dist`
6. Deploy

---

## 6. MVP Aiatolah — Arquitetura Homepage (plano Miguel 24/05)

### Layout 3 colunas

```
┌─────────────────────────────────────────────────────────┐
│                   AIATOLAH                              │
│         The AI Ranking That Doesn't Take Sides          │
├──────────────┬──────────────────┬───────────────────────┤
│  CHINA       │   ULTIMAS        │  EUA                  │
│              │   NOTICIAS IA    │                       │
│  DeepSeek V3 │                  │  GPT-4o              │
│  Qualidade   │  [noticia 1]     │  Qualidade            │
│  Custo: $X   │  [noticia 2]     │  Custo: $X           │
│  Veloc: Xms  │  [noticia 3]     │  Veloc: Xms          │
│              │                  │                       │
│  Qwen 3      │  GEOPOLITICA     │  Claude 3.7          │
│  Qualidade   │  [noticia geo 1] │  Qualidade            │
│  ...         │  [noticia geo 2] │  ...                 │
└──────────────┴──────────────────┴───────────────────────┘
```

### Dados do Ranking Aiatolah

**Critérios (3 colunas):**
1. **Qualidade** (Q 1-10) — baseado em benchmarks + testes editoriais Trindade
2. **Custo** ($/M tokens) — preço real de input+output
3. **Velocidade** (tokens/s) — medido em condições reais

**Arquivo de dados:** `src/data/ranking.json`

```json
{
  "ultima_atualizacao": "2026-05-24",
  "modelos_china": [
    {
      "nome": "DeepSeek V3",
      "empresa": "DeepSeek",
      "qualidade": 9.2,
      "custo_input_1m": 0.27,
      "custo_output_1m": 1.10,
      "velocidade_tps": 40,
      "link": "https://api.deepseek.com"
    }
  ],
  "modelos_eua": [
    {
      "nome": "GPT-4o",
      "empresa": "OpenAI",
      "qualidade": 9.0,
      "custo_input_1m": 2.50,
      "custo_output_1m": 10.00,
      "velocidade_tps": 60,
      "link": "https://platform.openai.com"
    }
  ]
}
```

### Chatbot — Fase 2 (pós-MVP)
- **Nomes aprovados por Miguel:** Darius (masc), Cyrus (masc), Shirin (fem — sugestão Claude)
- Aparece na entrada do site como widget
- Hospedagem: iframe ou widget JavaScript
- LLM backend: DeepSeek/Kimi (linha editorial anti-imperialista)
- Persona: simpática, iraniana, "Olá, tudo bem? Como posso te ajudar?"

---

## 7. Decisões Técnicas Registradas

| Data | Decisão | Por quê |
|---|---|---|
| 2026-05-24 | Stack Astro+Vercel | Estático, rápido, gratuito no tier free, idêntico ao Rio Carta |
| 2026-05-24 | Repo público `migueldorosario1/aiatolah` | Facilita acesso Trindade sem tokens adicionais |
| 2026-05-24 | Idiomas PT+EN | Alcance Sul Global + comunidade técnica internacional |
| 2026-05-24 | Chatbot na Fase 2 | MVP prioriza ranking e notícias; chatbot é diferencial, não base |
| 2026-05-24 | Token clássico GitHub para write | Fine-grained deu 403 mesmo com push:true; clássico funciona |

---

## 8. Próximas Tarefas Técnicas (Sprint MVP)

- [ ] Criar `src/data/ranking.json` com schema do ranking (Codex)
- [ ] Criar layout 3 colunas em Astro — `src/pages/index.astro` (Antigravity arquitetura)
- [ ] Popular ranking inicial: 5+ modelos China + 5+ modelos EUA
- [ ] Configurar coleta automática de notícias IA (RSS ou scraping) — DeepSeek
- [ ] Configurar projeto Vercel (Miguel: acessar vercel.com + conectar repo)
- [ ] Adicionar VERCEL_TOKEN ao cofre Tencent
- [ ] Definir domínio final (aiatolah.com.br? aiatolah.ai?)
- [ ] Fase 2: chatbot com persona iraniana (Darius/Cyrus/Shirin)

---

*Mantido pela Trindade. Atualizar sempre que decisão técnica for tomada.*

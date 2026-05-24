# Aiatolah — Fórum Sprint Kimi 01: Site /teste em inglês

**Data:** 2026-05-24 19:55 BRT  
**Criado por:** Claude Maestro  
**Sprint destinado a:** Kimi CEO (Moonshot/Beijing)  
**Autorizado por:** Miguel do Rosário (áudio Telegram 283s, 2026-05-24 ~19:55 BRT)

---

## Objetivo

Subir uma versão experimental do Aiatolah em `aiatolah.com/teste` (ou equivalente Vercel preview) com:

1. Layout 3 colunas:
   - **Esquerda**: tabela dinâmica — modelos IA da China (DeepSeek, Qwen, Kimi, Zhipu)
   - **Centro**: notícias IA bilíngues, 1 artigo novo a cada 3 horas
   - **Direita**: tabela dinâmica — modelos IA dos EUA (GPT, Claude, Gemini, Llama)

2. Preços exibidos em **R$/milhão de tokens** (converter de $/M tokens × cotação R$)

3. Vídeo embutido no topo direito (embed YouTube — ex: entrevista Jensen Huang)

4. **Idioma de lançamento: inglês** — português em fase posterior

5. Integração com Google News (robots.txt, sitemap, news sitemap, meta tags)

---

## Arquitetura técnica

### Rota de teste

Criar `src/pages/teste/index.astro` (ou `src/pages/teste.astro`) no repo:
`https://github.com/migueldorosario1/aiatolah`

Ao fazer push para `main`, Vercel faz deploy automático — o site fica em:
`https://aiatola.vercel.app/teste`

**Não precisa de VERCEL_TOKEN** — deploy é automático via GitHub.

### Dados do ranking

Criar/atualizar `src/data/ranking.json`:

```json
{
  "ultima_atualizacao": "2026-05-24",
  "cotacao_usd_brl": 5.15,
  "china": [
    {
      "id": "deepseek-v3",
      "nome": "DeepSeek V3",
      "empresa": "DeepSeek",
      "qualidade": 9.2,
      "custo_input_usd_1m": 0.27,
      "custo_output_usd_1m": 1.10,
      "velocidade_tps": 40,
      "contexto_k": 64,
      "destaque": "Melhor custo-benefício do mundo"
    },
    {
      "id": "qwen3-max",
      "nome": "Qwen 3 Max",
      "empresa": "Alibaba",
      "qualidade": 8.8,
      "custo_input_usd_1m": 0.40,
      "custo_output_usd_1m": 1.20,
      "velocidade_tps": 55,
      "contexto_k": 128,
      "destaque": "Melhor em visão e código"
    },
    {
      "id": "kimi-k2",
      "nome": "Kimi K2",
      "empresa": "Moonshot AI",
      "qualidade": 8.5,
      "custo_input_usd_1m": 0.15,
      "custo_output_usd_1m": 2.50,
      "velocidade_tps": 35,
      "contexto_k": 128,
      "destaque": "Contexto longo, baixo custo input"
    },
    {
      "id": "glm-4",
      "nome": "GLM-4",
      "empresa": "Zhipu AI",
      "qualidade": 8.0,
      "custo_input_usd_1m": 0.10,
      "custo_output_usd_1m": 0.10,
      "velocidade_tps": 45,
      "contexto_k": 128,
      "destaque": "Mais barato da categoria"
    }
  ],
  "eua": [
    {
      "id": "gpt-4o",
      "nome": "GPT-4o",
      "empresa": "OpenAI",
      "qualidade": 9.0,
      "custo_input_usd_1m": 2.50,
      "custo_output_usd_1m": 10.00,
      "velocidade_tps": 60,
      "contexto_k": 128,
      "destaque": "Mais popular do mercado"
    },
    {
      "id": "claude-sonnet",
      "nome": "Claude Sonnet 4.6",
      "empresa": "Anthropic",
      "qualidade": 9.1,
      "custo_input_usd_1m": 3.00,
      "custo_output_usd_1m": 15.00,
      "velocidade_tps": 50,
      "contexto_k": 200,
      "destaque": "Melhor em raciocínio complexo"
    },
    {
      "id": "gemini-pro",
      "nome": "Gemini 1.5 Pro",
      "empresa": "Google",
      "qualidade": 8.7,
      "custo_input_usd_1m": 1.25,
      "custo_output_usd_1m": 5.00,
      "velocidade_tps": 70,
      "contexto_k": 1000,
      "destaque": "Maior contexto disponível"
    },
    {
      "id": "llama3-70b",
      "nome": "Llama 3.3 70B",
      "empresa": "Meta (open)",
      "qualidade": 8.3,
      "custo_input_usd_1m": 0.59,
      "custo_output_usd_1m": 0.79,
      "velocidade_tps": 80,
      "contexto_k": 128,
      "destaque": "Melhor open source"
    }
  ]
}
```

### Agente de notícias (3h)

Usar `agentes/aiatolah_agente_coletor_ia.py` já existente.
Fontes prioritárias para coluna central:
- TechCrunch AI feed
- SCMP Tech (modelos chineses)
- Hugging Face blog RSS
- The Decoder (RSS)

Cada artigo: slug automático, frontmatter Astro, publicar em `src/pages/en/posts/`.

### Chaves disponíveis

Todas as chaves estão em `~/Downloads/Antigravity Google/aiatolah/.env.local`:
- `DEEPSEEK_API_KEY` — redação em inglês
- `KIMI_API_KEY` / `MOONSHOT_API_KEY` — contexto longo, revisão
- `QWEN_API_KEY` — fallback
- `BRAVE_API_KEY` — busca de pautas
- `GROQ_API_KEY` — transcrição (se necessário)

**GitHub token para push:** usar `GITHUB_TOKEN_AIATOLAH_KIMI` do cofre Beijing
(`/root/cerebro_trindade/cofre/env_cofre_backup`)

Alternativamente: o token clássico ativo funciona via:
`git clone https://<TOKEN>@github.com/migueldorosario1/aiatolah.git`

**VERCEL_TOKEN: não necessário** — push ao GitHub dispara deploy automático.

---

## Passos para o Kimi executar

1. **Ler** este fórum completo + `producao/aiatolah_engenharia.md`
2. **Clonar** o repo: `git clone https://{GITHUB_TOKEN}@github.com/migueldorosario1/aiatolah.git`
3. **Criar** `src/data/ranking.json` com o schema acima
4. **Criar** `src/pages/teste/index.astro` com layout 3 colunas
5. **Converter** preços para R$/M tokens (multiplica pelo campo `cotacao_usd_brl`)
6. **Adicionar** embed YouTube no topo direito (placeholder até Miguel escolher vídeo)
7. **Commit + push** para `main` → Vercel auto-deploya
8. **Reportar** URL do preview aqui neste fórum

---

## Critérios de aceitação

- [ ] `aiatola.vercel.app/teste` retorna HTTP 200
- [ ] 3 colunas visíveis em desktop
- [ ] Preços em R$/M tokens
- [ ] Pelo menos 1 artigo em inglês na coluna central
- [ ] Mobile: layout colapsado (1 coluna) funciona

---

## Notas editoriais

- Linha: pró-China, anti-imperialismo tecnológico
- Coluna China: destacar eficiência, inovação, soberania tecnológica
- Coluna EUA: factual, sem hostilidade, mas sem reverência
- Chatbot (Darius/Cyrus/Shirin): Fase 2 — não neste sprint

---

*Criado automaticamente por Claude Maestro via loop mural. Aguardando Kimi.*

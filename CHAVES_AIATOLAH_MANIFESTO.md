# Chaves do Aiatolah - manifesto seguro

Este arquivo registra quais chaves o Aiatolah precisa, onde elas devem ser buscadas e como instalar sem vazar segredo.

Regra central: valores reais de chave ficam em `.env.local`, variáveis do servidor, Vercel/GitHub Secrets ou cofre operacional. Não ficam em Git, ChatGPT, fórum ou canal.

## 1. Onde procurar as chaves reais

Fonte canônica no Cérebro:

- `Projeto Cafezinho Agentes/CEREBRO_NODE_COFRE_CHAVES.md`
- `Projeto Cafezinho Agentes/CEREBRO_NODE_OBSERVABILIDADE.md`

Arquivos operacionais locais já conhecidos pelo Cérebro:

- `Projeto Cafezinho Agentes/root/.env`
- `Projeto Cafezinho Agentes/root/.env.unificado`
- `Projeto Cafezinho Agentes/root/chaves_novas.env`
- `Projeto Cafezinho Agentes/root/chaves/alibaba_prometheus.env`

O último arquivo acima é o cofre específico do Prometheus Alibaba. Ele deve alimentar o `AIATOLAH_PROMETHEUS_PUSHGATEWAY`, mas o endpoint real não deve ser copiado para arquivos públicos.

## 2. Chaves mínimas para o Aiatolah nascer

LLMs:

- `DEEPSEEK_API_KEY` - redação, análise técnica e fallback forte.
- `QWEN_API_KEY` ou `DASHSCOPE_API_KEY` - revisão, limpeza, fallback e visão quando necessário.
- `KIMI_API_KEY` ou `MOONSHOT_API_KEY` - contexto longo, boletins e memória.
- `ZHIPU_API_KEY` - triagem, títulos, revisão rápida e fallback.

Busca e checagem:

- `BRAVE_API_KEY` - coleta de pauta e busca aberta.
- `PERPLEXITY_API_KEY` - fact-check caro e controlado. Usar só com regra explícita de custo.

Imagem e mídia:

- `FAL_API_KEY` - geração ou edição de imagem quando usada.
- `IDEOGRAM_API_KEY` - geração visual, se o fluxo editorial optar por ele.
- `FLICKR_API_KEY` - banco de imagem aberta, se usado.

Deploy:

- `GITHUB_TOKEN` ou chave SSH de deploy - publicar no repositório.
- `AIATOLAH_GITHUB_REPO` - repositório alvo.
- `VERCEL_TOKEN` - apenas se o fluxo usar API/CLI da Vercel. Se o deploy for por GitHub, pode não ser necessário.

Observabilidade:

- `AIATOLAH_PROMETHEUS_PUSHGATEWAY`
- `AIATOLAH_PROMETHEUS_JOB`
- `AIATOLAH_PROMETHEUS_INSTANCE`

## 3. Como instalar sem vazar

1. Copiar `.env.example` para `.env.local`.
2. Preencher `.env.local` com os valores reais, lendo do cofre.
3. Confirmar que `.env.local` está ignorado pelo Git.
4. Testar cada provider com chamada mínima antes de ativar cron ou publicador.
5. Registrar só fingerprints e resultado dos testes no fórum/canal.

## 4. O que vai para o ChatGPT

Pode ir:

- nomes das variáveis;
- arquitetura de uso;
- política de custo;
- exemplos com valores vazios;
- descrição dos papéis de cada provider.

Não pode ir:

- chaves reais;
- endpoint completo privado do Prometheus;
- tokens de GitHub/Vercel;
- chave SSH privada;
- arquivo `.env.local`.

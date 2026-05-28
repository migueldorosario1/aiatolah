# Leia primeiro — pacote canônico do Projeto ChatGPT Aiatolah

Esta pasta foi enxugada. Ela contém apenas os arquivos canônicos necessários para o ChatGPT ajudar Miguel a planejar e escrever o projeto **Aiatolah**.

## O que é o Aiatolah

O Aiatolah é um portal bilíngue de **inteligência artificial**.

Ele terá uma perspectiva de Sul Global, soberania tecnológica e crítica ao colonialismo digital, mas o assunto principal é IA: modelos, agentes, automação, custos, benchmarks, infraestrutura, observabilidade e impacto político/econômico/cultural da inteligência artificial.

## Ordem de upload

Suba os arquivos nesta ordem:

```text
00_LEIA_PRIMEIRO.md
01_ONBOARDING_CHATGPT_AIATOLAH_v2.md
02_CANONE_EDITORIAL_E_AGENTES.md
03_CANONE_PUBLICACAO_ASTRO_GITHUB_VERCEL.md
04_CANONE_METRICAS_E_OBSERVABILIDADE.md
05_RIOCARTA_content.config.ts
06_GSN_content.config.ts
07_RIOCARTA_vercel.json
08_DOMINIO_E_LABORATORIO_NO_AR.md
09_PROMETHEUS_E_CHAVES_DESDE_NASCENCA.md
10_CHAVES_AIATOLAH_MANIFESTO_SEGURO.md
11_PROMETHEUS_DESDE_NASCENCA_COMPLETO.md
12_ENV_EXAMPLE_AIATOLAH_SEM_SEGREDOS.txt
```

Os arquivos `10`, `11` e `12` foram copiados para esta pasta de propósito. Eles podem existir também em outros diretórios do projeto, mas esta pasta é o pacote fechado para upload no ChatGPT.

Não procurar arquivos fora desta pasta nesta primeira conversa com o ChatGPT.

## Prompt inicial

Depois de subir os arquivos `00` e `01`, pergunte:

```text
Leia os arquivos 00 e 01 e me diga o que você entendeu do projeto Aiatolah. Lembre que Aiatolah é um portal de inteligência artificial, não um portal de geopolítica.
```

Depois de subir todos os arquivos, pergunte:

```text
Com base nos arquivos do projeto, monte um plano enxuto para criar o Aiatolah em 6 frentes: site Astro/Vercel, conteúdo bilíngue, agentes automáticos, boletim técnico de IA, chaves/ambiente seguro e métricas Prometheus por post desde a primeira publicação.
```

## Segurança

Não subir chaves, `.env`, tokens, logs, bancos, imagens ou vídeos.

Este pacote não contém segredos. O arquivo `12_ENV_EXAMPLE_AIATOLAH_SEM_SEGREDOS.txt` é apenas um template com variáveis vazias.

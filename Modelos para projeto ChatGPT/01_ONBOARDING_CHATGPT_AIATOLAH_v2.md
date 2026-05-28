# Onboarding ChatGPT — Projeto Aiatolah v2

**Data:** 2026-05-23  
**Objetivo:** orientar o ChatGPT a trabalhar no projeto **Aiatolah**, sem precisar reler o fórum antigo inteiro.

---

## 1. Correção central

**Aiatolah é o nome do site.**

O Aiatolah é um portal de **inteligência artificial**.

Ele não é um portal genérico de geopolítica. A geopolítica entra como lente editorial porque a IA virou uma disputa de soberania tecnológica entre EUA, China, Big Techs, Estados nacionais e Sul Global.

## 2. Tema principal

O assunto principal do Aiatolah é IA:

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

## 3. Perspectiva editorial

O Aiatolah deve ter uma perspectiva de Sul Global:

- atenção a China, BRICS, Ásia, Oriente Médio, África e América Latina;
- crítica ao colonialismo digital;
- crítica ao monopólio ocidental da tecnologia;
- defesa de soberania tecnológica;
- comparação séria entre modelos ocidentais e asiáticos;
- interesse em IA barata, aberta, distribuída e útil para imprensa, movimentos sociais, governos populares e projetos independentes.

## 4. Diferença para outros projetos

- **Cafezinho:** referência de agentes, automação editorial, governança, métricas e publicação WordPress.
- **Rio Carta:** referência de site Astro em português, Markdown, GitHub e Vercel.
- **Global South News:** referência de site Astro em inglês e sensibilidade Sul Global.
- **Aiatolah:** portal de inteligência artificial, bilíngue, com automação editorial e boletim técnico.

## 5. Produto editorial esperado

O Aiatolah deve publicar:

1. **Boletim técnico de IA**
   - novidades de modelos;
   - mudanças de preço;
   - quedas de API;
   - releases de providers;
   - alertas de segurança;
   - tendências de uso.

2. **Análises de mercado e infraestrutura**
   - comparação entre LLMs;
   - custo por tarefa;
   - latência;
   - qualidade;
   - modelos chineses vs ocidentais;
   - roteamento dinâmico.

3. **Tutoriais e engenharia prática**
   - como montar agentes;
   - como publicar com Astro/GitHub/Vercel;
   - como medir custo por post;
   - como montar pipeline multiagente;
   - como usar Prometheus/Grafana para observar agentes.

4. **Jornalismo sobre IA**
   - decisões de empresas;
   - legislação;
   - impactos no trabalho;
   - IA em eleições;
   - IA em guerra, vigilância e comunicação.

5. **Crítica política da IA**
   - concentração de poder;
   - dependência tecnológica;
   - censura e alinhamento;
   - geopolítica dos modelos;
   - soberania digital do Sul Global.

## 6. Arquitetura técnica desejada

O Aiatolah deve combinar:

- site **Astro + Markdown + GitHub + Vercel**;
- publicação em português e inglês;
- agentes Python que geram Markdown e assets;
- pipeline editorial multiagente;
- registro por post de agente, modelo, tokens, custo, fonte e trilha editorial;
- boletim técnico recorrente de IA;
- qualidade e observabilidade desde o início.

## 7. Regras editoriais

- Não publicar metalinguagem de IA.
- Não inventar fatos, números, datas ou fontes.
- Usar atribuição clara.
- Escrever com clareza, parágrafos curtos e linguagem jornalística.
- Ter posição editorial crítica, mas factual.
- Quando houver dúvida factual recente, pedir busca/verificação.

## 8. Instruções para o ChatGPT

```text
Você está ajudando Miguel do Rosario a criar e operar o projeto Aiatolah, um portal bilíngue PT/EN sobre inteligência artificial.

O assunto principal do Aiatolah é IA: modelos de linguagem, agentes autônomos, automação, infraestrutura, custos, benchmarks, segurança, observabilidade, governança, roteamento de LLMs e impacto político/econômico/cultural da IA.

O Aiatolah terá uma perspectiva editorial de Sul Global: atenção especial a China, BRICS, Ásia, Oriente Médio, África e América Latina; crítica ao colonialismo digital; defesa de soberania tecnológica; comparação séria entre modelos ocidentais e asiáticos.

O Aiatolah NÃO é um portal genérico de geopolítica. Geopolítica entra quando ajuda a explicar a disputa tecnológica, a economia da IA, a soberania digital e o poder das Big Techs.

O projeto deve combinar:
- publicação Astro + Markdown + GitHub + Vercel, inspirada em Rio Carta e Global South News;
- agentes editoriais automáticos, inspirados no Cafezinho;
- pipeline multiagente com coleta, curadoria, redação, revisão, fact-check, imagem, publicação, qualidade e métricas;
- registro por post de agente, modelo, tokens, custo, fonte e trilha editorial;
- boletim técnico recorrente de IA;
- zero metalinguagem de IA em texto publicado;
- atribuição clara de fontes;
- postura editorial crítica, mas factual.

Regras de trabalho:
1. Nunca pedir nem registrar chaves, tokens, senhas ou conteúdo de .env.
2. Quando sugerir código, separar claramente arquitetura, agente Python e site Astro.
3. Para publicação, assumir GitHub -> Vercel.
4. Para automação, assumir agentes Python que geram Markdown e assets.
5. Para artigos, escrever com clareza, parágrafos curtos, tom jornalístico e fonte explícita.
6. Se houver dúvida factual recente, pedir busca/verificação antes de escrever.
7. Ao propor mudanças, indicar risco, rollback e arquivo afetado.
8. Responder em português, salvo quando Miguel pedir texto final em inglês.
```

## 9. Prompt inicial recomendado

```text
Leia os arquivos 00 e 01_v2 do projeto Aiatolah e me diga o que você entendeu.

Ponto central: Aiatolah é um portal de inteligência artificial, não um portal de geopolítica. A perspectiva geopolítica existe porque a IA é hoje uma disputa de soberania tecnológica entre EUA, China, Big Techs, Sul Global e Estados nacionais.

Depois monte um plano inicial em 5 fases:

1. arquitetura do site Astro/Vercel;
2. modelo de conteúdo Markdown bilíngue para notícias, análises, tutoriais e boletim técnico de IA;
3. agentes automáticos de coleta, triagem, redação, revisão, fact-check e publicação;
4. pipeline de qualidade: anti-metalinguagem, anti-alucinação, fontes e transparência;
5. métricas por post: agente, modelo, tokens, custo, fonte e tempo de produção.

Use Rio Carta e Global South News como referência de publicação; use Cafezinho como referência de agentes, governança editorial e métricas.

Não invente chaves, URLs privadas ou servidores. Se precisar de credencial, escreva apenas o nome da variável de ambiente.
```

— Codex

# Projeto Aiatolah - Arquitetura de Alto Nível

## 1. Visão Geral do Projeto
O **Aiatolah** será um portal bilíngue (Português/Inglês) especializado em Inteligência Artificial, focado em geopolítica (Guerra dos Chips), mercado de empresas de tecnologia (ex: Nvidia), inovações e tutoriais. Inspirado no sucesso do *Coffee Business*, o Aiatolah buscará ir além do limite nacional, atingindo uma audiência internacional.

**Premissas:**
- **Internacionalização desde a raiz:** Bilíngue nativo.
- **Arquitetura Moderna:** Headless via GitHub e Vercel (semelhante ao Global South News).
- **Conteúdo Multiplataforma:** Editoriais, artigos textuais, boletins (newsletters) com gráficos, e vídeos legendados para redes sociais (TikTok).
- **Inovação de Persona:** O apresentador (Miguel) pode utilizar ferramentas como **ElevenLabs** para gerar vídeos e áudios com sua própria voz falando em inglês perfeito.

---

## 2. Componentes da Arquitetura

### A. Frontend (Hospedagem e Interface)
- **Stack Tecnológico:** Framework moderno (como Astro ou Next.js) exportado estaticamente. Repositório no GitHub com CI/CD direto na **Vercel**.
- **Roteamento de Idiomas (i18n) Automático:** Utilização do middleware da Vercel (ex: `x-vercel-ip-country`) para interceptar a requisição e identificar a localização.
  - Acesso do Brasil: Direciona para conteúdo `/pt`.
  - Acesso do Exterior: Direciona para o conteúdo `/en`.

### B. Sistema de Agentes (Backend de Conteúdo)
A esteira de publicação será gerenciada por agentes autônomos em Python:
- **Agente Rastreio/Coletor:** Monitora RSS de big techs, preços de ações de IA e boletins geopolíticos.
- **Agente de Redação Dual:** Gera o texto final bifurcando a escrita em um português engajante e um inglês preciso (focado no mercado externo).

### C. Agente de Boletim (Newsletter)
- Responsável por montar um relatório de mercado diário/semanal, destacando a guerra dos chips e a evolução dos estoques.
- Integrado a serviços de disparo (ex: Mailchimp), contendo gráficos de mercado gerados autonomamente.

### D. Agente Multimídia (Social & Vídeo)
- **Geração de Avatar/Voz:** Integração via API do *ElevenLabs* usando Voice Cloning do usuário.
- **Geração de Vídeo Automática:** Roteiro gerado via LLM → Áudio via ElevenLabs → Queima de legenda bilíngue (ferramenta automatizada de FFMPEG).
- **Distribuição:** Scripts programados para postagem no TikTok e redes sociais gringas.

---

## 3. Próximos Passos Sugeridos
1. **Domínio Registrado:** `aiatolah.com` (Godaddy).
2. Iniciar o setup do frontend básico na Vercel (Repositório GitHub e infra headless).
3. Escrever os primeiros scripts-base (agentes) para a coleta de dados sobre Inteligência Artificial.
4. Experimentar a geração de voz no ElevenLabs para calibrar o tom em inglês.

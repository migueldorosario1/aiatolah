import os
import json
import sys
import feedparser
from datetime import datetime

# Conectar ao roteador da Trindade (Padrão Ouro Isolado)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'Projeto Cafezinho Agentes', 'root')))
try:
    from agente_roteador_llm import gerar_texto
except ImportError:
    print("[Erro] Não foi possível importar o roteador LLM. Rodando com mock.")
    def gerar_texto(sys_prompt, prompt, agente_nome="aiatolah", tema="ia", temperature=0.6):
        return f"[MOCK] Análise gerada pela IA sobre: {prompt[:50]}..."

# Feeds focados na Guerra dos Chips, IA e Mercado Asiático
FEEDS_MERCADO = {
    "Nvidia": "https://finance.yahoo.com/rss/headline?s=NVDA",
    "TSMC": "https://finance.yahoo.com/rss/headline?s=TSM",
    "Tech_AI": "https://techcrunch.com/category/artificial-intelligence/feed/",
    "China_Tech": "https://www.scmp.com/rss/318198/XML" # SCMP Tech
}

# Palavras-chave de alto valor para o diferencial do portal
KEYWORDS_CHINESAS = ["Kimi", "Moonshot", "Alibaba", "DeepSeek", "Qwen", "Baidu", "Ernie", "Tencent"]

def coletar_noticias():
    """Coleta as últimas notícias (Top 3) dos feeds RSS estratégicos."""
    noticias = []
    for categoria, url in FEEDS_MERCADO.items():
        print(f"[*] Coletando feed: {categoria}")
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]: # Busca mais fundo para achar as chinesas
            titulo = entry.title
            
            # Prioridade para notícias sobre modelos chineses (Diferencial do site)
            is_china_ai = any(kw.lower() in titulo.lower() for kw in KEYWORDS_CHINESAS)
            if categoria == "China_Tech" and not is_china_ai:
                continue # Filtra o feed chinês só para IA
                
            noticias.append({
                "categoria": categoria,
                "titulo": titulo,
                "link": entry.link,
                "data": getattr(entry, 'published', datetime.now().isoformat()),
                "foco_chines": is_china_ai
            })
    return noticias[:3] # Limita o total a 3 por rodada para não estourar custos

def simular_redacao_ia(noticia):
    """
    Chama a LLM para ler o título e gerar um texto rico focado no mercado e na tecnologia.
    Gera as duas versões: Inglês (principal) e Português.
    """
    slug = "".join([c if c.isalnum() else "-" for c in noticia['titulo'].lower()])[:50].strip('-')
    data_hoje = datetime.now().strftime("%Y-%m-%d")
    
    print(f"[LLM] Gerando análise para: {noticia['titulo']}")
    
    sys_prompt = "Você é um analista experiente focado no mercado global de Inteligência Artificial, semicondutores (Nvidia, TSMC) e modelos da China (DeepSeek, Kimi). Escreva uma análise breve e assertiva sobre o impacto do tema abaixo. Retorne APENAS o texto do artigo em formato Markdown limpo, sem tags markdown ao redor."
    prompt_en = f"Escreva em Inglês a análise sobre a seguinte notícia: {noticia['titulo']} (Categoria: {noticia['categoria']})."
    prompt_pt = f"Escreva em Português a análise sobre a seguinte notícia: {noticia['titulo']} (Categoria: {noticia['categoria']})."
    
    # Chama a LLM via Trindade
    texto_en = gerar_texto(sys_prompt, prompt_en, agente_nome="aiatolah_en", tema="tecnologia")
    texto_pt = gerar_texto(sys_prompt, prompt_pt, agente_nome="aiatolah_pt", tema="tecnologia")
    
    # Template Markdown para Astro (Inglês)
    conteudo_md_en = f"""---
title: "{noticia['titulo']} - Analysis"
date: {data_hoje}
category: "{noticia['categoria']}"
lang: "en"
source: "{noticia['link']}"
---

# {noticia['titulo']}

{texto_en}
"""

    # Template Markdown para Astro (Português)
    conteudo_md_pt = f"""---
title: "{noticia['titulo']} - Análise"
date: {data_hoje}
category: "{noticia['categoria']}"
lang: "pt-br"
source: "{noticia['link']}"
---

# {noticia['titulo']}

{texto_pt}
"""
    return slug, conteudo_md_en, conteudo_md_pt

def salvar_artigo_astro(slug, conteudo_en, conteudo_pt):
    """Salva os .md diretos no repositório Headless nas pastas de idioma."""
    pasta_base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'pages'))
    pasta_en = os.path.join(pasta_base, 'en', 'posts')
    pasta_pt = os.path.join(pasta_base, 'pt', 'posts')
    
    os.makedirs(pasta_en, exist_ok=True)
    os.makedirs(pasta_pt, exist_ok=True)
    
    caminho_en = os.path.join(pasta_en, f"{slug}.md")
    caminho_pt = os.path.join(pasta_pt, f"{slug}.md")
    
    with open(caminho_en, 'w', encoding='utf-8') as f:
        f.write(conteudo_en)
    with open(caminho_pt, 'w', encoding='utf-8') as f:
        f.write(conteudo_pt)
        
    print(f"[+] Artigos salvos em:\n   - {caminho_en}\n   - {caminho_pt}")

def main():
    print("=== Iniciando Aiatolah Agente Coletor ===")
    noticias = coletar_noticias()
    
    for noti in noticias:
        slug, md_en, md_pt = simular_redacao_ia(noti)
        salvar_artigo_astro(slug, md_en, md_pt)
        
    print("=== Coleta concluída. Próximo passo: git push para deploy na Vercel! ===")

if __name__ == "__main__":
    main()

import os
import json
import feedparser
from datetime import datetime

# Feeds focados na Guerra dos Chips, IA e Mercado
FEEDS_MERCADO = {
    "Nvidia": "https://finance.yahoo.com/rss/headline?s=NVDA",
    "TSMC": "https://finance.yahoo.com/rss/headline?s=TSM",
    "Tech_AI": "https://techcrunch.com/category/artificial-intelligence/feed/"
}

def coletar_noticias():
    """Coleta as últimas notícias (Top 3) dos feeds RSS estratégicos."""
    noticias = []
    for categoria, url in FEEDS_MERCADO.items():
        print(f"[*] Coletando feed: {categoria}")
        feed = feedparser.parse(url)
        for entry in feed.entries[:3]:
            noticias.append({
                "categoria": categoria,
                "titulo": entry.title,
                "link": entry.link,
                "data": getattr(entry, 'published', datetime.now().isoformat())
            })
    return noticias

def simular_redacao_ia(noticia):
    """
    Espaço reservado para a integração com a Trindade (Claude/Gemini).
    Aqui a LLM vai receber o link/título, ler o conteúdo, e escrever dois
    artigos profundos (um em PT e um em EN).
    """
    slug = "".join([c if c.isalnum() else "-" for c in noticia['titulo'].lower()])[:50]
    data_hoje = datetime.now().strftime("%Y-%m-%d")
    
    # Template Markdown (MDX/MD) que o Astro lê para gerar as páginas
    conteudo_md = f"""---
title: "{noticia['titulo']}"
date: {data_hoje}
category: "{noticia['categoria']}"
lang: "pt-br"
---

# {noticia['titulo']}

**Fonte:** {noticia['link']}

Este é um artigo gerado automaticamente pelos agentes Aiatolah focados no mercado de {noticia['categoria']}.
A integração final com a LLM (Trindade) injetará a análise geopolítica profunda aqui.
"""
    return slug, conteudo_md

def salvar_artigo_astro(slug, conteudo):
    """Salva o .md direto no repositório Headless."""
    pasta_destino = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'pages', 'posts'))
    os.makedirs(pasta_destino, exist_ok=True)
    
    caminho = os.path.join(pasta_destino, f"{slug}.md")
    with open(caminho, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    print(f"[+] Artigo salvo: src/pages/posts/{slug}.md")

def main():
    print("=== Iniciando Agente Coletor Aiatolah ===")
    noticias = coletar_noticias()
    
    for noti in noticias:
        slug, md = simular_redacao_ia(noti)
        salvar_artigo_astro(slug, md)
        
    print("=== Coleta concluída. Próximo passo: git push para deploy na Vercel! ===")

if __name__ == "__main__":
    main()

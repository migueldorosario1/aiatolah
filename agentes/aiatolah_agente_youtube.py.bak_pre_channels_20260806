import os
import json
import sys
import feedparser
import requests
from datetime import datetime

# Conectar ao roteador local isolado do Aiatolah
try:
    from roteador_local import gerar_texto
except ImportError:
    print("[Erro] Não foi possível importar o roteador local. Rodando com mock.")
    def gerar_texto(sys_prompt, prompt, agente_nome="aiatolah", tema="ia", temperature=0.6):
        return f"[MOCK] Análise de vídeo do YouTube sobre: {prompt[:50]}..."

# Canais estratégicos de IA e Ciência
CANAIS_AI = [
    {"nome": "Lex Fridman", "channel_id": "UC_QhL74eS6-s04aN_M190nQ"},
    {"nome": "Dwarkesh Patel", "channel_id": "UCxS9K_iT3Q4F03kM7Zc3c9A"},
    {"nome": "Andrej Karpathy", "channel_id": "UC7G0B3yO0hE5Z-w1-W1z1zA"},
    {"nome": "DeepLearning.AI", "channel_id": "UCcIXc5mJsHVYTZR1maL5l9w"},
    {"nome": "Google DeepMind", "channel_id": "UCxCO1M9qQeYF9-3k35W6v9A"},
    {"nome": "OpenAI", "channel_id": "UC78o7sX92w9o1sM01M42gQA"}
]

VISTOS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'agent_data', 'youtube_vistos.json'))

def carregar_vistos():
    if os.path.exists(VISTOS_PATH):
        try:
            with open(VISTOS_PATH, 'r', encoding='utf-8') as f:
                return set(json.load(f))
        except Exception:
            return set()
    return set()

def salvar_vistos(vistos):
    os.makedirs(os.path.dirname(VISTOS_PATH), exist_ok=True)
    with open(VISTOS_PATH, 'w', encoding='utf-8') as f:
        json.dump(list(vistos), f, ensure_ascii=False, indent=2)

def obter_transcricao(video_id):
    """Obtém a transcrição do vídeo usando a biblioteca youtube-transcript-api."""
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        api = YouTubeTranscriptApi()
        transcript = api.fetch(video_id, languages=['en', 'pt', 'es'])
        text = " ".join([snippet.text for snippet in transcript])
        return text
    except Exception as e:
        print(f"[YouTube] Falha ao obter transcrição para o vídeo {video_id}: {e}")
        return None

def gerar_e_salvar_imagem_destacada(slug, video_id, titulo_en):
    """Gera uma imagem de destaque por IA usando Fal.ai Flux Schnell."""
    import requests
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    hero_dir = os.path.join(base_dir, 'public', 'hero')
    os.makedirs(hero_dir, exist_ok=True)
    
    fal_key = os.environ.get("FAL_API_KEY")
    if not fal_key:
        print("[Visual] FAL_API_KEY não configurada. Usando thumbnail do YouTube.")
        return f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
        
    url = "https://fal.run/fal-ai/flux/schnell"
    headers = {
        "Authorization": f"Key {fal_key}",
        "Content-Type": "application/json"
    }
    
    prompt = f"Abstract editorial art for an AI science presentation about: {titulo_en}, premium corporate tech design, dark gradient, glowing neon cyan accents, 16:9, absolutely no text, no words, no letters."
    
    payload = {
        "prompt": prompt,
        "image_size": "landscape_16_9",
        "num_inference_steps": 4,
        "enable_safety_checker": True
    }
    
    try:
        print(f"[Visual] Gerando imagem para o vídeo {video_id}...")
        r = requests.post(url, json=payload, headers=headers, timeout=60)
        if r.status_code == 200:
            res = r.json()
            images = res.get("images", [])
            if images:
                img_url = images[0].get("url")
                print(f"[Visual] Baixando imagem de: {img_url}")
                img_data = requests.get(img_url).content
                local_path = os.path.join(hero_dir, f"youtube-{video_id}.jpg")
                with open(local_path, "wb") as f:
                    f.write(img_data)
                print(f"[Visual] Imagem salva localmente: /hero/youtube-{video_id}.jpg")
                return f"/hero/youtube-{video_id}.jpg"
        else:
            print(f"[Visual] Erro Fal.ai: HTTP {r.status_code} - {r.text}")
    except Exception as e:
        print(f"[Visual] Falha ao gerar/salvar imagem: {e}")
        
    # Fallback para o thumbnail oficial do YouTube caso falhe
    return f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"

def processar_video(video):
    """Processa o vídeo usando a LLM e gera os arquivos Markdown."""
    video_id = video['id']
    titulo_en = video['titulo']
    description = video['descricao']
    
    slug = f"youtube-{video_id}"
    data_hoje = datetime.now().strftime("%Y-%m-%d")
    
    # 1. Traduzir título
    try:
        sys_tradutor = (
            "Você é um tradutor de tecnologia profissional. Traduza o título a seguir do inglês para o português. "
            "Retorne APENAS a tradução limpa, sem aspas, tags ou explicações."
        )
        trad_pt = gerar_texto(sys_tradutor, f"Traduza: {titulo_en}", agente_nome="tradutor_titulo", tema="tecnologia")
        titulo_pt = trad_pt[0].strip('\"\'\n ') if isinstance(trad_pt, tuple) else trad_pt.strip('\"\'\n ')
        print(f"[YouTube] Título traduzido para PT: {titulo_pt}")
    except Exception as e:
        print(f"[Erro] Falha ao traduzir título: {e}")
        titulo_pt = titulo_en
        
    # 2. Obter transcrição e resumir
    transcricao = obter_transcricao(video_id)
    content_to_summarize = transcricao if transcricao else description
    
    sys_prompt = (
        "You are an engaging tech journalist writing for the Aiatolah portal. "
        "Your style must be simple, journalistic, and highly accessible, explaining tech clearly. "
        "Write an engaging, clear summary of the video content, framing the developments "
        "in a simple way and comparing them to global tech advances (especially Chinese breakthroughs like DeepSeek, Qwen, Kimi, and hardware/chips) "
        "and new scientific discoveries. Do NOT wrap the response in code blocks."
    )
    
    prompt_en = f"Generate a detailed technical summary in English for this AI video: '{titulo_en}'. Content:\n\n{content_to_summarize[:8000]}"
    prompt_pt = f"Gere um resumo técnico detalhado em Português para este vídeo de IA: '{titulo_pt}'. Conteúdo:\n\n{content_to_summarize[:8000]}"
    
    print(f"[YouTube] Gerando resumos para o vídeo {video_id}...")
    retorno_en = gerar_texto(sys_prompt, prompt_en, agente_nome="aiatolah_youtube_en", tema="tecnologia")
    retorno_pt = gerar_texto(sys_prompt, prompt_pt, agente_nome="aiatolah_youtube_pt", tema="tecnologia")
    
    texto_en = retorno_en[0] if isinstance(retorno_en, tuple) else retorno_en
    texto_pt = retorno_pt[0] if isinstance(retorno_pt, tuple) else retorno_pt
    
    # 3. Gerar imagem destacada
    hero_image = gerar_e_salvar_imagem_destacada(slug, video_id, titulo_en)
    
    def escape_yaml_single_quote(val):
        if not val:
            return "''"
        return f"'{str(val).replace(chr(39), chr(39)+chr(39))}'"

    titulo_en_yaml = escape_yaml_single_quote(f"{titulo_en} - Insights")
    titulo_pt_yaml = escape_yaml_single_quote(f"{titulo_pt} - Insights")
    link_youtube = f"https://www.youtube.com/watch?v={video_id}"
    
    embed_html = f"""<div class="youtube-embed" style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; margin: 25px 0; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 8px 32px rgba(0,0,0,0.5);">
  <iframe src="https://www.youtube.com/embed/{video_id}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border-radius: 12px;"></iframe>
</div>"""

    no_home_line = "noHome: true\n" if os.getenv("AIATOLAH_NO_HOME") == "1" else ""

    conteudo_md_en = f"""---
layout: ../../../layouts/PostLayout.astro
title: {titulo_en_yaml}
date: {data_hoje}
category: 'YouTube'
lang: "en"
source: '{link_youtube}'
heroImage: "{hero_image}"
{no_home_line}---

# {titulo_en}

{embed_html}

{texto_en}
"""

    conteudo_md_pt = f"""---
layout: ../../../layouts/PostLayout.astro
title: {titulo_pt_yaml}
date: {data_hoje}
category: 'YouTube'
lang: "pt-br"
source: '{link_youtube}'
heroImage: "{hero_image}"
{no_home_line}---

# {titulo_pt}

{embed_html}

{texto_pt}
"""
    return slug, conteudo_md_en, conteudo_md_pt, titulo_en, titulo_pt

def salvar_artigos(slug, conteudo_en, conteudo_pt):
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
        
    print(f"[YouTube] Artigos salvos em:\n   - {caminho_en}\n   - {caminho_pt}")

def executar_git_push():
    import subprocess
    repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    print(f"[*] Iniciando Git Push no repositório YouTube: {repo_dir}")
    try:
        status_res = subprocess.run(["git", "status", "--porcelain"], cwd=repo_dir, capture_output=True, text=True)
        if not status_res.stdout.strip():
            print("[*] Sem novos commits do YouTube.")
            return False
            
        subprocess.run(["git", "add", "."], cwd=repo_dir, check=True)
        data_hoje = datetime.now().strftime("%Y-%m-%d %H:%M")
        msg = f"[Aiatolah YouTube] Automático: Ingestão de vídeos de IA 🎥 ({data_hoje})"
        subprocess.run(["git", "commit", "-m", msg], cwd=repo_dir, check=True)
        subprocess.run(["git", "push", "origin", "main"], cwd=repo_dir, check=True)
        print("[+] Deploy YouTube executado com sucesso! 🚀")
        return True
    except Exception as e:
        print(f"[Erro] Falha ao executar Git Push do YouTube: {e}")
        return False

def disparar_ifttt_webhook(slug, titulo_pt, titulo_en):
    import requests
    ifttt_key = os.environ.get("IFTTT_KEY") or os.environ.get("IFTTT_WEBHOOK_KEY") or os.environ.get("IFTTT_MAKER_KEY")
    if not ifttt_key:
        return
        
    link_pt = f"https://aiatolah.com/pt/posts/{slug}"
    link_en = f"https://aiatolah.com/en/posts/{slug}"
    
    try:
        payload_pt = {"value1": f"🎥 {titulo_pt}", "value2": link_pt}
        for event in ["aiatolah_novo_post_pt", "aiatolah_novo_post"]:
            url = f"https://maker.ifttt.com/trigger/{event}/with/key/{ifttt_key}"
            requests.post(url, json=payload_pt, timeout=10)
    except Exception:
        pass
        
    try:
        payload_en = {"value1": f"🎥 {titulo_en}", "value2": link_en}
        url = f"https://maker.ifttt.com/trigger/aiatolah_novo_post_en/with/key/{ifttt_key}"
        requests.post(url, json=payload_en, timeout=10)
    except Exception:
        pass

def count_posts_today(pasta_en, prefix_youtube=False):
    today_str = datetime.now().strftime("%Y-%m-%d")
    count = 0
    if not os.path.exists(pasta_en):
        return 0
    for fname in os.listdir(pasta_en):
        if not fname.endswith(".md"):
            continue
        is_yt = fname.startswith("youtube-")
        if prefix_youtube != is_yt:
            continue
        fpath = os.path.join(pasta_en, fname)
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read()
                # Simple check for date in frontmatter
                if f"date: '{today_str}'" in content or f"date: {today_str}" in content:
                    count += 1
        except Exception:
            pass
    return count

def main():
    print("=== Iniciando Aiatolah Agente YouTube ===")
    
    pasta_base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'pages'))
    pasta_en = os.path.join(pasta_base, 'en', 'posts')
    
    published_today = count_posts_today(pasta_en, prefix_youtube=True)
    print(f"[*] Já publicados hoje: {published_today} vídeos do YouTube.")
    
    if published_today >= 1:
        print("[*] Limite de 1 vídeo do YouTube por dia já atingido. Nenhum novo vídeo será processado.")
        return
        
    vistos = carregar_vistos()
    
    primeira_vez = len(vistos) == 0
    videos_a_processar = []
    
    # 1. Coleta os feeds RSS de cada canal
    for canal in CANAIS_AI:
        feed_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={canal['channel_id']}"
        print(f"[*] Escaneando canal: {canal['nome']}")
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:3]: # Olha os 3 mais recentes
                video_id = entry.yt_videoid if hasattr(entry, 'yt_videoid') else entry.id.split(':')[-1]
                
                if video_id in vistos:
                    continue
                    
                titulo = entry.title
                descricao = entry.summary if hasattr(entry, 'summary') else ""
                
                videos_a_processar.append({
                    "id": video_id,
                    "titulo": titulo,
                    "descricao": descricao,
                    "canal": canal['nome']
                })
                
                # Se for a primeira vez rodando, inicializa o visto com todos os vídeos históricos
                # para evitar rodar dezenas de vídeos de uma vez.
                # Processamos apenas 1 mais recente como demonstração de que o agent funciona!
                if primeira_vez:
                    vistos.add(video_id)
        except Exception as e:
            print(f"[Erro] Falha ao coletar feed do canal {canal['nome']}: {e}")
            
    if primeira_vez and videos_a_processar:
        # Pega apenas o primeiro mais recente para processar
        demonstracao_video = videos_a_processar[0]
        vistos.remove(demonstracao_video["id"]) # remove para ser processado
        videos_a_processar = [demonstracao_video]
        print(f"[*] Primeira execução: Processando apenas o vídeo de demonstração '{demonstracao_video['titulo']}' para popular a base de vistos.")
        
    artigos_criados = []
    for vid in videos_a_processar:
        if published_today >= 1:
            print("[*] Limite de 1 vídeo do YouTube por dia atingido. Parando processamento.")
            break
            
        slug = f"youtube-{vid['id']}"
        caminho_en = os.path.join(pasta_en, f"{slug}.md")
        if os.path.exists(caminho_en):
            print(f"[*] Vídeo '{vid['titulo']}' já existe. Pulando.")
            vistos.add(vid['id'])
            continue
            
        try:
            slug, md_en, md_pt, titulo_en, titulo_pt = processar_video(vid)
            salvar_artigos(slug, md_en, md_pt)
            vistos.add(vid['id'])
            published_today += 1
            artigos_criados.append({
                "slug": slug,
                "titulo_en": titulo_en,
                "titulo_pt": titulo_pt
            })
        except Exception as e:
            print(f"[Erro] Falha ao processar vídeo {vid['id']}: {e}")
            
    if artigos_criados:
        salvar_vistos(vistos)
        print("=== Novos vídeos de IA publicados! Efetuando push... ===")
        if executar_git_push():
            for art in artigos_criados:
                disparar_ifttt_webhook(art['slug'], art['titulo_pt'], art['titulo_en'])
    else:
        print("[*] Sem novos vídeos nesta rodada.")

if __name__ == "__main__":
    main()


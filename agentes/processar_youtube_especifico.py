import os
import json
import sys
import requests
from datetime import datetime

# Importar o roteador local do Aiatolah
sys.path.append(os.path.dirname(__file__))
from roteador_local import gerar_texto

VIDEO_ID = "qPMhduk1qUs"
VIDEO_TITLE_EN = "The Hugging Face Breach, Moonshot AI Valued at $20B, and Living to 1,759 Years Old | EP #273"
VIDEO_AUTHOR = "Peter H. Diamandis"
LINK_YOUTUBE = f"https://www.youtube.com/watch?v={VIDEO_ID}"

def obter_transcricao(video_id):
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        api = YouTubeTranscriptApi()
        transcript = api.fetch(video_id, languages=['en', 'pt', 'es'])
        text = " ".join([snippet.text for snippet in transcript])
        return text
    except Exception as e:
        print(f"[YouTube] Erro ao obter transcrição: {e}")
        return None

def gerar_e_salvar_imagem_destacada(slug, video_id, titulo_en):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    hero_dir = os.path.join(base_dir, 'public', 'hero')
    os.makedirs(hero_dir, exist_ok=True)
    
    fal_key = os.environ.get("FAL_API_KEY")
    if fal_key:
        url = "https://fal.run/fal-ai/flux/schnell"
        headers = {
            "Authorization": f"Key {fal_key}",
            "Content-Type": "application/json"
        }
        prompt = (
            "Cybersecurity AI breach investigation, glowing cybernetic network, autonomous AI agents analyzing code logs, "
            "futuristic digital forensics, high quality editorial tech journalism image, dark background, neon cyan and amber accents, 16:9, no text, no words"
        )
        payload = {
            "prompt": prompt,
            "image_size": "landscape_16_9",
            "num_inference_steps": 4,
            "enable_safety_checker": True
        }
        try:
            print(f"[Visual] Gerando imagem via Fal.ai para o vídeo {video_id}...")
            r = requests.post(url, json=payload, headers=headers, timeout=60)
            if r.status_code == 200:
                res = r.json()
                images = res.get("images", [])
                if images:
                    img_url = images[0].get("url")
                    print(f"[Visual] Baixando imagem: {img_url}")
                    img_data = requests.get(img_url).content
                    local_path = os.path.join(hero_dir, f"youtube-{video_id}.jpg")
                    with open(local_path, "wb") as f:
                        f.write(img_data)
                    print(f"[Visual] Imagem salva: /hero/youtube-{video_id}.jpg")
                    return f"/hero/youtube-{video_id}.jpg"
            else:
                print(f"[Visual] Erro Fal.ai: HTTP {r.status_code} - {r.text}")
        except Exception as e:
            print(f"[Visual] Exceção na geração de imagem: {e}")
            
    print("[Visual] Fallback para thumbnail oficial do YouTube.")
    return f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"

def main():
    print(f"=== Processando vídeo {VIDEO_ID} para Aiatolah.com ===")
    
    transcricao = obter_transcricao(VIDEO_ID)
    if not transcricao:
        print("[Erro] Não foi possível obter a transcrição.")
        return

    print(f"[+] Transcrição obtida com sucesso! Tamanho: {len(transcricao)} caracteres.")
    
    # 1. Títulos
    titulo_pt = "A Invasão da Hugging Face por Agente Autônomo, Moonshot AI Avaliada em US$ 20 Bi e Longevidade Extrema"
    
    sys_prompt_pt = (
        "Você é um renomado jornalista de tecnologia e geopolítica de IA do portal Aiatolah (aiatolah.com). "
        "Escreva uma matéria editorial completa, altamente profissional, profunda e fascinante em Português do Brasil. "
        "A matéria deve analisar os três grandes pilares discutidos no episódio de Peter H. Diamandis:\n"
        "1. A Invasão Cibernética da Hugging Face realizada por um agente de IA autônomo, a recusa dos modelos da Anthropic e OpenAI em analisar o ataque por razões de alinhamento, e como a IA é o melhor 'Sherlock' para perícia de logs e endurecimento de infraestrutura cibernética anti-frágil.\n"
        "2. A ascensão avassaladora da Moonshot AI (avaliada em US$ 20 bilhões) e a força dos modelos chineses (DeepSeek, Kimi, Qwen) na guerra global de inteligência artificial e chips.\n"
        "3. Os avanços em longevidade humana, biotecnologia e medicina preventiva (viver até 1.759 anos).\n\n"
        "Estruture o texto com títulos h3 e h4, parágrafos fluidos, tom analítico e instigante. Não use blocos de código nem marque o resultado com ```markdown."
    )

    sys_prompt_en = (
        "You are a top-tier tech and AI geopolitics journalist writing for the Aiatolah portal (aiatolah.com). "
        "Write a comprehensive, highly professional, deep, and engaging editorial article in English. "
        "The article must analyze the three main pillars discussed in Peter H. Diamandis' podcast episode:\n"
        "1. The Autonomous AI Agent breach on Hugging Face, frontier model refusal (Anthropic/OpenAI) during forensic analysis, and how AI serves as the ultimate 'Sherlock' for log forensics and anti-fragile infrastructure hardening.\n"
        "2. Moonshot AI's historic $20B valuation and the rapid rise of Chinese AI ecosystem (Moonshot, DeepSeek, Qwen) in the global chip and model race.\n"
        "3. Breakthroughs in human longevity, biotech, and preventive health (living to 1,759 years old).\n\n"
        "Use engaging H3 and H4 section headers and fluent paragraphs. Do NOT wrap the response in markdown code blocks."
    )

    print("[+] Gerando artigo em Português...")
    prompt_pt = f"Título do vídeo: {VIDEO_TITLE_EN}\nTranscrição do vídeo (trecho principal):\n{transcricao[:18000]}"
    texto_pt = gerar_texto(sys_prompt_pt, prompt_pt, agente_nome="aiatolah_pt", tema="ia")

    print("[+] Gerando artigo em Inglês...")
    prompt_en = f"Video Title: {VIDEO_TITLE_EN}\nVideo Transcript (main section):\n{transcricao[:18000]}"
    texto_en = gerar_texto(sys_prompt_en, prompt_en, agente_nome="aiatolah_en", tema="ia")

    # Clean markdown backticks if present
    if texto_pt.startswith("```markdown"):
        texto_pt = texto_pt.split("\n", 1)[1]
    if texto_pt.endswith("```"):
        texto_pt = texto_pt.rsplit("```", 1)[0]

    if texto_en.startswith("```markdown"):
        texto_en = texto_en.split("\n", 1)[1]
    if texto_en.endswith("```"):
        texto_en = texto_en.rsplit("```", 1)[0]

    slug = f"youtube-{VIDEO_ID}"
    data_hoje = datetime.now().strftime("%Y-%m-%d")
    hero_image = gerar_e_salvar_imagem_destacada(slug, VIDEO_ID, VIDEO_TITLE_EN)

    embed_html = f"""<div class="youtube-embed" style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; margin: 25px 0; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 8px 32px rgba(0,0,0,0.5);">
  <iframe src="https://www.youtube.com/embed/{VIDEO_ID}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border-radius: 12px;"></iframe>
</div>"""

    conteudo_md_pt = f"""---
layout: ../../../layouts/PostLayout.astro
title: '{titulo_pt} - Insights'
date: {data_hoje}
category: 'YouTube'
lang: "pt-br"
source: '{LINK_YOUTUBE}'
heroImage: "{hero_image}"
---

# {titulo_pt}

{embed_html}

{texto_pt}
"""

    conteudo_md_en = f"""---
layout: ../../../layouts/PostLayout.astro
title: '{VIDEO_TITLE_EN} - Insights'
date: {data_hoje}
category: 'YouTube'
lang: "en"
source: '{LINK_YOUTUBE}'
heroImage: "{hero_image}"
---

# {VIDEO_TITLE_EN}

{embed_html}

{texto_en}
"""

    base_pages = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'pages'))
    path_pt = os.path.join(base_pages, 'pt', 'posts', f"{slug}.md")
    path_en = os.path.join(base_pages, 'en', 'posts', f"{slug}.md")

    os.makedirs(os.path.dirname(path_pt), exist_ok=True)
    os.makedirs(os.path.dirname(path_en), exist_ok=True)

    with open(path_pt, 'w', encoding='utf-8') as f:
        f.write(conteudo_md_pt)
    with open(path_en, 'w', encoding='utf-8') as f:
        f.write(conteudo_md_en)

    print(f"[+] Salvo em PT: {path_pt}")
    print(f"[+] Salvo em EN: {path_en}")

    # Atualizar vistos
    vistos_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'agent_data', 'youtube_vistos.json'))
    vistos = set()
    if os.path.exists(vistos_path):
        try:
            with open(vistos_path, 'r', encoding='utf-8') as f:
                vistos = set(json.load(f))
        except Exception:
            pass
    vistos.add(VIDEO_ID)
    os.makedirs(os.path.dirname(vistos_path), exist_ok=True)
    with open(vistos_path, 'w', encoding='utf-8') as f:
        json.dump(list(vistos), f, ensure_ascii=False, indent=2)

    print("[+] Adicionado ao youtube_vistos.json")

if __name__ == "__main__":
    main()

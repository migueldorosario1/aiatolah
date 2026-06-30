import os
import requests

# Load environment variables from .env.local if present
_env_local_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env.local'))
if os.path.exists(_env_local_path):
    with open(_env_local_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, val = line.split('=', 1)
                os.environ.setdefault(key.strip(), val.strip())

def gerar_texto(sys_prompt, prompt, agente_nome="aiatolah", tema="ia", temperature=0.6):
    """
    Isolated LLM router for the Aiatolah portal.
    Calls DeepSeek, falling back to OpenAI or Qwen if necessary.
    Uses Aiatolah's own local environment keys.
    """
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    base_url = "https://api.deepseek.com"
    model = "deepseek-chat"
    
    if not api_key:
        # Fallback to OpenAI
        api_key = os.environ.get("OPENAI_API_KEY")
        base_url = "https://api.openai.com/v1"
        model = "gpt-4o-mini"
        
    if not api_key:
        # Fallback to Qwen (Dashscope compatible mode)
        api_key = os.environ.get("QWEN_API_KEY") or os.environ.get("DASHSCOPE_API_KEY")
        base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
        model = "qwen-plus"

    if not api_key:
        print("[!] No API key found for Aiatolah local router. Using Mock.")
        return f"[Mock] Generated response for: {prompt[:100]}"

    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature
        }
        r = requests.post(f"{base_url}/chat/completions", json=payload, headers=headers, timeout=60)
        r.raise_for_status()
        res = r.json()
        return res["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"[Erro] Aiatolah Local Router failed for model {model}: {e}")
        # Try OpenAI emergency fallback
        if model == "deepseek-chat" and os.environ.get("OPENAI_API_KEY"):
            try:
                headers = {
                    "Authorization": f"Bearer {os.environ.get('OPENAI_API_KEY')}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": "gpt-4o-mini",
                    "messages": [
                        {"role": "system", "content": sys_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": temperature
                }
                r = requests.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers, timeout=60)
                r.raise_for_status()
                res = r.json()
                return res["choices"][0]["message"]["content"]
            except Exception as e2:
                print(f"[Erro] OpenAI fallback failed: {e2}")
        return "[Erro] Local router failed to generate text."

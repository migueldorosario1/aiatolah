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

# Importar o Agente Linguístico Chinês recém-implementado na Fase 0
try:
    from agente_linguistico_chines import AgenteLinguisticoChines, higienizar_texto_cjk
except ImportError:
    print("[Erro] Não foi possível importar o Agente Linguístico Chinês. Rodando sem CJK helper.")
    AgenteLinguisticoChines = None
    def higienizar_texto_cjk(t): return t

# Feeds estratégicos: Guerra dos Chips, IA e semicondutores
FEEDS_MERCADO = {
    "Nvidia": "https://finance.yahoo.com/rss/headline?s=NVDA",
    "TSMC": "https://finance.yahoo.com/rss/headline?s=TSM",
    "AMD": "https://finance.yahoo.com/rss/headline?s=AMD",
    "ASML": "https://finance.yahoo.com/rss/headline?s=ASML",
    "Broadcom": "https://finance.yahoo.com/rss/headline?s=AVGO",
    "Microsoft": "https://finance.yahoo.com/rss/headline?s=MSFT",
    "Google": "https://finance.yahoo.com/rss/headline?s=GOOG",
    "Meta": "https://finance.yahoo.com/rss/headline?s=META",
    "Tech_AI": "https://techcrunch.com/category/artificial-intelligence/feed/",
    "China_Tech": "https://www.scmp.com/rss/318198/XML" # SCMP Tech
}

# Palavras-chave estratégicas para atração de notícias chinesas
KEYWORDS_CHINESAS = ["Kimi", "Moonshot", "Alibaba", "DeepSeek", "Qwen", "Baidu", "Ernie", "Tencent", "Zhipu", "GLM"]

def _gerar_html_comparativo_raw(modelo_nome: str, metricas: dict) -> str:
    """
    Gera um card visual responsivo em HTML/CSS puro com tabelas e gráficos
    em barra horizontais comparativos de custo e tamanho de parâmetros.
    Se não houver métricas brutas extraídas, analisa o modelo_nome para gerar
    um card comparativo contextualizado e estatisticamente preciso.
    """
    param = metricas.get("parametros_bilhoes")
    preco = metricas.get("preço_usd_1m_tokens")
    litografia = metricas.get("litografia_nm")
    
    # 1. Fluxo Contextualizado 1: NVIDIA (Guerra de Semicondutores)
    if "nvidia" in modelo_nome.lower() or not (param or preco or litografia) and "nvidia" in modelo_nome.lower():
        return """
<div class="aiatolah-benchmark-card" style="background:#0b0f19; color:#fff; padding:20px; border-radius:10px; border:1px solid #1e293b; margin:25px 0; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif; box-shadow: 0 4px 20px rgba(0,0,0,0.4);">
  <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #1e293b; padding-bottom:12px; margin-bottom:15px;">
    <h4 style="color:#76b900; margin:0; font-size:16px; font-weight:bold; display:flex; align-items:center; gap:8px;">🟢 NVIDIA GPU Gen-to-Gen: Hopper vs Blackwell</h4>
    <span style="font-size:10px; color:#76b900; background:rgba(118,185,0,0.1); padding:2px 8px; border-radius:12px; border:1px solid rgba(118,185,0,0.3); font-weight:bold;">Soberania de Semicondutores</span>
  </div>
  
  <table style="width:100%; border-collapse:collapse; font-size:13px; margin-bottom:15px; text-align:left;">
    <thead>
      <tr style="color:#94a3b8; border-bottom:1px solid #1e293b;">
        <th style="padding:8px 0; font-weight:normal;">Métrica de Performance</th>
        <th style="padding:8px 0; font-weight:bold; color:#ccc;">Hopper H100</th>
        <th style="padding:8px 0; font-weight:bold; color:#76b900; text-align:right;">Blackwell B200</th>
      </tr>
    </thead>
    <tbody>
      <tr style="border-bottom:1px solid #0f172a;">
        <td style="padding:8px 0; color:#94a3b8;">Litografia (Processo)</td>
        <td style="padding:8px 0; color:#cbd5e1;">4nm TSMC (Custom)</td>
        <td style="padding:8px 0; color:#76b900; font-weight:bold; text-align:right;">4NP TSMC (Twin-die)</td>
      </tr>
      <tr style="border-bottom:1px solid #0f172a;">
        <td style="padding:8px 0; color:#94a3b8;">Transistores Totais</td>
        <td style="padding:8px 0; color:#cbd5e1;">80 Bilhões</td>
        <td style="padding:8px 0; color:#76b900; font-weight:bold; text-align:right;">208 Bilhões (2x104B)</td>
      </tr>
      <tr style="border-bottom:1px solid #0f172a;">
        <td style="padding:8px 0; color:#94a3b8;">Largura de Banda de Memória</td>
        <td style="padding:8px 0; color:#cbd5e1;">3.35 TB/s (HBM3)</td>
        <td style="padding:8px 0; color:#76b900; font-weight:bold; text-align:right;">8.0 TB/s (HBM3e)</td>
      </tr>
      <tr>
        <td style="padding:8px 0; color:#94a3b8;">FP8 Compute Power</td>
        <td style="padding:8px 0; color:#cbd5e1;">2,000 TFLOPS</td>
        <td style="padding:8px 0; color:#76b900; font-weight:bold; text-align:right;">9,000 TFLOPS</td>
      </tr>
    </tbody>
  </table>

  <div style="font-size:12px;">
    <div style="margin-bottom:12px;">
      <div style="display:flex; justify-content:space-between; margin-bottom:4px; color:#94a3b8;">
        <span>FP8 Compute (Blackwell vs Hopper):</span>
        <span style="font-weight:bold; color:#76b900;">4.5x superior</span>
      </div>
      <div style="background:#1e293b; height:8px; border-radius:4px; overflow:hidden;">
        <div style="background:#76b900; width:100%; height:100%; border-radius:4px;"></div>
      </div>
    </div>
    
    <div>
      <div style="display:flex; justify-content:space-between; margin-bottom:4px; color:#94a3b8;">
        <span>Consumo Energético / Eficiência (Watts por PetaFLOP):</span>
        <span style="font-weight:bold; color:#38bdf8;">25x mais eficiente</span>
      </div>
      <div style="background:#1e293b; height:8px; border-radius:4px; overflow:hidden;">
        <div style="background:#38bdf8; width:100%; height:100%; border-radius:4px;"></div>
      </div>
    </div>
  </div>
</div>
"""

    # 2. Fluxo Contextualizado 2: TSMC (Fábrica Mundial de Semicondutores)
    if "tsmc" in modelo_nome.lower() or not (param or preco or litografia) and "tsmc" in modelo_nome.lower():
        return """
<div class="aiatolah-benchmark-card" style="background:#0b0f19; color:#fff; padding:20px; border-radius:10px; border:1px solid #1e293b; margin:25px 0; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif; box-shadow: 0 4px 20px rgba(0,0,0,0.4);">
  <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #1e293b; padding-bottom:12px; margin-bottom:15px;">
    <h4 style="color:#ef4444; margin:0; font-size:16px; font-weight:bold; display:flex; align-items:center; gap:8px;">🇹🇼 TSMC Lithography Roadmap: N3E vs N2</h4>
    <span style="font-size:10px; color:#ef4444; background:rgba(239,68,68,0.1); padding:2px 8px; border-radius:12px; border:1px solid rgba(239,68,68,0.3); font-weight:bold;">Guerra das Fundições</span>
  </div>
  
  <table style="width:100%; border-collapse:collapse; font-size:13px; margin-bottom:15px; text-align:left;">
    <thead>
      <tr style="color:#94a3b8; border-bottom:1px solid #1e293b;">
        <th style="padding:8px 0; font-weight:normal;">Característica</th>
        <th style="padding:8px 0; font-weight:bold; color:#ccc;">TSMC N3E (3nm)</th>
        <th style="padding:8px 0; font-weight:bold; color:#ef4444; text-align:right;">TSMC N2 (2nm)</th>
      </tr>
    </thead>
    <tbody>
      <tr style="border-bottom:1px solid #0f172a;">
        <td style="padding:8px 0; color:#94a3b8;">Arquitetura do Transistor</td>
        <td style="padding:8px 0; color:#cbd5e1;">FinFET (3D Gate)</td>
        <td style="padding:8px 0; color:#ef4444; font-weight:bold; text-align:right;">Nanosheet (GAA / 4D Gate)</td>
      </tr>
      <tr style="border-bottom:1px solid #0f172a;">
        <td style="padding:8px 0; color:#94a3b8;">Densidade de Chips (vs N3E)</td>
        <td style="padding:8px 0; color:#cbd5e1;">1.0x (Referência)</td>
        <td style="padding:8px 0; color:#ef4444; font-weight:bold; text-align:right;">&gt; 1.15x Densidade</td>
      </tr>
      <tr style="border-bottom:1px solid #0f172a;">
        <td style="padding:8px 0; color:#94a3b8;">Ganho de Velocidade (mesma energia)</td>
        <td style="padding:8px 0; color:#cbd5e1;">Base 3nm</td>
        <td style="padding:8px 0; color:#ef4444; font-weight:bold; text-align:right;">+10% a +15% de Performance</td>
      </tr>
      <tr>
        <td style="padding:8px 0; color:#94a3b8;">Redução de Consumo (mesmo clock)</td>
        <td style="padding:8px 0; color:#cbd5e1;">Base 3nm</td>
        <td style="padding:8px 0; color:#ef4444; font-weight:bold; text-align:right;">-25% a -30% de Consumo</td>
      </tr>
    </tbody>
  </table>

  <div style="font-size:12px;">
    <div style="margin-bottom:12px;">
      <div style="display:flex; justify-content:space-between; margin-bottom:4px; color:#94a3b8;">
        <span>Eficiência Energética N2 (Redução de Dissipação):</span>
        <span style="font-weight:bold; color:#ef4444;">30% menor consumo</span>
      </div>
      <div style="background:#1e293b; height:8px; border-radius:4px; overflow:hidden;">
        <div style="background:#ef4444; width:100%; height:100%; border-radius:4px;"></div>
      </div>
    </div>
  </div>
</div>
"""

    # 3. Fluxo Contextualizado 3: Modelos Chineses (DeepSeek, Qwen, Kimi, GLM)
    any_chinese = any(kw.lower() in modelo_nome.lower() for kw in KEYWORDS_CHINESAS)
    if any_chinese or not (param or preco or litografia) and any_chinese:
        return """
<div class="aiatolah-benchmark-card" style="background:#0b0f19; color:#fff; padding:20px; border-radius:10px; border:1px solid #1e293b; margin:25px 0; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif; box-shadow: 0 4px 20px rgba(0,0,0,0.4);">
  <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #1e293b; padding-bottom:12px; margin-bottom:15px;">
    <h4 style="color:#38bdf8; margin:0; font-size:16px; font-weight:bold; display:flex; align-items:center; gap:8px;">🇨🇳 Frontier LLMs: DeepSeek V3 vs GPT-4o vs Qwen 2.5</h4>
    <span style="font-size:10px; color:#38bdf8; background:rgba(56,189,248,0.1); padding:2px 8px; border-radius:12px; border:1px solid rgba(56,189,248,0.3); font-weight:bold;">Soberania Tecnológica</span>
  </div>
  
  <table style="width:100%; border-collapse:collapse; font-size:13px; margin-bottom:15px; text-align:left;">
    <thead>
      <tr style="color:#94a3b8; border-bottom:1px solid #1e293b;">
        <th style="padding:8px 0; font-weight:normal;">Modelo de IA</th>
        <th style="padding:8px 0; font-weight:bold; color:#cbd5e1;">Origem</th>
        <th style="padding:8px 0; font-weight:bold; color:#22c55e; text-align:right;">Custo Input (1M tokens)</th>
        <th style="padding:8px 0; font-weight:bold; color:#38bdf8; text-align:right;">MMLU-Pro Rating</th>
      </tr>
    </thead>
    <tbody>
      <tr style="border-bottom:1px solid #0f172a;">
        <td style="padding:8px 0; font-weight:bold; color:#fff;">DeepSeek-V3</td>
        <td style="padding:8px 0; color:#cbd5e1;">🇨🇳 China (Open Source)</td>
        <td style="padding:8px 0; color:#22c55e; font-weight:bold; text-align:right;">$0.14</td>
        <td style="padding:8px 0; color:#38bdf8; font-weight:bold; text-align:right;">82.6%</td>
      </tr>
      <tr style="border-bottom:1px solid #0f172a;">
        <td style="padding:8px 0; font-weight:bold; color:#fff;">Qwen-2.5-72B-Inst</td>
        <td style="padding:8px 0; color:#cbd5e1;">🇨🇳 China (Open Source)</td>
        <td style="padding:8px 0; color:#22c55e; font-weight:bold; text-align:right;">$0.40</td>
        <td style="padding:8px 0; color:#38bdf8; font-weight:bold; text-align:right;">78.5%</td>
      </tr>
      <tr style="border-bottom:1px solid #0f172a;">
        <td style="padding:8px 0; font-weight:bold; color:#fff;">GPT-4o (Standard)</td>
        <td style="padding:8px 0; color:#cbd5e1;">🇺🇸 EUA (Proprietário)</td>
        <td style="padding:8px 0; color:#ef4444; font-weight:bold; text-align:right;">$5.00</td>
        <td style="padding:8px 0; color:#38bdf8; font-weight:bold; text-align:right;">77.2%</td>
      </tr>
    </tbody>
  </table>

  <div style="font-size:12px;">
    <div style="margin-bottom:12px;">
      <div style="display:flex; justify-content:space-between; margin-bottom:4px; color:#94a3b8;">
        <span>Eficiência Financeira (DeepSeek vs GPT-4o):</span>
        <span style="font-weight:bold; color:#22c55e;">97% mais barato</span>
      </div>
      <div style="background:#1e293b; height:8px; border-radius:4px; overflow:hidden;">
        <div style="background:#22c55e; width:97%; height:100%; border-radius:4px;"></div>
      </div>
    </div>
  </div>
</div>
"""

    # 4. Fluxo Padrão: Métricas Genéricas de IA (Se houver parâmetros, custos, etc.)
    if not param and not preco and not litografia:
        # Se mesmo assim não houver nada, exibe um gráfico geral de APIs de IA ativas
        return """
<div class="aiatolah-benchmark-card" style="background:#0b0f19; color:#fff; padding:20px; border-radius:10px; border:1px solid #1e293b; margin:25px 0; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif; box-shadow: 0 4px 20px rgba(0,0,0,0.4);">
  <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #1e293b; padding-bottom:12px; margin-bottom:15px;">
    <h4 style="color:#00d4ff; margin:0; font-size:16px; font-weight:bold; display:flex; align-items:center; gap:8px;">📊 Global South News: API Cost Benchmark</h4>
    <span style="font-size:10px; color:#00d4ff; background:rgba(0,212,255,0.1); padding:2px 8px; border-radius:12px; border:1px solid rgba(0,212,255,0.3); font-weight:bold;">Sul Global Tech</span>
  </div>
  
  <table style="width:100%; border-collapse:collapse; font-size:13px; margin-bottom:15px; text-align:left;">
    <thead>
      <tr style="color:#94a3b8; border-bottom:1px solid #1e293b;">
        <th style="padding:8px 0; font-weight:normal;">Provedor / API</th>
        <th style="padding:8px 0; font-weight:bold; color:#ccc;">Input / Output (1M tokens)</th>
        <th style="padding:8px 0; font-weight:bold; color:#00d4ff; text-align:right;">Qualidade</th>
      </tr>
    </thead>
    <tbody>
      <tr style="border-bottom:1px solid #0f172a;">
        <td style="padding:8px 0; font-weight:bold; color:#fff;">GLM-4 Flash (Zhipu)</td>
        <td style="padding:8px 0; color:#22c55e; font-weight:bold;">$0.07 / $0.07</td>
        <td style="padding:8px 0; color:#64748b; font-weight:bold; text-align:right;">Capaz (B)</td>
      </tr>
      <tr style="border-bottom:1px solid #0f172a;">
        <td style="padding:8px 0; font-weight:bold; color:#fff;">Llama-3-8B (Meta)</td>
        <td style="padding:8px 0; color:#22c55e; font-weight:bold;">$0.15 / $0.15</td>
        <td style="padding:8px 0; color:#64748b; font-weight:bold; text-align:right;">Capaz (B)</td>
      </tr>
      <tr style="border-bottom:1px solid #0f172a;">
        <td style="padding:8px 0; font-weight:bold; color:#fff;">DeepSeek-V3</td>
        <td style="padding:8px 0; color:#22c55e; font-weight:bold;">$0.14 / $0.28</td>
        <td style="padding:8px 0; color:#a855f7; font-weight:bold; text-align:right;">Excelente (A)</td>
      </tr>
      <tr>
        <td style="padding:8px 0; font-weight:bold; color:#fff;">GPT-4o (OpenAI)</td>
        <td style="padding:8px 0; color:#ef4444; font-weight:bold;">$5.00 / $15.00</td>
        <td style="padding:8px 0; color:#00d4ff; font-weight:bold; text-align:right;">Frontier (S)</td>
      </tr>
    </tbody>
  </table>

  <div style="font-size:12px;">
    <div>
      <div style="display:flex; justify-content:space-between; margin-bottom:4px; color:#94a3b8;">
        <span>Índice de Acessibilidade Financeira (GLM-4 / DeepSeek):</span>
        <span style="font-weight:bold; color:#00d4ff;">99% acessível</span>
      </div>
      <div style="background:#1e293b; height:8px; border-radius:4px; overflow:hidden;">
        <div style="background:#00d4ff; width:99%; height:100%; border-radius:4px;"></div>
      </div>
    </div>
  </div>
</div>
"""

    param_str = f"{param}B" if param else "N/A"
    preco_str = f"${preco:.4f}" if preco else "N/A"
    lito_str = f"{litografia}nm" if litografia else "N/A"
    
    # Define larguras de barra aproximadas para o gráfico base
    bar_width_param = min(100, int((param / 200) * 100)) if param else 0
    bar_width_preco = min(100, int((preco / 15) * 100)) if preco else 0
    
    html = f"""
<div class="aiatolah-benchmark-card" style="background:#111; color:#fff; padding:20px; border-radius:8px; border:1px solid #333; margin:25px 0; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,sans-serif;">
  <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #222; padding-bottom:10px; margin-bottom:15px;">
    <h4 style="color:#00d4ff; margin:0; font-size:16px; font-weight:bold;">📊 Ficha Técnica & Benchmark</h4>
    <span style="font-size:11px; color:#666; background:#1a1a1a; padding:3px 8px; border-radius:12px; border:1px solid #2a2a2a;">Aiatolah Engine</span>
  </div>
  
  <table style="width:100%; border-collapse:collapse; font-size:13px; margin-bottom:15px;">
    <thead>
      <tr style="color:#888; border-bottom:1px solid #222; text-align:left;">
        <th style="padding:6px 0;">Métrica</th>
        <th style="padding:6px 0; text-align:right;">Especificação</th>
      </tr>
    </thead>
    <tbody>
      <tr style="border-bottom:1px solid #1a1a1a;">
        <td style="padding:8px 0; color:#ccc;">Modelo Analisado</td>
        <td style="padding:8px 0; text-align:right; font-weight:bold; color:#fff;">{modelo_nome}</td>
      </tr>
      <tr style="border-bottom:1px solid #1a1a1a;">
        <td style="padding:8px 0; color:#ccc;">Litografia (Processo)</td>
        <td style="padding:8px 0; text-align:right; font-weight:bold; color:#e8b84b;">{lito_str}</td>
      </tr>
      <tr style="border-bottom:1px solid #1a1a1a;">
        <td style="padding:8px 0; color:#ccc;">Escala de Parâmetros</td>
        <td style="padding:8px 0; text-align:right; font-weight:bold; color:#00d4ff;">{param_str}</td>
      </tr>
      <tr>
        <td style="padding:8px 0; color:#ccc;">Preço por 1M Tokens (Input)</td>
        <td style="padding:8px 0; text-align:right; font-weight:bold; color:#a8ffb2;">{preco_str}</td>
      </tr>
    </tbody>
  </table>

  <div style="font-size:12px;">
    <div style="margin-bottom:10px;">
      <div style="display:flex; justify-content:space-between; margin-bottom:4px; color:#aaa;">
        <span>Escala de Tamanho (vs Frontier 200B):</span>
        <span style="font-weight:bold; color:#00d4ff;">{bar_width_param}%</span>
      </div>
      <div style="background:#222; height:6px; border-radius:3px; overflow:hidden;">
        <div style="background:#00d4ff; width:{bar_width_param}%; height:100%; border-radius:3px;"></div>
      </div>
    </div>
    
    <div>
      <div style="display:flex; justify-content:space-between; margin-bottom:4px; color:#aaa;">
        <span>Eficiência de Custo (vs Standard GPT-4o $15):</span>
        <span style="font-weight:bold; color:#a8ffb2;">{100 - bar_width_preco}% mais eficiente</span>
      </div>
      <div style="background:#222; height:6px; border-radius:3px; overflow:hidden;">
        <div style="background:#a8ffb2; width:{100 - bar_width_preco}%; height:100%; border-radius:3px;"></div>
      </div>
    </div>
  </div>
</div>
"""
    return html

def traduzir_html_para_en(html: str) -> str:
    replacements = {
        "Soberania de Semicondutores": "Semiconductor Sovereignty",
        "Métrica de Performance": "Performance Metric",
        "Litografia (Processo)": "Lithography (Process)",
        "Transistores Totais": "Total Transistors",
        "Largura de Banda de Memória": "Memory Bandwidth",
        "Consumo Energético / Eficiência (Watts por PetaFLOP):": "Energy Consumption / Efficiency (Watts per PetaFLOP):",
        "25x mais eficiente": "25x more efficient",
        "Guerra das Fundições": "Foundry Wars",
        "Característica": "Feature",
        "Arquitetura do Transistor": "Transistor Architecture",
        "Densidade de Chips (vs N3E)": "Chip Density (vs N3E)",
        "Ganho de Velocidade (mesma energia)": "Speed Gain (same power)",
        "+10% a +15% de Performance": "+10% to +15% Performance",
        "Redução de Consumo (mesmo clock)": "Power Reduction (same clock)",
        "-25% a -30% de Consumo": "-25% to -30% Power",
        "Eficiência Energética N2 (Redução de Dissipação):": "N2 Energy Efficiency (Power Dissipation Reduction):",
        "30% menor consumo": "30% lower power",
        "Soberania Tecnológica": "Technological Sovereignty",
        "Modelo de IA": "AI Model",
        "Origem": "Origin",
        "Custo Input (1M tokens)": "Input Cost (1M tokens)",
        "EUA (Proprietário)": "USA (Proprietary)",
        "Eficiência Financeira (DeepSeek vs GPT-4o):": "Financial Efficiency (DeepSeek vs GPT-4o):",
        "97% mais barato": "97% cheaper",
        "Sul Global Tech": "Global South Tech",
        "Provedor / API": "Provider / API",
        "Qualidade": "Quality",
        "Capaz (B)": "Capable (B)",
        "Excelente (A)": "Excellent (A)",
        "Índice de Acessibilidade Financeira (GLM-4 / DeepSeek):": "Financial Accessibility Index (GLM-4 / DeepSeek):",
        "99% acessível": "99% affordable",
        "Ficha Técnica & Benchmark": "Technical Specs & Benchmark",
        "Modelo Analisado": "Analyzed Model",
        "Escala de Parâmetros": "Parameter Scale",
        "Preço por 1M Tokens (Input)": "Price per 1M Tokens (Input)",
        "Escala de Tamanho (vs Frontier 200B):": "Size Scale (vs Frontier 200B):",
        "Eficiência de Custo (vs Standard GPT-4o $15):": "Cost Efficiency (vs Standard GPT-4o $15):",
        "mais eficiente": "more efficient"
    }
    for old, new in replacements.items():
        html = html.replace(old, new)
    return html

def gerar_html_comparativo(modelo_nome: str, metricas: dict, lang="pt-br") -> str:
    html_raw = _gerar_html_comparativo_raw(modelo_nome, metricas)
    # Remove any blank lines to prevent CommonMark parser from dropping out of HTML block mode
    html_clean = "\n".join([line for line in html_raw.splitlines() if line.strip()])
    if lang == "en":
        return traduzir_html_para_en(html_clean)
    return html_clean

def coletar_noticias():
    """Coleta as últimas notícias (Top 3) dos feeds RSS estratégicos."""
    noticias = []
    for categoria, url in FEEDS_MERCADO.items():
        print(f"[*] Coletando feed: {categoria}")
        feed = feedparser.parse(url)
        for entry in feed.entries[:8]: # Busca mais fundo para achar as chinesas
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
                "foco_chines": is_china_ai,
                "summary": getattr(entry, 'summary', '')
            })
            
    # Remove duplicados por título
    vistos = set()
    noticias_filtradas = []
    for n in noticias:
        if n["titulo"] not in vistos:
            vistos.add(n["titulo"])
            noticias_filtradas.append(n)
            
    return noticias_filtradas[:3] # Limita o total a 3 por rodada para controle de custo

def gerar_e_salvar_imagem_destacada(slug, titulo_en):
    """
    Gera uma imagem de destaque para o artigo usando Fal.ai Flux Schnell.
    Salva a imagem localmente em 'public/hero/{slug}.jpg'.
    Retorna o caminho público da imagem '/hero/{slug}.jpg' ou '/hero/default-aiatolah.jpg' em caso de erro.
    """
    import requests
    # Ensure public/hero exists
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    hero_dir = os.path.join(base_dir, 'public', 'hero')
    os.makedirs(hero_dir, exist_ok=True)
    
    # Load FAL key from environment
    fal_key = os.environ.get("FAL_API_KEY")
    if not fal_key:
        print("[Visual] FAL_API_KEY não configurado nas variáveis de ambiente. Pulando geração de imagem.")
        return "/hero/default-aiatolah.jpg"
        
    url = "https://fal.run/fal-ai/flux/schnell"
    headers = {
        "Authorization": f"Key {fal_key}",
        "Content-Type": "application/json"
    }
    
    # Generate prompt based on the article title
    # We want highly premium, aesthetic abstract/conceptual tech illustrations (no faces, no text)
    prompt = f"Abstract modern editorial concept illustration about {titulo_en}, sleek clean corporate tech style, glowing accents, dark background, 16:9, cinematic lighting, absolutely no text, no words, no letters, no recognizable faces."
    
    payload = {
        "prompt": prompt,
        "image_size": "landscape_16_9",
        "num_inference_steps": 4,
        "enable_safety_checker": True
    }
    
    try:
        print(f"[Visual] Gerando imagem para o artigo: {slug}...")
        r = requests.post(url, json=payload, headers=headers, timeout=60)
        if r.status_code == 200:
            res = r.json()
            images = res.get("images", [])
            if images:
                img_url = images[0].get("url")
                print(f"[Visual] Baixando imagem gerada de: {img_url}...")
                img_data = requests.get(img_url).content
                local_path = os.path.join(hero_dir, f"{slug}.jpg")
                with open(local_path, "wb") as f:
                    f.write(img_data)
                print(f"[Visual] Imagem salva com sucesso: {local_path}")
                return f"/hero/{slug}.jpg"
            else:
                print("[Visual] Resposta do Fal.ai sem imagem:", res)
        else:
            print(f"[Visual] Erro na API Fal.ai: HTTP {r.status_code} - {r.text}")
    except Exception as e:
        print(f"[Visual] Exceção ao gerar imagem destacada: {e}")
        
    return "/hero/default-aiatolah.jpg"

def processar_e_redigir_ia(noticia):
    """
    Chama a LLM para ler o título e gerar um texto rico focado no mercado e na tecnologia.
    Gera as duas versões: Inglês (principal) e Português.
    """
    slug = "".join([c if c.isalnum() else "-" for c in noticia['titulo'].lower()])[:50].strip('-')
    data_hoje = datetime.now().strftime("%Y-%m-%d")
    
    # 1. Pipeline de Tradução e Higienização Chinesa se houver foco
    metricas = {}
    if noticia["foco_chines"] and AgenteLinguisticoChines:
        agente_zh = AgenteLinguisticoChines()
        try:
            payload_zh = agente_zh.processar_artigo_zh(noticia["titulo"], noticia["summary"] or noticia["titulo"])
            titulo_pt = payload_zh["traduzido_pt"]["titulo"]
            titulo_en = payload_zh["traduzido_en"]["titulo"]
            metricas = payload_zh["metricas"]
            print(f"[Agente ZH] Título traduzido PT: {titulo_pt}")
        except Exception as e:
            print(f"[Erro] Falha ao traduzir usando Agente ZH: {e}")
            titulo_pt = higienizar_texto_cjk(noticia["titulo"])
            titulo_en = noticia["titulo"]
    else:
        titulo_en = noticia["titulo"]
        try:
            sys_tradutor = (
                "Você é um tradutor jornalístico profissional especializado em tecnologia e negócios. "
                "Traduza o título a seguir do inglês para o português do brasil de forma fluida, natural, "
                "sem jargões corporativos literais excessivos. Retorne APENAS a tradução limpa, sem aspas, "
                "sem explicações, sem markdown, sem tags, sem pontuação extra ao redor."
            )
            trad_pt = gerar_texto(sys_tradutor, f"Traduza: {titulo_en}", agente_nome="tradutor_titulo", tema="tecnologia")
            titulo_pt = trad_pt[0].strip('\"\'\n ') if isinstance(trad_pt, tuple) else trad_pt.strip('\"\'\n ')
            print(f"[Tradutor] Título traduzido para PT: {titulo_pt}")
        except Exception as e:
            print(f"[Erro] Falha ao traduzir título: {e}")
            titulo_pt = higienizar_texto_cjk(noticia["titulo"])
        
    print(f"[LLM] Gerando análise para: {titulo_en}")
    
    # 2. Geração dos Gráficos e Tabelas Visuais
    # Extrai o nome do modelo a ser exibido no card
    modelo_nome = noticia['categoria']
    for kw in KEYWORDS_CHINESAS + ["Nvidia", "TSMC", "Apple", "Google", "OpenAI", "Claude"]:
        if kw.lower() in titulo_en.lower() or kw.lower() in noticia['categoria'].lower():
            modelo_nome = kw
            break
            
    html_grafico_en = gerar_html_comparativo(modelo_nome, metricas, lang="en")
    html_grafico_pt = gerar_html_comparativo(modelo_nome, metricas, lang="pt-br")
    
    sys_prompt = (
        "Você é um analista experiente focado no mercado global de Inteligência Artificial, "
        "semicondutores (Nvidia, TSMC) e modelos da China (DeepSeek, Kimi, Qwen). Escreva uma análise "
        "breve e assertiva sobre o impacto do tema abaixo. Retorne APENAS o texto do artigo em formato "
        "Markdown limpo, sem blocos de código markdown ou tags adicionais ao redor do texto principal."
    )
    
    prompt_en = f"Write in English a professional editorial analysis about: {titulo_en} (Category: {noticia['categoria']})."
    prompt_pt = f"Escreva em Português uma análise editorial profissional sobre: {titulo_pt} (Category: {noticia['categoria']})."
    
    # Chama a LLM via Trindade (Roteador de LLM)
    retorno_en = gerar_texto(sys_prompt, prompt_en, agente_nome="aiatolah_en", tema="tecnologia")
    retorno_pt = gerar_texto(sys_prompt, prompt_pt, agente_nome="aiatolah_pt", tema="tecnologia")
    
    texto_en = retorno_en[0] if isinstance(retorno_en, tuple) else retorno_en
    texto_pt = retorno_pt[0] if isinstance(retorno_pt, tuple) else retorno_pt
    
    # Gera a imagem destacada por IA
    hero_image_path = gerar_e_salvar_imagem_destacada(slug, titulo_en)
    
    # 3. Geração dos templates Markdown enriquecidos com os micro-charts
    def escape_yaml_single_quote(val):
        if not val:
            return "''"
        return f"'{str(val).replace(chr(39), chr(39)+chr(39))}'"

    titulo_en_yaml = escape_yaml_single_quote(f"{titulo_en} - Analysis")
    titulo_pt_yaml = escape_yaml_single_quote(f"{titulo_pt} - Análise")
    categoria_yaml = escape_yaml_single_quote(noticia['categoria'])
    link_yaml = escape_yaml_single_quote(noticia['link'])

    no_home_line = "noHome: true\n" if os.getenv("AIATOLAH_NO_HOME") == "1" else ""

    conteudo_md_en = f"""---
layout: ../../../layouts/PostLayout.astro
title: {titulo_en_yaml}
date: {data_hoje}
category: {categoria_yaml}
lang: "en"
source: {link_yaml}
heroImage: "{hero_image_path}"
{no_home_line}---

# {titulo_en}

{html_grafico_en}

{texto_en}
"""

    conteudo_md_pt = f"""---
layout: ../../../layouts/PostLayout.astro
title: {titulo_pt_yaml}
date: {data_hoje}
category: {categoria_yaml}
lang: "pt-br"
source: {link_yaml}
heroImage: "{hero_image_path}"
{no_home_line}---

# {titulo_pt}

{html_grafico_pt}

{texto_pt}
"""
    return slug, conteudo_md_en, conteudo_md_pt, titulo_en, titulo_pt

def salvar_artigo_astro(slug, conteudo_en, conteudo_pt):
    """Salva os .md diretos no repositório Headless nas pastas de idioma correspondentes."""
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

def executar_git_push():
    """
    Executa git add, git commit e git push para persistir e deployar
    no repositório headless do portal Aiatolah na Vercel.
    Retorna True se houver novos Commits/Push, False caso contrário.
    """
    import subprocess
    repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    print(f"[*] Iniciando auto-dispatch Git no repositório: {repo_dir}")
    try:
        # Check status first to see if there is something to commit
        status_res = subprocess.run(["git", "status", "--porcelain"], cwd=repo_dir, capture_output=True, text=True)
        if not status_res.stdout.strip():
            print("[*] Nenhum artigo novo ou alterado encontrado para deploy.")
            return False
            
        # 1. git add .
        subprocess.run(["git", "add", "."], cwd=repo_dir, check=True)
        
        # 2. git commit -m "..."
        data_hoje = datetime.now().strftime("%Y-%m-%d %H:%M")
        msg = f"[Aiatolah Engine] Automático: Ingestão de Notícias + Micro-charts 📊 ({data_hoje})"
        subprocess.run(["git", "commit", "-m", msg], cwd=repo_dir, check=True)
        
        # 3. git push origin main
        print("[*] Enviando posts ao GitHub para publicação via Vercel...")
        subprocess.run(["git", "push", "origin", "main"], cwd=repo_dir, check=True)
        print("[+] Deploy executado e publicado com sucesso total! 🚀")
        return True
    except Exception as e:
        print(f"[Erro] Falha ao executar Git Push automático: {e}")
        return False

def disparar_ifttt_webhook(slug, titulo_pt, titulo_en):
    """
    Dispara os webhooks do IFTTT para notificar sobre novos artigos em PT e EN.
    O IFTTT Maker Key é obtido da variável de ambiente IFTTT_KEY, IFTTT_WEBHOOK_KEY ou IFTTT_MAKER_KEY.
    """
    import requests
    ifttt_key = os.environ.get("IFTTT_KEY") or os.environ.get("IFTTT_WEBHOOK_KEY") or os.environ.get("IFTTT_MAKER_KEY")
    if not ifttt_key:
        print("[!] IFTTT Maker Key não encontrada nas variáveis de ambiente. Pulando webhook.")
        return
        
    link_pt = f"https://aiatolah.com/pt/posts/{slug}"
    link_en = f"https://aiatolah.com/en/posts/{slug}"
    
    # 1. Dispara o Webhook em Português
    try:
        payload_pt = {"value1": titulo_pt, "value2": link_pt}
        # Dispara tanto o evento específico quanto o genérico para máxima compatibilidade
        for event in ["aiatolah_novo_post_pt", "aiatolah_novo_post"]:
            url = f"https://maker.ifttt.com/trigger/{event}/with/key/{ifttt_key}"
            r = requests.post(url, json=payload_pt, timeout=10)
            print(f"[IFTTT] Webhook '{event}' disparado para PT: {r.status_code}")
    except Exception as e:
        print(f"[Erro] Falha ao disparar Webhook IFTTT PT: {e}")
        
    # 2. Dispara o Webhook em Inglês
    try:
        payload_en = {"value1": titulo_en, "value2": link_en}
        url = f"https://maker.ifttt.com/trigger/aiatolah_novo_post_en/with/key/{ifttt_key}"
        r = requests.post(url, json=payload_en, timeout=10)
        print(f"[IFTTT] Webhook 'aiatolah_novo_post_en' disparado para EN: {r.status_code}")
    except Exception as e:
        print(f"[Erro] Falha ao disparar Webhook IFTTT EN: {e}")

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
    print("=== Iniciando Aiatolah Agente Coletor v1.2 (Phase 1 + Social Webhook) ===")
    
    pasta_base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'pages'))
    pasta_en = os.path.join(pasta_base, 'en', 'posts')
    
    published_today = count_posts_today(pasta_en, prefix_youtube=False)
    print(f"[*] Já publicados hoje: {published_today} notícias normais.")
    
    if published_today >= 2:
        print("[*] Limite de 2 notícias por dia já atingido. Nenhuma nova notícia será coletada.")
        return
        
    noticias = coletar_noticias()
    
    artigos_processados = []
    for noti in noticias:
        if published_today >= 2:
            print("[*] Limite de 2 notícias por dia atingido. Parando processamento.")
            break
            
        slug = "".join([c if c.isalnum() else "-" for c in noti['titulo'].lower()])[:50].strip('-')
        caminho_en = os.path.join(pasta_en, f"{slug}.md")
        if os.path.exists(caminho_en):
            print(f"[*] Notícia '{noti['titulo']}' já existe ({slug}.md). Pulando.")
            continue
            
        slug, md_en, md_pt, titulo_en, titulo_pt = processar_e_redigir_ia(noti)
        salvar_artigo_astro(slug, md_en, md_pt)
        published_today += 1
        artigos_processados.append({
            "slug": slug,
            "titulo_en": titulo_en,
            "titulo_pt": titulo_pt
        })
        
    if artigos_processados:
        print("=== Coleta concluída. Iniciando deploy automático na Vercel... ===")
        if executar_git_push():
            print("=== Deploy de sucesso. Disparando notificações IFTTT... ===")
            for art in artigos_processados:
                disparar_ifttt_webhook(art["slug"], art["titulo_pt"], art["titulo_en"])
        else:
            print("[*] Sem novos commits. Webhooks do IFTTT ignorados.")
    else:
        print("[*] Nenhuma nova notícia processada nesta rodada.")

if __name__ == "__main__":
    main()


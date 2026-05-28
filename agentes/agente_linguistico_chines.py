#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agente Linguístico Chinês — Preprocessador de dados e fontes técnicas CJK.
Focado em extrair, traduzir e normalizar informações de IAs, chips e semicondutores
do ecossistema asiático (DeepSeek, Qwen, Zhipu GLM, Baidu Ernie, etc.)
em conformidade com o Blueprint Aiatolah v1.0.
"""

import os
import re
import sys
import json
from datetime import datetime

# Conectar ao roteador da Trindade (Padrão Ouro Isolado)
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'Projeto Cafezinho Agentes', 'root'))
sys.path.append(ROOT_DIR)

try:
    from agente_roteador_llm import gerar_texto
except ImportError:
    # Fallback se executado fora do ambiente de chaves unificadas
    def gerar_texto(sys_prompt, prompt, agente_nome="aiatolah", tema="ia", temperature=0.6):
        return f"[MOCK TRADUÇÃO] Texto processado sem roteador ativo: {prompt[:50]}..."


# Dicionário de normalização de termos técnicos chineses de IA
DICIONARIO_TERMOS_IA = {
    "智谱": "Zhipu AI (GLM)",
    "阿里": "Alibaba Cloud (Qwen)",
    "百度": "Baidu (Ernie)",
    "腾讯": "Tencent (Hunyuan)",
    "字节跳动": "ByteDance (Doubao)",
    "深度求索": "DeepSeek",
    "芯片": "chips / semicondutores",
    "半导体": "semicondutores",
    "光刻机": "máquina de litografia",
    "算力": "poder computacional / hashing",
    "大模型": "LLM (Large Language Model)",
    "开源": "Open Source",
    "参数": "parâmetros",
    "千亿": "100 bilhões",
    "万亿": "1 trilhão",
}


def higienizar_texto_cjk(texto: str) -> str:
    """
    Substitui termos chineses de IA conhecidos por suas nomenclaturas
    padronizadas ocidentais para facilitar a análise e triagem.
    """
    if not texto:
        return ""
    
    texto_limpo = texto
    for termo_zh, padrao_en in DICIONARIO_TERMOS_IA.items():
        texto_limpo = texto_limpo.replace(termo_zh, f" {padrao_en} ")
    
    # Remove múltiplos espaços em branco gerados pela substituição
    texto_limpo = re.sub(r'\s+', ' ', texto_limpo).strip()
    return texto_limpo


def converter_cambio(valor_rmb: float, taxa_usd_cny: float = 7.24) -> float:
    """
    Converte valores financeiros (preços de API, rounds de investimento)
    de Renminbi (Yuan) para Dólar Americano (USD).
    """
    if valor_rmb <= 0:
        return 0.0
    return round(valor_rmb / taxa_usd_cny, 4)


def extrair_dados_tecnicos(texto: str) -> dict:
    """
    Realiza regexes simples no texto higienizado para extrair
    parâmetros numéricos, litografia (nm) e custos aproximados em RMB.
    """
    dados = {
        "litografia_nm": None,
        "parametros_bilhoes": None,
        "preço_rmb_1m_tokens": None,
    }
    
    # Encontra litografia (ex: 7nm, 5nm, 3nm)
    nm_match = re.search(r'(\d+)\s*(?:nm|纳米)', texto, re.IGNORECASE)
    if nm_match:
        dados["litografia_nm"] = int(nm_match.group(1))
        
    # Encontra parâmetros em bilhões (ex: 72B, 720亿)
    param_match = re.search(r'(\d+)\s*(?:b|亿参数)', texto, re.IGNORECASE)
    if param_match:
        dados["parametros_bilhoes"] = int(param_match.group(1))
        
    # Encontra custo por 1M tokens em RMB (ex: 0.1元/万 tokens ou similar)
    preco_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:元|rmb)\s*/\s*(?:百万|1m|100万)', texto, re.IGNORECASE)
    if preco_match:
        dados["preço_rmb_1m_tokens"] = float(preco_match.group(1))
        
    return dados


def traduzir_tecnico_zh(texto_chines: str, idioma_destino: str = "pt") -> str:
    """
    Chama a LLM via Trindade com um prompt ultra-especializado em tradução técnica CJK,
    garantindo que nomes de modelos, custos, métricas e benchmarks não sejam alucinados ou perdidos.
    """
    if not texto_chines or len(texto_chines) < 10:
        return ""
        
    sys_prompt = (
        "Você é um Tradutor Técnico especializado em Semicondutores, Inteligência Artificial "
        "e Geopolítica Computacional Chinesa. Traduza o texto original de forma exata, "
        "preservando rigorosamente todos os nomes de modelos, siglas, dados quantitativos (nm, TFLOPs, "
        "preços em Yuan/RMB/USD, contagem de parâmetros) e datas. "
        "Não embeleze ou suavize o tom jornalístico/científico original. "
        "Retorne APENAS a tradução limpa."
    )
    
    prompt = (
        f"Traduza o seguinte texto em Chinês Técnico para o idioma '{idioma_destino}':\n\n"
        f"{texto_chines}"
    )
    
    # Executa com temperatura baixa para máxima precisão literal
    retorno = gerar_texto(
        sys_prompt=sys_prompt,
        prompt=prompt,
        agente_nome="aiatolah_linguistico_chines",
        tema="tecnologia",
        temperature=0.2
    )
    
    # Unpack se for uma tupla (texto, modelo)
    texto_traduzido = retorno[0] if isinstance(retorno, tuple) else retorno
    
    return texto_traduzido.strip() if texto_traduzido else ""


class AgenteLinguisticoChines:
    """Classe controladora para processamento de feeds de inteligência asiática."""
    
    def __init__(self, taxa_cambio_cny: float = 7.24):
        self.taxa_cambio_cny = taxa_cambio_cny
        
    def processar_artigo_zh(self, titulo_zh: str, texto_zh: str) -> dict:
        """Processa um artigo técnico em chinês bruto e gera o payload estruturado."""
        print(f"[*] Agente ZH processando: {titulo_zh[:40]}...")
        
        # 1. Higienização preliminar de nomes
        titulo_higienizado = higienizar_texto_cjk(titulo_zh)
        texto_higienizado = higienizar_texto_cjk(texto_zh)
        
        # 2. Extração determinística de parâmetros e custos
        dados_metrica = extrair_dados_tecnicos(texto_higienizado)
        if dados_metrica["preço_rmb_1m_tokens"] is not None:
            dados_metrica["preço_usd_1m_tokens"] = converter_cambio(
                dados_metrica["preço_rmb_1m_tokens"], 
                self.taxa_cambio_cny
            )
        else:
            dados_metrica["preço_usd_1m_tokens"] = None
            
        # 3. Tradução técnica fiel das metadados e corpo
        titulo_traduzido_pt = traduzir_tecnico_zh(titulo_zh, "pt")
        titulo_traduzido_en = traduzir_tecnico_zh(titulo_zh, "en")
        texto_traduzido_pt = traduzir_tecnico_zh(texto_zh, "pt")
        texto_traduzido_en = traduzir_tecnico_zh(texto_zh, "en")
        
        return {
            "zh_original": {
                "titulo": titulo_zh,
                "texto": texto_zh
            },
            "higienizado": {
                "titulo": titulo_higienizado,
                "texto": texto_higienizado
            },
            "metricas": dados_metrica,
            "traduzido_pt": {
                "titulo": titulo_traduzido_pt,
                "texto": texto_traduzido_pt
            },
            "traduzido_en": {
                "titulo": titulo_traduzido_en,
                "texto": texto_traduzido_en
            },
            "data_processamento": datetime.now().isoformat()
        }


if __name__ == "__main__":
    # Smoke test simples
    teste_zh = "阿里推出了开源大模型 Qwen-2.5-72B，价格低至 0.2元/百万 tokens，采用先进芯片算力算力系统。"
    print("--- TESTE DE HIGIENIZAÇÃO ---")
    print(higienizar_texto_cjk(teste_zh))
    
    print("\n--- TESTE DE EXTRAÇÃO DADOS ---")
    print(extrair_dados_tecnicos(teste_zh))
    
    print("\n--- TESTE DE CAMBIO ---")
    print(f"0.2 RMB = ${converter_cambio(0.2)} USD")
    
    print("\n--- AGENTE INTEGRADO ---")
    agente = AgenteLinguisticoChines()
    resultado = agente.processar_artigo_zh(
        "阿里推出了 Qwen-2.5-72B 开源模型",
        teste_zh
    )
    print(json.dumps(resultado, indent=2, ensure_ascii=False))

import os
import requests
import json
from enviar_planilha import enviar_para_webhook

# Tenta carregar variáveis de ambiente
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

GROQ_KEY = os.getenv("GROQ_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

def pesquisar_contexto_gemini(tema, perfil_id):
    """
    Usa o Gemini Flash para gerar uma análise estratégica profunda.
    """
    if not GEMINI_KEY:
        print("⚠️ GEMINI_API_KEY não encontrada. Usando Groq como fallback...")
        return pesquisar_contexto_groq(tema, perfil_id)

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    
    headers = {"Content-Type": "application/json"}
    
    prompt = f"""
    Aja como o Agente Pesquisador Sênior do sistema Arquiteto Vivo.
    O Agente Radar detectou este tema em alta: "{tema}"
    Perfil Alvo: {perfil_id}

    Sua missão é entregar um Dossiê de Inteligência:
    1. CONTEXTO ESTATÍSTICO: Por que esse tema é relevante hoje? Traga dados ou tendências.
    2. 3 ÂNGULOS DE ATAQUE:
       - Ângulo 1: Educativo e Profundo.
       - Ângulo 2: Controverso/Polêmico.
       - Ângulo 3: Rápido e Viral (curiosidade).
    3. ANÁLISE DE CONCORRÊNCIA: O que os grandes canais estão ignorando sobre esse tema?

    Responda em texto limpo, sem markdown complexo, focado em estratégia pura.
    """

    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    try:
        res = requests.post(url, json=payload, headers=headers, timeout=20)
        res_json = res.json()
        if 'candidates' in res_json:
            return res_json['candidates'][0]['content']['parts'][0]['text']
        else:
            print(f"❌ Erro na API Gemini: {res_json}")
            return pesquisar_contexto_groq(tema, perfil_id)
    except Exception as e:
        print(f"⚠️ Falha no Gemini: {e}. Usando Groq...")
        return pesquisar_contexto_groq(tema, perfil_id)

def pesquisar_contexto_groq(tema, perfil_id):
    """Fallback usando Groq/Llama-3"""
    if not GROQ_KEY:
        return "⚠️ Erro: Nenhuma API de inteligência disponível."

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": f"Analise o tema estratégico: {tema} para o perfil {perfil_id}"}],
        "temperature": 0.7
    }
    
    try:
        res = requests.post(url, json=payload, headers=headers)
        return res.json()['choices'][0]['message']['content']
    except:
        return "Falha total na análise estratégica."

def aprofundar_ideia(tema, perfil_id, enviar=True):
    """Executa o fluxo de pesquisa e salva na planilha se enviar=True"""
    print(f"🔎 [PESQUISADOR] Analisando: {tema} com Gemini Flash...")
    contexto = pesquisar_contexto_gemini(tema, perfil_id)
    
    if enviar:
        payload = {
            "tema": tema,
            "perfil": perfil_id,
            "contexto": contexto,
            "status": "Analisado"
        }
        enviar_para_webhook(payload, "ideias")
    
    return contexto

if __name__ == "__main__":
    aprofundar_ideia("O impacto da tecnologia TOPCon na eficiência solar em 2026", "jcantunes")

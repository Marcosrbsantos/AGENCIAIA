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

def gerar_estrategia(tema, perfil_id, formato, contexto_pesquisa):
    """
    O Agente Estrategista decide o Gancho, a Estrutura e o CTA.
    Usa o Gemini Flash para garantir sofisticação estratégica.
    """
    if not GEMINI_KEY:
        return "⚠️ Erro: GEMINI_API_KEY não configurada para o Estrategista."

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    
    headers = {"Content-Type": "application/json"}
    
    prompt = f"""
    Aja como o Agente Estrategista do sistema Arquiteto Vivo.
    Sua missão é definir a engenharia de retenção para um novo conteúdo.

    DADOS DE ENTRADA:
    - Tema: "{tema}"
    - Perfil: {perfil_id}
    - Formato: {formato}
    - Contexto da Pesquisa: {contexto_pesquisa}

    SAÍDA REQUERIDA (Seja direto e brilhante):
    1. GANCHO (HOOK): A frase exata de abertura (0-5 segundos) que IMPEDE o usuário de rolar a tela.
    2. ESTRUTURA EM 3 BLOCOS:
       - Bloco 1 (Conexão): O que dizer logo após o gancho para manter a pessoa?
       - Bloco 2 (Valor/Tensão): O núcleo do conteúdo.
       - Bloco 3 (Revelação/Clímax): O insight final.
    3. CTA (CHAMADA PARA AÇÃO): O que o usuário deve fazer exatamente ao terminar? (Ex: Comentar uma palavra, clicar no link, etc.)

    Responda em formato de texto limpo, pronto para ser lido pelo Roteirista.
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
            return "Falha na geração estratégica pelo Gemini."
    except Exception as e:
        return f"Erro no Agente Estrategista: {e}"

def decidir_estrategia(tema, perfil_id, formato, contexto_pesquisa, enviar=True):
    """Executa a decisão estratégica e salva se enviar=True"""
    print(f"🧠 [ESTRATEGISTA] Traçando estratégia para: {tema} ({perfil_id})")
    
    estrategia_completa = gerar_estrategia(tema, perfil_id, formato, contexto_pesquisa)
    
    if enviar:
        payload = {
            "tema": tema,
            "perfil": perfil_id,
            "formato": formato,
            "estrategia_gancho_cta": estrategia_completa,
            "status": "Estrategia Definida",
            "data": json.dumps(time.strftime("%d/%m/%Y")) if 'time' in globals() else "13/03/2026"
        }
        enviar_para_webhook(payload, "roteiros")
        
    return estrategia_completa

if __name__ == "__main__":
    import time
    # Simulação de Handoff do Agente 2 e 3
    tema_ex = "Como usar a Lei 14.300 para vender mais energia solar"
    perf_ex = "jcantunes"
    form_ex = "Carrossel Instagram"
    cont_ex = "O mercado está com medo da taxação, mas a lei garante o direito adquirido para quem instalar agora..."
    
    resultado = decidir_estrategia(tema_ex, perf_ex, form_ex, cont_ex)
    print(f"\n🎯 Estratégia Traçada:\n{resultado}")

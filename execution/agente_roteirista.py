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

PERFIS_ROTEIRO = {
    "marcos": {
        "identidade": "Marcos Rafael, criador de conteúdo e estrategista digital. Estilo Renascença Profissional.",
        "tom": "educativo, direto, psicológico, provocador",
        "objetivo": "Transformar o espectador através de insights profundos sobre comportamento e marketing."
    },
    "jcantunes": {
        "identidade": "Empresa JC Antunes, autoridade em energia solar e economia.",
        "tom": "institucional, confiável, comercial, profissional",
        "objetivo": "Educar sobre economia de energia e vender soluções solares com segurança."
    }
}

def carregar_modelos():
    """Tenta carregar modelos de Mad Libs da pasta de referências"""
    try:
        ref_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "referencias", "modelos_roteiros.md")
        if os.path.exists(ref_path):
            with open(ref_path, "r", encoding="utf-8") as f:
                return f.read()
    except Exception as e:
        print(f"⚠️ Erro ao carregar modelos: {e}")
    return ""

def escrever_roteiro_completo(tema, perfil_id, formato, estrategia, contexto):
    """
    O Agente Roteirista escreve o conteúdo final.
    Usa Llama 3.3 70B via Groq para qualidade criativa máxima.
    """
    if not GROQ_KEY:
        return "⚠️ Erro: GROQ_API_KEY não configurada para o Roteirista."

    perfil = PERFIS_ROTEIRO.get(perfil_id, PERFIS_ROTEIRO["marcos"])
    modelos_referencia = carregar_modelos()

    prompt = f"""
    Aja como o Agente Roteirista de Elite do sistema Arquiteto Vivo.
    Sua missão é escrever o roteiro final, palavra por palavra, com base nos dados abaixo.

    MODELOS DE REFERÊNCIA E ESTILO (USE COMO GUIA):
    {modelos_referencia}

    DADOS DE PRODUÇÃO:
    - Tema: "{tema}"
    - Perfil: {perfil['identidade']}
    - Tom de Voz: {perfil['tom']}
    - Objetivo: {perfil['objetivo']}
    - Formato: {formato}
    - Estratégia Definida: {estrategia}
    - Contexto da Pesquisa: {contexto}

    REGRAS DE ESCRITA:
    1. PRIORIZE OS MODELOS ACIMA (MAD LIBS) SE DISPONÍVEIS PARA O FORMATO.
    2. Responda APENAS com o texto do roteiro. Sem introduções ou comentários.
    3. NÃO use negrito, itálico, hashtags ou caracteres especiais de Markdown (#, *, -).
    4. O texto deve ser limpo, pronto para ser lido em voz alta ou colocado em slides.
    5. Respeite as marcações de ritmo (ex: pausa, ênfase) apenas se necessário para a leitura.
    
    ESTRUTURA POR FORMATO:
    - Se YouTube: Use o modelo de 3 blocos detalhado.
    - Se Reels/Shorts: Use o modelo rápido de ganchos visuais.
    - Se Carrossel: Texto para Slide 1 (Gancho), Slides 2-6 (Desenvolvimento), Slide Final (CTA).

    Escreva agora (em Português do Brasil):
    """

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "system", "content": "Você é um roteirista profissional de alta conversão."}, 
                     {"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    try:
        res = requests.post(url, json=payload, headers=headers, timeout=30)
        return res.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"Falha na escrita do roteiro: {e}"

def produzir_conteudo_final(tema, perfil_id, formato, estrategia, contexto, enviar=True):
    """Executa a escrita e salva na planilha se enviar=True"""
    print(f"✍️ [ROTEIRISTA] Escrevendo conteúdo para: {tema} ({formato})")
    
    roteiro_final = escrever_roteiro_completo(tema, perfil_id, formato, estrategia, contexto)
    
    if enviar:
        payload = {
            "tema": tema,
            "perfil": perfil_id,
            "formato": formato,
            "conteudo": roteiro_final,
            "status": "Pronto para Gravar"
        }
        enviar_para_webhook(payload, "roteiros")
        
    return roteiro_final
if __name__ == "__main__":
    # Teste de Escrita
    t = "Por que 99 por cento falha ao economizar energia"
    p = "jcantunes"
    f = "Reels"
    e = "Gancho: Você está jogando dinheiro no lixo. CTA: Siga para parar de perder."
    c = "O erro comum é ignorar as perdas por calor e fiação antiga."
    
    roteiro = produzir_conteudo_final(t, p, f, e, c)
    print(f"\n📜 Roteiro Gerado:\n{roteiro}")

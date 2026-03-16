import os
import requests
import json
import time
from dotenv import load_dotenv

load_dotenv()
WEBHOOK_URL = os.getenv("MAKE_WEBHOOK_URL")

def enviar_mapeamento_mestre():
    """
    Envia um pacote com TODOS os campos possíveis de todos os agentes.
    Isso serve para o Make.com "aprender" todos os campos de uma vez só.
    """
    if not WEBHOOK_URL:
        print("❌ Erro: Link do Webhook não encontrado no .env")
        return

    # Super Payload com TODOS os campos de TODAS as abas
    payload_mestre = {
        # Campos Universais
        "aba_destino": "mapeamento",
        "perfil": "teste_perfil",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "data": time.strftime("%d/%m/%Y"),
        "status": "Aberto",
        
        # Campos da aba 'ideias' e 'roteiros'
        "tema": "Título de Teste",
        "formato": "Reels",
        "nota_relevancia": 10,
        "prioridade": 10,
        "contexto": "Análise estratégica...",
        "gancho": "Gancho impacto...",
        "cta": "Chamada para ação...",
        "conteudo": "Texto do roteiro...",
        "estrategia_gancho_cta": "Estratégia completa...",
        "performance": "Métricas iniciais",

        # Campos da aba 'insights' (Estes estavam faltando!)
        "insight": "Dica de ouro de teste",
        "categoria": "Tendência",
        "usado": "Não",

        # Campos da aba 'design_queue'
        "template": "premium_dark",
        "arquivo_gerado": "foto_v1.png",
        "link_drive": "https://link-da-imagem.com",
        "imagem_url": "https://link-da-imagem.com",

        # Campos de Agenda (Calendário)
        "data_publicacao": "2026-03-13",
        "hora_publicacao": "18:00",
        "hora": "18:00",
        "plataforma": "Instagram",

        # Campos de Analytics
        "periodo": "Mensal",
        "top_conteudo": "Post Solar",
        "padrao_identificado": "Vídeos curtos engajam mais",
        "recomendação": "Postar 3x por semana",
        "views": 1000,
        "likes": 50,
        "insight_aprendizado": "Aprendizado contínuo"
    }

    print("📤 Enviando o Mapeamento Mestre para o Make.com...")
    try:
        res = requests.post(WEBHOOK_URL, json=payload_mestre, timeout=10)
        if res.status_code == 200:
            print("✅ SUCESSO! O Make.com agora conhece todos os campos.")
            print("👉 Agora você pode voltar lá e mapear tudo com calma.")
        else:
            print(f"❌ Erro {res.status_code}: {res.text}")
    except Exception as e:
        print(f"❌ Falha: {e}")

if __name__ == "__main__":
    enviar_mapeamento_mestre()

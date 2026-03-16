import os
import requests
import json
import time
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()
WEBHOOK_URL = os.getenv("MAKE_WEBHOOK_URL")

def enviar_tiro_certeiro():
    """Envia um dado sem pastas ou filtros complexos para teste real"""
    print(f"📡 Disparando 'Tiro Certeiro' para {WEBHOOK_URL}...")
    
    payload = {
        "Destino": "IDEIAS",
        "Insight": "TESTE DE EMERGÊNCIA: Se você vir isso, o filtro de IDEIAS funcionou!",
        "Plataforma": "TESTE",
        "Data_Criacao": time.strftime("%d/%m/%Y %H:%M:%S"),
        "Referencia_Link": "N/A"
    }
    
    print(f"📦 Payload enviado:\n{json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(WEBHOOK_URL, json=payload, timeout=10)
        print(f"\n📡 Resposta do Servidor: {response.status_code}")
        print(f"💬 Mensagem: {response.text}")
        if response.status_code == 200:
            print("\n✅ O Make.com RECEBEU. Se não está na planilha, o erro é no FILTRO ou no SHEET ID.")
    except Exception as e:
        print(f"❌ Falha crítica: {str(e)}")

if __name__ == "__main__":
    enviar_tiro_certeiro()
 Eleanor

import os
import requests
from dotenv import load_dotenv
import json

load_dotenv()

MAKE_URL = os.getenv("MAKE_WEBHOOK_URL")
FAREJADOR_URL = os.getenv("FAREJADOR_URL")
GROQ_KEY = os.getenv("GROQ_API_KEY")

print("--- INICIANDO TESTE DA INFRAESTRUTURA NUVEM ---")

def test_make():
    print(f"\n1. Testando Make.com Webhook ({MAKE_URL})")
    try:
        data = {"nicho": "saude"}
        res = requests.post(MAKE_URL, json=data)
        print(f"Status Code: {res.status_code}")
        print(f"Resposta: {res.text}")
    except Exception as e:
        print(f"Erro: {e}")

def test_pythonanywhere():
    print(f"\n2. Testando PythonAnywhere Scraper ({FAREJADOR_URL})")
    try:
        url = FAREJADOR_URL + "?nicho=saude"
        res = requests.get(url)
        print(f"Status Code: {res.status_code}")
        print(f"Resposta: {res.text[:200]}...") # truncate para não poluir
    except Exception as e:
        print(f"Erro: {e}")

def test_groq():
    print(f"\n3. Testando Chave de API Groq Whisper")
    if not GROQ_KEY or len(GROQ_KEY) < 10:
        print(f"Chave Groq parece inválida ou não encontrada.")
        return
    try:
        # Testa a API de modelos simples do groq para ver se a chave é válida
        headers = {"Authorization": f"Bearer {GROQ_KEY}"}
        res = requests.get("https://api.groq.com/openai/v1/models", headers=headers)
        print(f"Status Code: {res.status_code}")
        if res.status_code == 200:
            print("Conexão com Groq OK!")
        else:
            print(f"Erro: {res.text}")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    if not requests:
        print("requests precisa ser instalado")
    else:
        test_make()
        test_pythonanywhere()
        test_groq()

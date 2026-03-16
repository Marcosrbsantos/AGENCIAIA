import os
import requests
from dotenv import load_dotenv
import json

load_dotenv()
TOKEN = os.getenv("PENPOT_ACCESS_TOKEN")

if not TOKEN:
    print("❌ Token não encontrado no .env")
    exit()

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

print("🔄 Testando autenticação Penpot...")
response = requests.get("https://design.penpot.app/api/rpc/command/get-profile", headers=headers)

if response.status_code == 200:
    print("✅ Sucesso!")
    data = response.json()
    print(f"👤 Usuário: {data.get('email')}")
    
    # Pegar os times
    print("\n🏢 Buscando Times do Usuário...")
    teams = requests.get("https://design.penpot.app/api/rpc/command/get-teams", headers=headers).json()
    for team in teams:
        print(f" - Time: {team.get('name')} (ID: {team.get('id')})")
        
        # Pegar projetos do time
        team_id = team.get('id')
        payload = {"id": team_id}
        projects = requests.post("https://design.penpot.app/api/rpc/command/get-projects", headers=headers, json=payload).json()
        for p in projects:
             print(f"   📂 Projeto: {p.get('name')} (ID: {p.get('id')})")
             
else:
    print(f"❌ Erro na API: {response.status_code}")
    print(response.text)

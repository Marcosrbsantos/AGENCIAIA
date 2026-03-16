from flask import Flask, render_template, request, jsonify, session
import os
import requests
import json
import csv
import io

# Tenta carregar bibliotecas opcionais
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

app = Flask(__name__)
app.config['SECRET_KEY'] = 'creata-secret-key-arquiteto'

GROQ_KEY = os.getenv("GROQ_API_KEY")

# CONFIGURAÇÃO DE PERFIS
PERFIS = {
    "marcos": {
        "nome": "Marcos (Pessoal)",
        "nicho": "Marketing, Tecnologia, Comportamento",
        "tema": "Renascença Profissional",
        "estilo": "educativo, direto, psicológico",
        "cor": "#940000"
    },
    "jcantunes": {
        "nome": "JC Antunes (Empresa)",
        "nicho": "Energia Solar, Economia",
        "tema": "Profissional, Clean",
        "estilo": "institucional, comercial, confiável",
        "cor": "#004a94"
    }
}

# CONFIGURAÇÃO DA PLANILHA (Sincronização Reversa)
PUB_ID = "2PACX-1vRLiVnBrAAYV7wCGLP1eN53ha8OMQO1hzzp4bkqL8uHaui-s5mshZpTBlteeSmCDX2x9GgorIItNuD7"
GIDS = {
    "ideias": "0", # GID real da sua aba ideias (ajustar se mudar)
    "roteiros": "123456", # Exemplo de GID
    "insights": "2005377382",
    "analytics": "78910"
}

def carregar_dados_perfil(perfil_id):
    """Carrega dados da planilha filtrados por perfil"""
    url_ideias = f"https://docs.google.com/spreadsheets/d/e/{PUB_ID}/pub?output=csv&gid={GIDS['ideias']}"
    
    dados = {"ideias": [], "insights": []}
    
    try:
        # Carregar Ideias
        res = requests.get(url_ideias, timeout=5)
        if res.status_code == 200:
            reader = csv.DictReader(io.StringIO(res.text))
            for row in reader:
                # Se o perfil na planilha bater com o selecionado
                if row.get("perfil", "").lower() == perfil_id:
                    dados["ideias"].append(row)
        
        # Carregar Insights (Geral)
        url_insights = f"https://docs.google.com/spreadsheets/d/e/{PUB_ID}/pub?output=csv&gid={GIDS['insights']}"
        res_i = requests.get(url_insights, timeout=5)
        if res_i.status_code == 200:
            reader_i = csv.DictReader(io.StringIO(res_i.text))
            for row in reader_i:
                dados["insights"].append(row)
                
        return dados
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        return None

def chamar_arquiteto_llm(perfil_id, user_input):
    if not GROQ_KEY: 
        return "⚠️ [ERRO]: Cérebro off-line. Configure a GROQ_API_KEY."
    
    perfil = PERFIS.get(perfil_id, PERFIS["marcos"])
    
    system_prompt = f"""Você é o Arquiteto Vivo, agindo no perfil {perfil['nome']}.
Nicho: {perfil['nicho']}. Tom: {perfil['estilo']}.
Siga rigorosamente a identidade deste perfil."""

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_input}],
        "temperature": 0.5
    }
    
    try:
        res = requests.post(url, json=payload, headers=headers)
        return res.json()['choices'][0]['message']['content']
    except:
        return "Falha na conexão com o cérebro."

@app.route('/')
def index():
    perfil_id = request.args.get('perfil', 'marcos')
    if perfil_id not in PERFIS: perfil_id = 'marcos'
    
    dados = carregar_dados_perfil(perfil_id)
    perfil_info = PERFIS[perfil_id]
    
    return render_template('index.html', 
                           perfil=perfil_info, 
                           perfil_id=perfil_id,
                           ideias=dados["ideias"] if dados else [],
                           insights=dados["insights"] if dados else [])

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    perfil_id = data.get('perfil', 'marcos')
    user_msg = data.get('message', '')
    response = chamar_arquiteto_llm(perfil_id, user_msg)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True, port=8100)

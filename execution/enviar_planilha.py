import os
import requests
import json
import time
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()
WEBHOOK_URL = os.getenv("MAKE_WEBHOOK_URL")

def limpar_markdown(texto):
    """Remove caracteres de marcação Markdown e evita células gigantes na planilha"""
    if not texto:
        return ""
    # Remove marcações comuns
    for char in ["#", "*", "---", "__", ">", "`"]:
        texto = texto.replace(char, "")
    
    # Limpa espaços em branco e quebras de linha excessivas
    linhas = [l.strip() for l in texto.split("\n") if l.strip()]
    
    if len(linhas) > 5:
        # Mantém as 3 primeiras linhas e junta o resto com um separador
        topo = linhas[:3]
        resto = " | ".join(linhas[3:15])
        return "\n".join(topo) + "\n---\n" + resto + ("..." if len(linhas) > 15 else "")
    
    return "\n".join(linhas)

def enviar_para_webhook(payload, aba_destino):
    """
    Envia qualquer payload para o Make.com.
    aba_destino deve ser: ideias, roteiros, insights, design_queue, calendario ou analytics.
    """
    if not WEBHOOK_URL:
        print("Erro: MAKE_WEBHOOK_URL não encontrada no .env")
        return False

    # Limpeza Automática de todos os campos do payload
    for chave, valor in payload.items():
        if isinstance(valor, str):
            # Se for um campo de texto longo, limpa marcações
            if chave in ["contexto", "conteudo", "estrategia_gancho_cta"]:
                payload[chave] = limpar_markdown(valor)
            else:
                payload[chave] = valor.strip()

    # Adiciona metadados universais
    payload["aba_destino"] = aba_destino
    payload["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")

    try:
        response = requests.post(WEBHOOK_URL, json=payload, timeout=15)
        if response.status_code == 200:
            print(f"✅ [SINC] {aba_destino.upper()}: Enviado com sucesso.")
            return True
        else:
            print(f"❌ [ERRO] {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"❌ [FALHA]: {str(e)}")
        return False

def formatar_ideia(tema, perfil, relevancia, formato="A definir"):
    """Padroniza o objeto Ideia para a aba 'ideias'"""
    return {
        "tema": tema,
        "perfil": perfil,
        "data": time.strftime("%d/%m/%Y"),
        "status": "Aberto",
        "nota_relevancia": relevancia,
        "formato": formato
    }

def sincronizar_roteiros_completos():
    """Sincroniza os roteiros detalhados"""
    caminho_base = r"C:\Users\Admin\.gemini\antigravity\brain\bb885d9d-17c4-480d-8b96-bc832cb3e051"
    
    scripts = {
        "roteiro_detalhado_youtube.md": ("A Engenharia do Vício (YouTube)", "Vídeo Longo", "https://www.youtube.com/watch?v=RfQD9unCQtE", "https://img.youtube.com/vi/RfQD9unCQtE/maxresdefault.jpg"),
        "roteiro_vicios.md": ("A Arquitetura do Vício (Reels)", "Vídeo Curto", "https://www.youtube.com/shorts/bE7MpdG7WrU", "https://img.youtube.com/vi/bE7MpdG7WrU/maxresdefault.jpg"),
        "roteiro_tdah_foco.md": ("O Labirinto da Atenção (TDAH)", "Vídeo Longo", "https://www.youtube.com/shorts/Ezs-SRrUXOA", "https://img.youtube.com/vi/Ezs-SRrUXOA/maxresdefault.jpg")
    }

    print("📤 Sincronizando Roteiros...")
    for filename, (titulo, tipo, link, thumb) in scripts.items():
        path = os.path.join(caminho_base, filename)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                conteudo = f.read()
                payload = {
                    "Tema": f"[{tipo}] {titulo}",
                    "Data_Pesquisa": time.strftime("%d/%m/%Y %H:%M:%S"),
                    "Relatorio": limpar_markdown(conteudo),
                    "Link": link,
                    "Miniatura": thumb
                }
                enviar_para_webhook(payload, "roteiros")

def sincronizar_aba_ideias():
    """Sincroniza 10 ideias de vídeo"""
    print("\n💡 Sincronizando 10 Ideias...")
    ideias = [
        ("O Jejum de Dopamina 2.0", "jcantunes", 8, "YouTube"),
        ("A Armadilha do Scroll Infinito", "jcantunes", 7, "Reels"),
        ("Habit Stacking para TDAH", "jcantunes", 9, "Shorts"),
        ("O Custo do Context Switch", "jcantunes", 8, "YouTube"),
        ("Deep Work em Ambientes Ruidosos", "jcantunes", 7, "Shorts"),
        ("A Ciência do Gancho de 1.5s", "jcantunes", 6, "Reels"),
        ("O Mal do Século: Atenção Fragmentada", "jcantunes", 9, "YouTube"),
        ("Sono Coletivo e Luz Azul", "jcantunes", 7, "Shorts"),
        ("A Escada da Complexidade", "jcantunes", 8, "YouTube"),
        ("Minimalismo Digital Hoje", "jcantunes", 6, "Reels")
    ]

    for tema, perfil, relevancia, formato in ideias:
        payload = formatar_ideia(tema, perfil, relevancia, formato)
        enviar_para_webhook(payload, "ideias")

if __name__ == "__main__":
    sincronizar_roteiros_completos()
    sincronizar_aba_ideias()

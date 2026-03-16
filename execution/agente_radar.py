import os
import requests
import xml.etree.ElementTree as ET
from enviar_planilha import enviar_para_webhook, formatar_ideia

# CONFIGURAÇÃO DE FONTES POR PERFIL
FONTES = {
    "marcos": [
        "https://meioemensagem.com.br/feed",
        "https://canaltech.com.br/rss/",
        "https://wired.com/feed/rss"
    ],
    "jcantunes": [
        "https://canalsolar.com.br/feed/",
        "https://absolar.org.br/feed/",
        "https://www.portalsolar.com.br/noticias/feed"
    ]
}

def buscar_tendencias(perfil_id):
    """Varre os feeds RSS em busca de notícias recentes"""
    urls = FONTES.get(perfil_id, [])
    ideias_encontradas = []

    print(f"🛰️ Radar ativado para: {perfil_id}")
    
    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                root = ET.fromstring(response.content)
                # RSS padrão tem itens dentro de channel
                items = root.findall("./channel/item")
                for item in items[:1]: # Pega apenas a mais recente de cada fonte
                    titulo = item.find("title").text
                    link = item.find("link").text
                    
                    # Criar objeto Ideia
                    ideia = formatar_ideia(
                        tema=f"{titulo} (Fonte: {url.split('/')[2]})",
                        perfil=perfil_id,
                        relevancia=8, # Valor base
                        formato="A definir"
                    )
                    ideias_encontradas.append(ideia)
        except Exception as e:
            print(f"⚠️ Falha ao ler feed {url}: {e}")

    return ideias_encontradas

def executar_radar_completo():
    """Executa a varredura para ambos os perfis e envia para a planilha"""
    for perfil in ["marcos", "jcantunes"]:
        resultados = buscar_tendencias(perfil)
        print(f"✅ {len(resultados)} ideias encontradas para {perfil}.")
        
        for item in resultados:
            enviar_para_webhook(item, "ideias")

if __name__ == "__main__":
    executar_radar_completo()

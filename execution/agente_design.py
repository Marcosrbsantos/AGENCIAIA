import os
import requests
import json
import urllib.parse
from enviar_planilha import enviar_para_webhook

# O Design Agent usa Pollinations.ai (100% Grátis e sem API Key)
BASE_POLLINATIONS_URL = "https://pollinations.ai/p/"

def carregar_tokens():
    """Tenta carregar tokens de design da pasta de referências"""
    try:
        ref_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "referencias", "estetica_tokens.md")
        if os.path.exists(ref_path):
            with open(ref_path, "r", encoding="utf-8") as f:
                return f.read()
    except Exception as e:
        print(f"⚠️ Erro ao carregar tokens: {e}")
    return ""

def gerar_prompt_visual(tema, perfil_id):
    """
    Usa a inteligência para criar um prompt de imagem otimizado com base nos tokens.
    """
    tokens = carregar_tokens()
    
    # Se for Marcos, aplicamos a Estética "Anatomia Mestra" que o usuário enviou como referência.
    if perfil_id == "marcos":
        # Extrair a palavra-chave central para a anatomia (ex: cerebro, coracao, olho, funil, etc)
        # Por enquanto vamos usar 'brain' como default para testar a engine.
        prompt_base = f"Highly detailed vintage medical engraving illustration of a human anatomy related to {tema}, pure white lines on a solid black background, minimalist, encyclopedia style, high contrast, clean vector style, no text, no background noise, centered."
    else:
        estetica_base = "clean, solar energy, bright, modern architecture, eco-friendly"
        prompt_base = f"{tema}, {estetica_base}, photorealistic, 8k, cinematic lighting. Follow brand styles: {perfil_id.upper()}"
        
    return urllib.parse.quote(prompt_base)

def criar_design_automatico(tema, perfil_id, roteiro_breve, enviar=True):
    """
    O Agente de Design gera o conceito visual e o link da imagem.
    """
    print(f"🎨 [DESIGN] Gerando conceito visual para: {tema}")
    
    prompt_encoded = gerar_prompt_visual(tema, perfil_id)
    image_url = f"{BASE_POLLINATIONS_URL}{prompt_encoded}?width=1024&height=1024&model=flux"
    
    # Simulação de template (Agente decidiria qual usar)
    template = "post_promocional" if perfil_id == "jcantunes" else "capa_reels"

    if enviar:
        payload = {
            "tema": tema,
            "perfil": perfil_id,
            "template": template,
            "status": "Imagem Gerada",
            "arquivo_gerado": f"visual_{perfil_id}_{time.strftime('%H%M%S')}.png" if 'time' in globals() else "visual_pendente.png",
            "link_drive": image_url # Por enquanto enviamos o link direto da IA
        }
        enviar_para_webhook(payload, "design_queue")
    
    return image_url

if __name__ == "__main__":
    import time
    # Teste de Design
    t = "O Futuro das Baterias Solares"
    p = "jcantunes"
    r = "As baterias de grafeno estão chegando para mudar tudo..."
    
    url_final = criar_design_automatico(t, p, r)
    print(f"\n🖼️ Design Gerado com Sucesso!")
    print(f"🔗 Link da Imagem: {url_final}")

import os
import requests
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import textwrap

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

def baixar_imagem(url, caminho_local):
    """Baixa a imagem do Pollinations para o computador local"""
    try:
        # Adicionar User-Agent para evitar ser bloqueado
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            with open(caminho_local, "wb") as f:
                f.write(response.content)
            # Verifica se a imagem tem um tamanho mínimo (ex: > 10KB)
            if os.path.getsize(caminho_local) > 10000:
                return True
            else:
                print(f"⚠️ Imagem baixada é muito pequena ({os.path.getsize(caminho_local)} bytes). Provável erro da API.")
    except Exception as e:
        print(f"❌ Erro ao baixar imagem: {e}")
    return False

from compositor_anatomia import criar_slide_anatomia

def compor_post_final(tema, perfil_id, url_imagem, output_path):
    """
    Pega a imagem crua da IA e adiciona o título estratégico com design premium.
    """
    temp_img_path = "temp_background.png"
    usar_fallback = False
    
    if not baixar_imagem(url_imagem, temp_img_path):
        print("⚠️ Usando fallback de cor sólida (Design Minimalista).")
        usar_fallback = True

    # Se for Marcos, usa a novíssima estética "Anatomia das Vendas"
    if perfil_id == "marcos" and not usar_fallback:
        texto_principal = tema.split("(Fonte:")[0].strip().upper()
        if len(texto_principal) > 80:
            texto_principal = texto_principal[:80] + "..."
        texto_secundario = "Anatomia do Marketing Estratégico"
        
        caminho_gerado = criar_slide_anatomia(texto_principal, texto_secundario, temp_img_path, output_path)
        if os.path.exists(temp_img_path):
            os.remove(temp_img_path)
        print(f"✅ Slide 'Anatomia' Gerado: {caminho_gerado}")
        return caminho_gerado

    try:
        # 1. Definir Estética por Perfil (JC Antunes ou Fallback)
        width, height = 1080, 1350 # Modernizado para formato Reels/Carousel portrait
        
        if usar_fallback:
            if perfil_id == "marcos":
                img = Image.new("RGBA", (width, height), (0, 0, 0, 255)) # Preto Anatomia
            else:
                img = Image.new("RGBA", (width, height), (0, 40, 80, 255)) # Azul Solar Profundo
        else:
            img = Image.open(temp_img_path).convert("RGBA")
            img = img.resize((width, height), Image.Resampling.LANCZOS)
        
        # 2. Criar camada de desenho
        overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        if not usar_fallback:
            if perfil_id != "marcos":
                # Gradiente preto na base
                for i in range(height // 2):
                    alpha = int(220 * (i / (height // 2)))
                    draw.line([(0, height - i), (width, height - i)], fill=(0, 0, 0, alpha))
            else:
                # Tintura azulada
                draw.rectangle([0, 0, width, height], fill=(0, 20, 50, 80))
        
        cor_texto = (255, 255, 255, 255)

        # 4. Configurar Fonte
        try:
            font_path = "C:\\Windows\\Fonts\\arialbd.ttf"
            font_size = int(width * 0.07)
            font = ImageFont.truetype(font_path, font_size)
            font_small = ImageFont.truetype(font_path, int(font_size * 0.5))
        except:
            font = ImageFont.load_default()
            font_small = ImageFont.load_default()

        # 5. Processar Texto
        texto_limpo = tema.split("(Fonte:")[0].strip().upper()
        # Se for muito longo, corta
        if len(texto_limpo) > 100:
            texto_limpo = texto_limpo[:100] + "..."
            
        linhas = textwrap.wrap(texto_limpo, width=20)
        
        # 6. Desenhar Texto Centralizado
        total_h = len(linhas) * (font_size + 10)
        y_text = (height - total_h) // 2
        
        for linha in linhas:
            # Sombra
            draw.text((width//2 + 3, y_text + 3), linha, font=font, fill=(0, 0, 0, 200), anchor="mm")
            # Principal
            draw.text((width//2, y_text), linha, font=font, fill=cor_texto, anchor="mm")
            y_text += font_size + 15

        # 7. Assinatura
        barra_y = height - 100
        draw.rectangle([width//2 - 150, barra_y, width//2 + 150, barra_y + 2], fill=cor_texto)
        draw.text((width//2, barra_y + 30), f"@{perfil_id.upper()} | ARQUITETO VIVO", font=font_small, fill=cor_texto, anchor="mm")

        # 8. Mesclar e Salvar
        final_img = Image.alpha_composite(img, overlay)
        final_img = final_img.convert("RGB")
        
        if not os.path.exists(os.path.dirname(output_path)):
            os.makedirs(os.path.dirname(output_path))
            
        final_img.save(output_path, "JPEG", quality=90)
        if os.path.exists(temp_img_path):
            os.remove(temp_img_path)
            
        print(f"✅ Post Final Gerado: {output_path}")
        return output_path

    except Exception as e:
        print(f"❌ Erro na composição: {e}")
        return None

if __name__ == "__main__":
    # Teste Rápido
    t = "O SEGREDO DA DOPAMINA DIGITAL NO REELS"
    p = "marcos"
    u = "https://pollinations.ai/p/digital%20dopamine%20dark%20concept?width=1024&height=1024&model=flux"
    o = "outputs/teste_marcos.png"
    compor_post_final(t, p, u, o)

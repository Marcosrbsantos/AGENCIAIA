import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

def criar_slide_anatomia(texto_principal, texto_secundario, imagem_anatomica_path, output_path):
    """
    Recria o estilo 'Anatomia das Vendas' (Fundo Preto, Letras Brancas Bold, Ilustração Central).
    """
    largura, altura = 1080, 1350
    img = Image.new('RGB', (largura, altura), color='#000000')
    draw = ImageDraw.Draw(img)

    # 1. Carregar e colar a ilustração anatômica
    img_anatomia = None
    if os.path.exists(imagem_anatomica_path):
        try:
            anatomia = Image.open(imagem_anatomica_path).convert("RGBA")
            # Redimensionar para caber bem no centro (max 800px)
            anatomia.thumbnail((800, 800), Image.Resampling.LANCZOS)
            x_offset = (largura - anatomia.width) // 2
            y_offset = (altura - anatomia.height) // 2
            
            # Ajustar a posição (em alguns slides fica no topo, outros no centro)
            # Vamos colocar ligeiramente acima do centro para o texto respirar
            img.paste(anatomia, (x_offset, int(altura * 0.2)), anatomia)
        except Exception as e:
            print(f"Erro ao carregar anatomia: {e}")

    # 2. Carregar Fontes (Tentando fontes limpas e impactantes)
    try:
        font_path = "C:\\Windows\\Fonts\\arialbd.ttf"  # Arial Bold (Padrão Windows)
        font_titulo = ImageFont.truetype(font_path, 120)
        font_sub = ImageFont.truetype(font_path, 60)
    except:
        font_titulo = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    # 3. Desenhar Texto Principal (ex: "Anatomia das\nvendas.")
    y_text = int(altura * 0.65)
    linhas_titulo = textwrap.wrap(texto_principal, width=20)
    for linha in linhas_titulo:
        # getbbox retorna (left, top, right, bottom)
        bbox = draw.textbbox((0, 0), linha, font=font_titulo)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        draw.text(((largura - w) / 2, y_text), linha, font=font_titulo, fill="white")
        y_text += h + 10

    # 4. Desenhar Texto Secundário (ex: "A estrutura invisível...")
    y_text += 40
    linhas_sub = textwrap.wrap(texto_secundario, width=40)
    for linha in linhas_sub:
        bbox = draw.textbbox((0, 0), linha, font=font_sub)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        draw.text(((largura - w) / 2, y_text), linha, font=font_sub, fill="#CCCCCC") # Cinza claro para subtítulo
        y_text += h + 10

    # Salvar
    img.save(output_path, "PNG")
    print(f"✅ Slide 'Anatomia' criado com sucesso em: {output_path}")
    return output_path

if __name__ == "__main__":
    os.makedirs("outputs", exist_ok=True)
    
    # Criar uma imagem "falsa" para simular a anatomia temporariamente
    fake_brain = Image.new('RGBA', (500, 500), color='#222222')
    fake_draw = ImageDraw.Draw(fake_brain)
    fake_draw.ellipse([50, 50, 450, 450], fill="#555555", outline="white")
    fake_brain.save("outputs/temp_cerebro.png")
    
    criar_slide_anatomia(
        "Anatomia das\nvendas.",
        "A estrutura invisível por trás de todo negócio digital",
        "outputs/temp_cerebro.png",
        "outputs/demo_anatomia.png"
    )

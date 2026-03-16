import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

def criar_slide_anatomia_perfect(texto_principal, output_path):
    """
    Usa as medidas milimétricas (1080x1350) e a tipografia limpa baseada no SVG de referência.
    """
    largura, altura = 1080, 1350
    
    # Grid Padrão: bg preto com máscara branca superior (que é onde vai a ilustração)
    # E um bloco de fundo abaixo para prender o texto (tudo baseado no SVG)
    img = Image.new('RGB', (largura, altura), color='#000000')
    draw = ImageDraw.Draw(img)

    # 1. Carregar Fonte (Arial Preto ou similar, peso forte)
    try:
        font_path = "C:\\Windows\\Fonts\\arialbd.ttf"
        font_titulo = ImageFont.truetype(font_path, 80)
    except:
        font_titulo = ImageFont.load_default()

    # Baseado na estrutura do SVG fornecido:
    # A área de texto fica mais ou menos a partir do Y=700 (abaixo do centro)
    # E está distribuído em um box.
    
    y_text = 750
    linhas_titulo = textwrap.wrap(texto_principal.upper(), width=22)
    
    for linha in linhas_titulo:
        bbox = draw.textbbox((0, 0), linha, font=font_titulo)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        
        # Centralizando e desenhando branco sólido exato ao modelo SVG
        draw.text(((largura - w) / 2, y_text), linha, font=font_titulo, fill="white")
        y_text += h + 20

    # Salvar
    img.save(output_path, "PNG")
    print(f"✅ Slide 'Perfeito' criado com sucesso em: {output_path}")
    return output_path

if __name__ == "__main__":
    os.makedirs("outputs", exist_ok=True)
    criar_slide_anatomia_perfect(
        "Como a dopamina dita suas emoções todo o tempo",
        "outputs/demo_anatomia_perfect.png"
    )

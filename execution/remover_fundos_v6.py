import os
from rembg import remove
from PIL import Image

def process_image(input_path, output_path):
    print(f"Buscando fundo em: {input_path}")
    input_image = Image.open(input_path)
    output_image = remove(input_image)
    output_image.save(output_path)
    print(f"Salvo sem fundo: {output_path}")

paths = [
    ("C:/Users/Admin/.gemini/antigravity/brain/bb885d9d-17c4-480d-8b96-bc832cb3e051/new_warrior_statue_1773511225584.png", "C:/Users/Admin/.gemini/antigravity/brain/bb885d9d-17c4-480d-8b96-bc832cb3e051/new_warrior_transparent.png")
]

for in_p, out_p in paths:
    process_image(in_p, out_p)

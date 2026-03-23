"""
render_post.py - Motor de renderização isolado via Playwright.
Chamado via subprocess pelo agente_telegram.py.
Argumentos: titulo descricao caminho_saida
"""
import sys
import os
import asyncio
from playwright.async_api import async_playwright


TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "template_universal.html")


async def main(titulo, descricao, caminho_saida, template_name="premium_dark", tag="Design Creata"):
    template_file = f"{template_name}.html"
    template_base = os.path.join(os.path.dirname(__file__), "templates", template_file)
    
    # Fallback caso não exista na pasta templates
    if not os.path.exists(template_base):
        template_base = os.path.join(os.path.dirname(__file__), "template_universal.html")

    html_path = "file:///" + os.path.abspath(template_base).replace("\\", "/")
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1080, "height": 1080})
        await page.goto(html_path)

        # Injeta conteúdo no template
        titulo_safe = titulo.replace("'", " ").replace('"', " ").upper()
        descricao_safe = descricao.replace("'", " ").replace('"', " ")
        tag_safe = tag.replace("'", " ").replace('"', " ").upper()
        
        await page.evaluate(f"setContent('{titulo_safe[:80]}', '{descricao_safe[:200]}', '{tag_safe}')")

        await page.wait_for_timeout(1500)
        await page.screenshot(path=caminho_saida, type="png")
        await browser.close()

    print(f"OK:{caminho_saida}")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("USO: python render_post.py 'titulo' 'descricao' 'caminho_saida.png' [template] [tag]")
        sys.exit(1)

    titulo = sys.argv[1]
    descricao = sys.argv[2]
    saida = sys.argv[3]
    template = sys.argv[4] if len(sys.argv) > 4 else "premium_dark"
    tag = sys.argv[5] if len(sys.argv) > 5 else "CREATA IA V10"

    asyncio.run(main(titulo, descricao, saida, template, tag))

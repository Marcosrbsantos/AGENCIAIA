import os
import asyncio
from playwright.async_api import async_playwright

async def generate_image():
    html_path = "file:///" + os.path.abspath("c:/Users/Admin/Desktop/Agente/execution/template_design2.html").replace("\\", "/")
    output_path = os.path.abspath("c:/Users/Admin/Desktop/Agente/outputs/design_profissional_tenis.png")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1080, "height": 1350})
        await page.goto(html_path)
        
        # Wait for the background image and fonts to load
        await page.wait_for_timeout(3000)
        
        # Take screenshot of the exact 1080x1350 viewport
        await page.screenshot(path=output_path, type="png")
        await browser.close()
        
    print(f"✅ Design gerado com perfeição tipográfica em: {output_path}")

if __name__ == "__main__":
    asyncio.run(generate_image())

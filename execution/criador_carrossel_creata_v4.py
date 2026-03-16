import os
import asyncio
from playwright.async_api import async_playwright

def generate_html_slide1():
    img_thinker = "file:///" + os.path.abspath("C:/Users/Admin/.gemini/antigravity/brain/bb885d9d-17c4-480d-8b96-bc832cb3e051/statue_thinker_transparent.png").replace("\\", "/")
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
body {{ margin: 0; padding: 0; width: 1080px; height: 1080px; background-color: #FDF5E6; font-family: 'Inter', sans-serif; position: relative; overflow: hidden; }}
.orange-bar {{ position: absolute; right: 0; top: 0; width: 50px; height: 100%; background-color: #FCA311; z-index: 5; }}
.title-container {{ position: absolute; top: 120px; left: 100px; max-width: 800px; z-index: 20; }}
.title {{ font-size: 100px; font-weight: 900; letter-spacing: -4px; background: linear-gradient(90deg, #1A1A1A 0%, #1A1A1A 30%, #D68311 60%, rgba(214,131,17,0.3) 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0; line-height: 0.9; text-transform: uppercase; }}
.body-text {{ font-size: 34px; font-weight: 400; color: #1A1A1A; line-height: 1.35; margin-top: 30px; max-width: 650px; }}
.body-text strong {{ color: #1A1A1A; font-weight: 800; }}
.sub-text {{ font-size: 26px; font-weight: 800; color: #D68311; margin-top: 40px; }}
.quotes-container {{ margin-top: 80px; }}
.small-texts {{ font-size: 28px; font-weight: 700; color: #E6A755; font-style: italic; line-height: 1.6; transform: rotate(-3deg); display: inline-block; vertical-align: top; }}
.statue {{ position: absolute; bottom: -50px; right: -180px; width: 900px; z-index: 10; filter: drop-shadow(-15px 15px 25px rgba(0,0,0,0.3)); }}
.arrow-btn {{ display: inline-block; border: 3px solid #1A1A1A; border-radius: 8px; padding: 5px 15px; margin-top: 50px; margin-left: 50px; font-weight: 900; font-size: 26px; color: #1A1A1A; vertical-align: top; }}
</style>
</head>
<body>
<div class="orange-bar"></div>
<div class="title-container">
    <h1 class="title">questionamento</h1>
    <div class="body-text">
        Sobre o uso excessivo do celular na atualidade, a pergunta brutal que poucos fazem é: <br><br>
        estamos controlando a ferramenta ou <strong>sendo controlados</strong> por ela?
    </div>
    <div class="sub-text">Isso vai te ajudar a repensar<br>seu consumo digital</div>
    
    <div class="quotes-container">
        <div class="small-texts">
            "só mais um shorts..."<br>
            "deixa eu ver os stories rapidinho..."<br>
            "por que não durmo bem?"
        </div>
        <div class="arrow-btn">&gt;</div>
    </div>
</div>
<img src="{img_thinker}" class="statue">
</body>
</html>"""

def generate_html_slide2():
    img_bust = "file:///" + os.path.abspath("C:/Users/Admin/.gemini/antigravity/brain/bb885d9d-17c4-480d-8b96-bc832cb3e051/statue_bust_transparent.png").replace("\\", "/")
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
body {{ margin: 0; padding: 0; width: 1080px; height: 1080px; background-color: #111; font-family: 'Inter', sans-serif; position: relative; overflow: hidden; }}
.bg-text {{ position: absolute; font-size: 190px; font-weight: 900; color: rgba(255,255,255,0.06); top: -20px; left: -20px; line-height: 0.9; letter-spacing: -6px; z-index: 1; }}
.card {{ position: absolute; top: 50%; transform: translateY(-50%); left: 80px; width: 620px; background-color: #FCA311; border-radius: 60px 0 0 60px; z-index: 5; padding: 80px 80px 80px 80px; box-sizing: border-box; box-shadow: -20px 0 50px rgba(0,0,0,0.5); display: flex; flex-direction: column; justify-content: center; }}
.card-text {{ font-size: 38px; font-weight: 400; color: #332200; line-height: 1.35; }}
.card-text strong {{ color: #FDF5E6; font-weight: 700; text-shadow: 0 0 10px rgba(255,255,255,0.2); }}
.quotes {{ margin-top: 40px; font-size: 30px; color: #FFE3B3; text-align: left; line-height: 1.6; font-weight: 600; padding-left: 20px; }}
.buttons-row {{ margin-top: 40px; display: flex; gap: 15px; font-size: 26px; font-weight: 600; color: #B36800; }}
.btn-ativo {{ color: #FDF5E6; background: rgba(0,0,0,0.1); padding: 5px 15px; border-radius: 8px; }}
.bottom-text {{ font-size: 24px; font-weight: 700; color: #FFE3B3; transform: rotate(-5deg); margin-top: 40px; margin-left: 20px; }}
.statue {{ position: absolute; right: -250px; top: 150px; width: 850px; z-index: 10; filter: drop-shadow(-20px 20px 30px rgba(0,0,0,0.6)); }}
.arrow-btn {{ display: inline-block; border: 3px solid #332200; border-radius: 8px; padding: 5px 15px; margin-top: 30px; align-self: center; font-weight: 900; font-size: 26px; color:#332200; }}
</style>
</head>
<body>
<div class="bg-text">CELULAR<br>CONTROLE<br>ESCRAVO</div>
<div class="card">
    <div class="card-text">
        Muitos "usuários" do mercado não tem nenhuma base de consciência para <strong>nortear ou validar</strong> se a tecnologia está ajudando ou sugando o tempo.
    </div>
    <div class="quotes">
        "você tem uma nova notificação"<br>
        "você precisa responder agora"<br>
        "veja o que estão fazendo"
    </div>
    <div class="buttons-row">
        <span class="btn-ativo">obedece</span>
        <span>não vê sentido</span>
        <span style="opacity: 0.5;">se frustra</span>
    </div>
    <div class="bottom-text">
        o triste caso da rolagem<br>infinita vazia de propósito
    </div>
    <div class="arrow-btn">&gt;</div>
</div>
<img src="{img_bust}" class="statue">
</body>
</html>"""

def generate_html_slide3():
    img_hercules = "file:///" + os.path.abspath("C:/Users/Admin/.gemini/antigravity/brain/bb885d9d-17c4-480d-8b96-bc832cb3e051/statue_hercules_transparent.png").replace("\\", "/")
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
body {{ margin: 0; padding: 0; width: 1080px; height: 1080px; background-color: #111; font-family: 'Inter', sans-serif; position: relative; overflow: hidden; }}
.bg-text {{ position: absolute; font-size: 190px; font-weight: 900; color: rgba(255,255,255,0.06); top: -20px; left: -20px; line-height: 0.9; letter-spacing: -6px; z-index: 1; }}
.card {{ position: absolute; top: 50%; transform: translateY(-50%); left: 80px; width: 620px; background-color: #FCA311; border-radius: 60px 0 0 60px; z-index: 5; padding: 80px 80px 80px 80px; box-sizing: border-box; box-shadow: -20px 0 50px rgba(0,0,0,0.5); display: flex; flex-direction: column; justify-content: center; }}
.text-main {{ font-size: 42px; font-weight: 400; color: #332200; line-height: 1.25; letter-spacing: -1px; }}
.text-main strong {{ color: #FDF5E6; }}
.huge-text {{ font-size: 60px; font-weight: 900; color: #FDF5E6; letter-spacing: -2px; margin: 15px 0; }}
.small-desc {{ font-size: 26px; color: #332200; line-height: 1.4; margin-top: 20px; font-weight:600; }}
.orange-highlight {{ font-size: 28px; font-weight: 700; color: #FFE3B3; margin-top: 40px; }}
.statue {{ position: absolute; right: -250px; bottom: -50px; width: 900px; z-index: 10; filter: drop-shadow(-20px 20px 30px rgba(0,0,0,0.6)); }}
.arrow-btn {{ display: inline-block; border: 3px solid #332200; border-radius: 8px; padding: 5px 15px; margin-top: 40px; align-self: center; font-weight: 900; font-size: 26px; color:#332200; }}
</style>
</head>
<body>
<div class="bg-text">ENERGIA<br>TEMPO<br>VÍCIO</div>
<div class="card">
    <div class="text-main">
        Consumir conteúdo que você <strong>ACHA</strong><br>que está te evoluindo, é uma perda de
    </div>
    <div class="huge-text">energia, dinheiro e tempo</div>
    <div class="small-desc">
        depois do boom das redes de formato curto, as plataformas se fortaleceram na cultura do "rolar sem pensar" (just do it)
    </div>
    <div class="orange-highlight">
        mas ela peca em um ponto <strong>muito</strong> importante
    </div>
    <div class="arrow-btn">&gt;</div>
</div>
<img src="{img_hercules}" class="statue">
</body>
</html>"""

def generate_html_slide4():
    img_spartan = "file:///" + os.path.abspath("C:/Users/Admin/.gemini/antigravity/brain/bb885d9d-17c4-480d-8b96-bc832cb3e051/spartan_army_frame_1773455967640.png").replace("\\", "/")
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
body {{ margin: 0; padding: 0; width: 1080px; height: 1080px; background-color: #111111; font-family: 'Inter', sans-serif; position: relative; overflow: hidden; }}
.light-glow {{ position: absolute; top: 0; left: 0; width: 800px; height: 800px; background: radial-gradient(circle at center, rgba(252, 163, 17, 0.4) 0%, transparent 60%); z-index: 1; }}
.orange-bar {{ position: absolute; left: 0; top: 0; width: 20px; height: 100%; background-color: #FCA311; z-index: 2; }}
.center-content {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); z-index: 10; width: 800px; }}
.image-box {{ width: 600px; height: 350px; background-image: url('{img_spartan}'); background-size: cover; background-position: center; border-radius: 40px; margin: 0 auto; box-shadow: 0 30px 60px rgba(0,0,0,0.8); border: 2px solid rgba(252, 163, 17, 0.3); }}
.main-quote {{ text-align: center; color: #FCA311; font-size: 40px; margin-top: 40px; line-height: 1.35; font-weight: 400; }}
.small-white {{ text-align: center; color: #FDF5E6; font-size: 26px; margin-top: 60px; font-weight: 500; letter-spacing: -1px; }}
.rotated-text {{ position: absolute; right: -50px; top: 380px; font-size: 32px; font-weight: 800; color: #FDF5E6; transform: rotate(15deg); line-height: 1.2; text-shadow: 0 0 20px rgba(255,255,255,0.4); }}
.arrow-btn {{ border: 3px solid #FDF5E6; border-radius: 8px; padding: 5px 15px; display: inline-block; margin-top: 20px; font-weight: 900; font-size: 24px; color:#FDF5E6; }}
</style>
</head>
<body>
<div class="light-glow"></div>
<div class="orange-bar"></div>
<div class="center-content">
    <div class="image-box"></div>
    <div class="main-quote">
        a verdade pode ser dura,<br>mas ainda é a verdade...
    </div>
    <div class="rotated-text">sem papo<br>furado, tá?</div>
    <div class="small-white">
        suas ações em relação à tela precisam de um propósito de volta<br>
        <div class="arrow-btn">&gt;</div>
    </div>
</div>
</body>
</html>"""

async def generate_all_images():
    html_slide1 = generate_html_slide1()
    html_slide2 = generate_html_slide2()
    html_slide3 = generate_html_slide3()
    html_slide4 = generate_html_slide4()
    
    with open("c:/Users/Admin/Desktop/Agente/execution/temp_slide1.html", "w", encoding="utf-8") as f: f.write(html_slide1)
    with open("c:/Users/Admin/Desktop/Agente/execution/temp_slide2.html", "w", encoding="utf-8") as f: f.write(html_slide2)
    with open("c:/Users/Admin/Desktop/Agente/execution/temp_slide3.html", "w", encoding="utf-8") as f: f.write(html_slide3)
    with open("c:/Users/Admin/Desktop/Agente/execution/temp_slide4.html", "w", encoding="utf-8") as f: f.write(html_slide4)

    os.makedirs("c:/Users/Admin/Desktop/Agente/outputs/carrossel_creata_v4", exist_ok=True)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1080, "height": 1080})
        
        await page.goto("file:///" + os.path.abspath("c:/Users/Admin/Desktop/Agente/execution/temp_slide1.html").replace("\\", "/"))
        await page.wait_for_timeout(2000)
        await page.screenshot(path="c:/Users/Admin/Desktop/Agente/outputs/carrossel_creata_v4/slide_01.png", type="png")
        
        await page.goto("file:///" + os.path.abspath("c:/Users/Admin/Desktop/Agente/execution/temp_slide2.html").replace("\\", "/"))
        await page.wait_for_timeout(2000)
        await page.screenshot(path="c:/Users/Admin/Desktop/Agente/outputs/carrossel_creata_v4/slide_02.png", type="png")
        
        await page.goto("file:///" + os.path.abspath("c:/Users/Admin/Desktop/Agente/execution/temp_slide3.html").replace("\\", "/"))
        await page.wait_for_timeout(2000)
        await page.screenshot(path="c:/Users/Admin/Desktop/Agente/outputs/carrossel_creata_v4/slide_03.png", type="png")
        
        await page.goto("file:///" + os.path.abspath("c:/Users/Admin/Desktop/Agente/execution/temp_slide4.html").replace("\\", "/"))
        await page.wait_for_timeout(2000)
        await page.screenshot(path="c:/Users/Admin/Desktop/Agente/outputs/carrossel_creata_v4/slide_04.png", type="png")
        
        await browser.close()
        
    print("✅ Carrossel Creata v4 gerado com sucesso!")

if __name__ == "__main__":
    asyncio.run(generate_all_images())

import os
import asyncio
from playwright.async_api import async_playwright

def generate_html_slide1():
    img_thinker = "file:///" + os.path.abspath("C:/Users/Admin/.gemini/antigravity/brain/bb885d9d-17c4-480d-8b96-bc832cb3e051/statue_thinker_1773455860065.png").replace("\\", "/")
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
body {{ margin: 0; padding: 0; width: 1080px; height: 1350px; background-color: #f7ede2; font-family: 'Inter', sans-serif; position: relative; overflow: hidden; }}
.orange-bar {{ position: absolute; right: 0; top: 0; width: 60px; height: 100%; background-color: #fca311; }}
.title-container {{ position: absolute; top: 350px; left: 120px; }}
.title {{ font-size: 180px; font-weight: 900; letter-spacing: -8px; background: linear-gradient(90deg, #111 0%, #111 20%, #b36800 50%, #fdf5e6 90%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0; line-height: 0.9; }}
.body-text {{ font-size: 40px; font-weight: 400; color: #111; max-width: 780px; line-height: 1.3; margin-top: 40px; }}
.highlight {{ color: #d68311; font-weight: 700; }}
.sub-text {{ font-size: 32px; font-weight: 800; color: #d68311; margin-top: 50px; }}
.small-texts {{ font-size: 34px; font-weight: 700; color: #e6a755; margin-top: 60px; font-style: italic; line-height: 1.6; transform: rotate(-3deg); }}
.statue {{ position: absolute; bottom: -50px; right: 100px; width: 600px; z-index: 10; filter: drop-shadow(-10px 10px 20px rgba(0,0,0,0.15)); mix-blend-mode: multiply; }}
.arrow-btn {{ display: inline-block; border: 3px solid #111; border-radius: 8px; padding: 5px 15px; margin-left: 310px; margin-top: -150px; position:absolute; font-weight: 900; font-size: 30px; }}
</style>
</head>
<body>
<div class="orange-bar"></div>
<div class="title-container">
    <h1 class="title">controle</h1>
    <div class="body-text">
        Sobre o uso excessivo do celular na atualidade, a pergunta brutal que poucos fazem é: <br><br>
        estamos controlando a ferramenta ou <strong>sendo controlados</strong> por ela?
    </div>
    <div class="sub-text">Isso vai te ajudar a repensar seu consumo digital</div>
    
    <div class="small-texts">
        "só mais um shorts..."<br>
        "deixa eu ver os stories rapidinho..."<br>
        "por que não durmo bem?"
    </div>
    <div class="arrow-btn">&gt;</div>
</div>
<img src="{img_thinker}" class="statue">
</body>
</html>"""

def generate_html_slide2():
    img_bust = "file:///" + os.path.abspath("C:/Users/Admin/.gemini/antigravity/brain/bb885d9d-17c4-480d-8b96-bc832cb3e051/statue_bust_1773455872467.png").replace("\\", "/")
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
body {{ margin: 0; padding: 0; width: 1080px; height: 1350px; background-color: #111; font-family: 'Inter', sans-serif; position: relative; overflow: hidden; }}
.bg-text {{ position: absolute; font-size: 300px; font-weight: 900; color: rgba(255,255,255,0.02); top: 0; left: -100px; line-height: 0.8; letter-spacing: -10px; z-index: 1; word-wrap: break-word; }}
.card {{ position: absolute; top: 180px; left: 60px; right: 0px; bottom: 180px; background-color: #fca311; border-radius: 60px 0 0 60px; z-index: 5; padding: 120px 180px 100px 100px; box-sizing: border-box; box-shadow: -20px 0 50px rgba(0,0,0,0.5); }}
.card-text {{ font-size: 45px; font-weight: 400; color: #222; line-height: 1.4; }}
.card-text strong {{ color: #ffffff; font-weight: 600; text-shadow: 0 0 10px rgba(255,255,255,0.3); }}
.quotes {{ margin-top: 50px; font-size: 35px; color: #ffdb99; text-align: center; line-height: 1.6; font-weight: 600; }}
.buttons-row {{ margin-top: 80px; display: flex; gap: 20px; font-size: 32px; font-weight: 600; color: #a46100; justify-content: center; }}
.btn-ativo {{ color: #fff; background: rgba(255,255,255,0.2); padding: 5px 20px; border-radius: 10px; }}
.bottom-text {{ font-size: 30px; font-weight: 700; color: #ffdb99; transform: rotate(-5deg); margin-top: 80px; margin-left: 40px; }}
.statue {{ position: absolute; right: -50px; top: 350px; width: 550px; z-index: 10; filter: drop-shadow(-20px 20px 30px rgba(0,0,0,0.6)); mix-blend-mode: multiply; }}
.arrow-btn {{ display: flex; justify-content: center; border: 3px solid #222; border-radius: 8px; padding: 5px 15px; width: 30px; margin: 60px auto 0; font-weight: 900; font-size: 30px; color:#222; }}
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
    img_hercules = "file:///" + os.path.abspath("C:/Users/Admin/.gemini/antigravity/brain/bb885d9d-17c4-480d-8b96-bc832cb3e051/statue_hercules_1773455887151.png").replace("\\", "/")
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
body {{ margin: 0; padding: 0; width: 1080px; height: 1350px; background-color: #111; font-family: 'Inter', sans-serif; position: relative; overflow: hidden; }}
.bg-text {{ position: absolute; font-size: 300px; font-weight: 900; color: rgba(255,255,255,0.02); top: 0; left: -100px; line-height: 0.8; letter-spacing: -10px; z-index: 1; word-wrap: break-word; }}
.card {{ position: absolute; top: 180px; left: 60px; right: 0px; bottom: 180px; background-color: #fca311; border-radius: 60px 0 0 60px; z-index: 5; padding: 180px 250px 100px 100px; box-sizing: border-box; box-shadow: -20px 0 50px rgba(0,0,0,0.5); }}
.text-main {{ font-size: 55px; font-weight: 400; color: #222; line-height: 1.2; letter-spacing: -1px; }}
.text-main strong {{ color: #ffffff; }}
.huge-text {{ font-size: 78px; font-weight: 900; color: #ffffff; letter-spacing: -2px; margin: 15px 0; }}
.small-desc {{ font-size: 24px; color: #111; line-height: 1.4; margin-top: 20px; font-weight:600; max-width: 600px; }}
.orange-highlight {{ font-size: 30px; font-weight: 700; color: #ffd285; margin-top: 30px; }}
.statue {{ position: absolute; right: -80px; bottom: -80px; width: 600px; z-index: 10; filter: drop-shadow(-20px 20px 30px rgba(0,0,0,0.6)); mix-blend-mode: multiply; }}
.arrow-btn {{ display: flex; justify-content: center; border: 3px solid #222; border-radius: 8px; padding: 5px 15px; width: 30px; margin: 100px 0 0 350px; font-weight: 900; font-size: 30px; color:#222; }}
</style>
</head>
<body>
<div class="bg-text">ENERGIA<br>TEMPO<br>VÍCIO</div>
<div class="card">
    <div class="text-main">
        Consumir conteúdo que você <strong>ACHA</strong><br>que está te evoluindo, é uma perca de
    </div>
    <div class="huge-text">energia, dinheiro e tempo</div>
    <div class="small-desc">
        depois do boom das redes de formato curto (Tiktok, Reels), as empresas se fortaleceram na cultura do "rolar sem pensar" (que projeta lucro)
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
body {{ margin: 0; padding: 0; width: 1080px; height: 1350px; background-color: #0d0d0d; font-family: 'Inter', sans-serif; position: relative; overflow: hidden; }}
.light-glow {{ position: absolute; top: 0; left: 0; width: 700px; height: 900px; background: radial-gradient(circle at center, rgba(252, 163, 17, 0.4) 0%, transparent 60%); z-index: 1; }}
.orange-bar {{ position: absolute; left: 0; top: 0; width: 25px; height: 100%; background-color: #fca311; z-index: 2; }}
.center-content {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); z-index: 10; width: 800px; margin-top:-50px; }}
.image-box {{ width: 600px; height: 250px; background-image: url('{img_spartan}'); background-size: cover; background-position: center; border-radius: 40px; margin: 0 auto; box-shadow: 0 30px 60px rgba(0,0,0,0.8); border: 2px solid rgba(252, 163, 17, 0.3); }}
.main-quote {{ text-align: center; color: #fca311; font-size: 45px; margin-top: 40px; line-height: 1.3; font-weight: 400; }}
.small-white {{ text-align: center; color: #fff; font-size: 30px; margin-top: 80px; font-weight: 500; letter-spacing: -1px; }}
.rotated-text {{ position: absolute; right: 0; top: 300px; font-size: 32px; font-weight: 800; color: #fff; transform: rotate(15deg); line-height: 1.2; text-shadow: 0 0 20px rgba(255,255,255,0.4); }}
.arrow-btn {{ border: 3px solid #fff; border-radius: 8px; padding: 5px 15px; display: inline-block; margin-top: 30px; font-weight: 900; font-size: 30px; color:#fff; }}
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

    os.makedirs("c:/Users/Admin/Desktop/Agente/outputs/carrossel_celular", exist_ok=True)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1080, "height": 1350})
        
        await page.goto("file:///" + os.path.abspath("c:/Users/Admin/Desktop/Agente/execution/temp_slide1.html").replace("\\", "/"))
        await page.wait_for_timeout(2000)
        await page.screenshot(path="c:/Users/Admin/Desktop/Agente/outputs/carrossel_celular/slide_01.png", type="png")
        
        await page.goto("file:///" + os.path.abspath("c:/Users/Admin/Desktop/Agente/execution/temp_slide2.html").replace("\\", "/"))
        await page.wait_for_timeout(2000)
        await page.screenshot(path="c:/Users/Admin/Desktop/Agente/outputs/carrossel_celular/slide_02.png", type="png")
        
        await page.goto("file:///" + os.path.abspath("c:/Users/Admin/Desktop/Agente/execution/temp_slide3.html").replace("\\", "/"))
        await page.wait_for_timeout(2000)
        await page.screenshot(path="c:/Users/Admin/Desktop/Agente/outputs/carrossel_celular/slide_03.png", type="png")
        
        await page.goto("file:///" + os.path.abspath("c:/Users/Admin/Desktop/Agente/execution/temp_slide4.html").replace("\\", "/"))
        await page.wait_for_timeout(2000)
        await page.screenshot(path="c:/Users/Admin/Desktop/Agente/outputs/carrossel_celular/slide_04.png", type="png")
        
        await browser.close()
        
    print("✅ Carrossel Creata gerado com sucesso!")

if __name__ == "__main__":
    asyncio.run(generate_all_images())

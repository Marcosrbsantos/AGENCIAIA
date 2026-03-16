import os
import asyncio
from playwright.async_api import async_playwright

def generate_html_slide1():
    # Estátua Original do Slide 1
    img_thinker = "file:///" + os.path.abspath("C:/Users/Admin/.gemini/antigravity/brain/bb885d9d-17c4-480d-8b96-bc832cb3e051/statue_thinker_transparent.png").replace("\\", "/")
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
body {{ margin: 0; padding: 0; width: 1080px; height: 1080px; background-color: #FDF5E6; font-family: 'Inter', sans-serif; position: relative; overflow: hidden; }}
.orange-bar {{ position: absolute; right: 0; top: 0; width: 50px; height: 100%; background-color: #FCA311; z-index: 5; }}
.title-container {{ position: absolute; top: 120px; left: 100px; width: 950px; z-index: 20; }}

/* Redução sutil na fonte e expansão do Tracking para o QUESTIONAMENTO caber com sobras */
.title {{ font-size: 85px; font-weight: 900; letter-spacing: -2px; background: linear-gradient(90deg, #1A1A1A 0%, #1A1A1A 30%, #D68311 60%, rgba(214,131,17,0.3) 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0; line-height: 0.9; text-transform: uppercase; white-space: nowrap; }}
.body-text {{ font-size: 34px; font-weight: 400; color: #1A1A1A; line-height: 1.35; margin-top: 30px; max-width: 650px; }}
.body-text strong {{ color: #1A1A1A; font-weight: 800; }}
.sub-text {{ font-size: 26px; font-weight: 800; color: #D68311; position: absolute; top: 600px; left: 100px; z-index: 20; }}

/* Exclusao da Caixa amarela pedida pelo usuario. Agora eh um float limpo de aspas da esquerda */
.quotes-container {{ position: absolute; top: 760px; left: 100px; z-index: 50; padding-left: 20px; border-left: 5px solid #FCA311; }}
.small-texts {{ font-size: 28px; font-weight: 700; color: #E6A755; font-style: italic; line-height: 1.6; display: inline-block; vertical-align: top; text-shadow: 0 0 10px rgba(253,245,230,0.8); }}

.statue {{ position: absolute; bottom: -50px; right: -180px; width: 900px; z-index: 10; filter: drop-shadow(-15px 15px 25px rgba(0,0,0,0.3)); }}
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
</div>
<div class="sub-text">Isso vai te ajudar a repensar<br>seu consumo digital</div>
<div class="quotes-container">
    <div class="small-texts">
        "só mais um shorts..."<br>
        "deixa eu ver os stories rapidinho..."<br>
        "por que não durmo bem?"
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
.quotes {{ margin-top: 40px; font-size: 32px; color: #FFE3B3; text-align: left; line-height: 1.4; font-weight: 600; padding-left: 20px; border-left: 6px solid #FFE3B3; }}

/* Removido o Botao Consome o Dia */

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
        "você tem uma nova notificação, você precisa responder agora, veja o que estão fazendo..."
    </div>
</div>
<img src="{img_bust}" class="statue">
</body>
</html>"""

def generate_html_slide3():
    # Voltamos ao Pensador Clássico (Pedido do usuario no audio)
    img_warrior = "file:///" + os.path.abspath("C:/Users/Admin/.gemini/antigravity/brain/bb885d9d-17c4-480d-8b96-bc832cb3e051/statue_thinker_transparent.png").replace("\\", "/")
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
.orange-highlight {{ font-size: 30px; font-weight: 800; color: #FFE3B3; margin-top: 40px; }}
.statue {{ position: absolute; right: -250px; bottom: 0; width: 850px; z-index: 10; filter: drop-shadow(-20px 20px 30px rgba(0,0,0,0.6)); }}
.arrow-btn {{ display: inline-block; border: 3px solid #332200; border-radius: 8px; padding: 5px 15px; margin-top: 40px; align-self: center; font-weight: 900; font-size: 26px; color:#332200; }}
</style>
</head>
<body>
<div class="bg-text">ENERGIA<br>TEMPO<br>GUERRA</div>
<div class="card">
    <div class="text-main">
        Consumir conteúdo que você <strong>ACHA</strong><br>que está te evoluindo, é uma perda de
    </div>
    <div class="huge-text">energia, dinheiro e paz</div>
    <div class="small-desc">
        depois do boom das redes de formato curto, a cultura do "rolar tela" esconde uma guerra fria silenciosa (contra o seu foco)
    </div>
    <div class="orange-highlight">
        e você está lutando do lado errado...
    </div>
    <div class="arrow-btn">&gt;</div>
</div>
<img src="{img_warrior}" class="statue">
</body>
</html>"""

def generate_html_slide4():
    # Inserida a Mão fotorealista segurando o celular
    img_hand = "file:///" + os.path.abspath("C:/Users/Admin/.gemini/antigravity/brain/bb885d9d-17c4-480d-8b96-bc832cb3e051/mockup_hand_transparent.png").replace("\\", "/")
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
body {{ margin: 0; padding: 0; width: 1080px; height: 1080px; background-color: #111111; font-family: 'Inter', sans-serif; position: relative; overflow: hidden; }}
.light-glow {{ position: absolute; top: 0; left: 0; width: 1000px; height: 1000px; background: radial-gradient(circle at top left, rgba(252, 163, 17, 0.4) 0%, transparent 70%); z-index: 1; }}
.orange-bar {{ position: absolute; left: 0; top: 0; width: 20px; height: 100%; background-color: #FCA311; z-index: 2; }}
.content-area {{ position: absolute; top: 50%; left: 80px; transform: translateY(-50%); z-index: 10; width: 600px; }}
.main-quote {{ color: #FCA311; font-size: 55px; margin-top: 0; line-height: 1.25; font-weight: 700; letter-spacing: -2px; text-transform: uppercase; }}
.small-white {{ color: #FDF5E6; font-size: 30px; margin-top: 50px; font-weight: 500; letter-spacing: -1px; }}
.rotated-text {{ position: absolute; right: -50px; top: -100px; font-size: 32px; font-weight: 800; color: #FDF5E6; transform: rotate(15deg); line-height: 1.2; text-shadow: 0 0 20px rgba(255,255,255,0.4); }}
.arrow-btn {{ border: 3px solid #FDF5E6; border-radius: 8px; padding: 5px 15px; display: inline-block; margin-top: 40px; font-weight: 900; font-size: 24px; color:#FDF5E6; text-align:center; }}

/* Posicao do Render Fotorealista da Mao com Celular */
.hand-mockup {{ position: absolute; bottom: -50px; right: -50px; width: 550px; z-index: 10; filter: drop-shadow(-20px 20px 40px rgba(0,0,0,0.8)); }}

</style>
</head>
<body>
<div class="light-glow"></div>
<div class="orange-bar"></div>
<div class="content-area">
    <div class="rotated-text">seu tempo<br>não volta, tá?</div>
    <div class="main-quote">
        A dura verdade<br>é que você está entregando<br>sua vida de graça.
    </div>
    <div class="small-white">
        assuma o controle. a ferramenta existe para <strong>servir você</strong>,<br>e não o contrário.
        <br>
        <div class="arrow-btn">&gt;</div>
    </div>
</div>

<!-- A Arte Final 3D do Celular fica grudada no chao/base direita pra dar a sensacao tatil -->
<img src="{img_hand}" class="hand-mockup">
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

    os.makedirs("c:/Users/Admin/Desktop/Agente/outputs/carrossel_creata_v8", exist_ok=True)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1080, "height": 1080})
        
        await page.goto("file:///" + os.path.abspath("c:/Users/Admin/Desktop/Agente/execution/temp_slide1.html").replace("\\", "/"))
        await page.wait_for_timeout(2000)
        await page.screenshot(path="c:/Users/Admin/Desktop/Agente/outputs/carrossel_creata_v8/slide_01.png", type="png")
        
        await page.goto("file:///" + os.path.abspath("c:/Users/Admin/Desktop/Agente/execution/temp_slide2.html").replace("\\", "/"))
        await page.wait_for_timeout(2000)
        await page.screenshot(path="c:/Users/Admin/Desktop/Agente/outputs/carrossel_creata_v8/slide_02.png", type="png")
        
        await page.goto("file:///" + os.path.abspath("c:/Users/Admin/Desktop/Agente/execution/temp_slide3.html").replace("\\", "/"))
        await page.wait_for_timeout(2000)
        await page.screenshot(path="c:/Users/Admin/Desktop/Agente/outputs/carrossel_creata_v8/slide_03.png", type="png")
        
        await page.goto("file:///" + os.path.abspath("c:/Users/Admin/Desktop/Agente/execution/temp_slide4.html").replace("\\", "/"))
        await page.wait_for_timeout(2000)
        await page.screenshot(path="c:/Users/Admin/Desktop/Agente/outputs/carrossel_creata_v8/slide_04.png", type="png")
        
        await browser.close()
        
    print("✅ Carrossel Creata v8 gerado com sucesso!")

if __name__ == "__main__":
    asyncio.run(generate_all_images())

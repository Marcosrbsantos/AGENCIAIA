import asyncio
import os
import re
import json
import urllib.parse
import time
from dotenv import load_dotenv
from groq import AsyncGroq
import httpx

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

from supabase_config import supabase

async def upload_to_supabase_storage(file_path, filename):
    """Envia arquivo para o Supabase Storage (Bucket: agenciaia-designs)"""
    bucket_name = "agenciaia-designs"
    try:
        with open(file_path, 'rb') as f:
            # Upload do arquivo
            supabase.storage.from_(bucket_name).upload(
                path=filename,
                file=f,
                file_options={"content-type": "image/png"}
            )
        # Retorna a URL pública
        url = supabase.storage.from_(bucket_name).get_public_url(filename)
        return url
    except Exception as e:
        print(f"❌ Falha no Supabase Storage: {e}")
        # Tenta criar o bucket caso não exista (Pode falhar por falta de permissão, mas vale a tentativa)
        try:
            supabase.storage.create_bucket(bucket_name, options={"public": True})
        except:
            pass
    return None

def carregar_contexto(arquivo):
    """Lê um arquivo .md das referências"""
    caminho = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'referencias', arquivo)
    try:
        if os.path.exists(caminho):
            with open(caminho, 'r', encoding='utf-8') as f:
                return f.read()
    except Exception as e:
         print(f"Erro lendo {arquivo}: {e}")
    return "Nenhum modelo específico encontrado."

async def baixar_imagem(url, caminho):
    """Baixa imagem com headers de navegador"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(url, headers=headers, timeout=20.0)
            if response.status_code == 200:
                with open(caminho, 'wb') as f:
                    f.write(response.content)
                return True
    except Exception as e:
        print(f"Erro ao baixar imagem: {e}")
    return False

async def executar_logica_pesquisa(tema, tipo="Normal"):
    """Motor de pesquisa estratégica"""
    prompt = f"Realize uma pesquisa (Estilo: {tipo}) extremamente aprofundada, com viés estratégico e referências bibliográficas plausíveis sobre: {tema}."
    contexto_geral = carregar_contexto('modelos_roteiros.md')
    system_pesquisa = f"Especialista em Pesquisa e Neuroestética. Profundo, denso, revelador. Base de Pensamento Analítico:\n{contexto_geral}"
    
    client = AsyncGroq(api_key=GROQ_API_KEY)
    response = await client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": system_pesquisa}, {"role": "user", "content": prompt}],
        temperature=0.5, max_tokens=2500
    )
    return response.choices[0].message.content

async def executar_logica_copy(tema, formato, contexto_pesquisa):
    """Motor de roteirização e copy"""
    biblia_panorama = carregar_contexto('panorama_design_2026.md')
    modelos_copy = carregar_contexto('modelos_roteiros.md')
    system_base = f"Você é um Roteirista Copywriter brabo. Direto, minimalista, poderoso.\n\nBÍBLIA 2026:\n{biblia_panorama}\n\nExemplos:\n{modelos_copy}"
    
    prompt = f"Com base na pesquisa: {str(contexto_pesquisa)[:1500]}\n\nCrie uma copy visceral para {formato} sobre {tema}. Use neuroestética."
    
    client = AsyncGroq(api_key=GROQ_API_KEY)
    response = await client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": system_base}, {"role": "user", "content": prompt}],
        temperature=0.7, max_tokens=1500
    )
    return response.choices[0].message.content

async def gerar_prompt_visual(copy, formato):
    """Gera o prompt para IA de imagem - Otimizado para ser ULTRA CONCISO (Keywords Only)"""
    tokens_estetica = str(carregar_contexto('estetica_tokens.md'))[:1500]
    biblia_panorama = str(carregar_contexto('panorama_design_2026.md'))[:1500]
    
    system_design = f"Você é Diretor de Arte Premium. Use estes guias:\n{biblia_panorama}\nTokens:\n{tokens_estetica}"
    
    prompt_pedido = f"""
    Baseado nesta copy: {str(copy)[:300]}
    Formato: {formato}
    
    Crie um prompt visual técnico e curto (máximo 40 palavras). 
    Foque em: Sujeito, Estilo de Iluminação, Textura de Materiais, Qualidade 8k, Cinematic.
    Responda APENAS com o prompt em inglês para melhor resultado.
    """
    
    client = AsyncGroq(api_key=GROQ_API_KEY)
    response = await client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_design},
            {"role": "user", "content": prompt_pedido}
        ],
        temperature=0.5, max_tokens=150
    )
    return response.choices[0].message.content.strip()

BACKEND_URL = "http://localhost:8000"

async def render_screenshot_creata(html_content, output_path):
    """Renderiza HTML para PNG usando Playwright"""
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1080, "height": 1080})
        await page.set_content(html_content)
        await page.wait_for_timeout(1000) # Esperar fontes e glows
        await page.screenshot(path=output_path, type="png")
        await browser.close()
    return output_path

async def executar_logica_carrossel(tema, num_slides=5):
    """Gera carrossel estruturado com motor CREATA (Penpot Style)"""
    # 1. Planejar Conteúdo dos Slides via Groq
    prompt_plano = f"Crie um plano para um carrossel de {num_slides} slides sobre: {tema}. Para cada slide, dê um TÍTULO curto e uma DESCRIÇÃO impactante. Responda em JSON: [{{'titulo': '...', 'desc': '...'}}]"
    
    client = AsyncGroq(api_key=GROQ_API_KEY)
    chat_completion = await client.chat.completions.create(
        messages=[{"role": "user", "content": prompt_plano}],
        model="llama-3.3-70b-versatile",
        response_format={"type": "json_object"}
    )
    import json
    plano_data = json.loads(chat_completion.choices[0].message.content)
    slides_data = list(plano_data) if isinstance(plano_data, list) else list(plano_data.get('slides', []))

    # 2. Renderizar cada slide usando Template Premium
    template_path = os.path.join(os.path.dirname(__file__), "templates", "premium_dark.html")
    with open(template_path, "r", encoding="utf-8") as f:
        template_html = f.read()

    os.makedirs("outputs/carrossel_v11", exist_ok=True)
    slides_finais = []
    
    for i, slide in enumerate(slides_data[:num_slides]):
        # Customização do HTML
        html_custom = template_html.replace(
            "document.getElementById('main-title').innerText = title;",
            f"document.getElementById('main-title').innerText = {json.dumps(slide['titulo'])};"
        ).replace(
            "document.getElementById('main-desc').innerText = desc;",
            f"document.getElementById('main-desc').innerText = {json.dumps(slide['desc'])};"
        )
        
        filename = f"slide_{i+1}_{os.urandom(3).hex()}.png"
        output_path = os.path.join("outputs", "carrossel_v11", filename)
        await render_screenshot_creata(html_custom, output_path)
        
        # Cloud Storage: Upload para Supabase
        storage_url = await upload_to_supabase_storage(output_path, filename)
        final_url = storage_url if storage_url else f"{BACKEND_URL}/outputs/carrossel_v11/{filename}"
        
        slides_finais.append({
            "titulo": slide['titulo'],
            "url": final_url
        })
        
    return slides_finais

async def gerar_design_url(prompt_visual):
    """Gera Design Premium via motor Creata (Penpot Style) com Cloud Bridge"""
    output_dir = "outputs/design_mestre"
    os.makedirs(output_dir, exist_ok=True)
    filename = f"design_{os.urandom(4).hex()}.png"
    output_path = os.path.join(output_dir, filename)
    
    template_path = os.path.join(os.path.dirname(__file__), "templates", "premium_dark.html")
    with open(template_path, "r", encoding="utf-8") as f:
        html = f.read()
        
    prompt_str = str(prompt_visual)
    titulo = prompt_str[:50] + "..." if len(prompt_str) > 50 else prompt_str
    desc = "Arquitetura Visual Gerada pela Neural Engine AGENCIAIA V11."
    
    html = html.replace(
        "document.getElementById('main-title').innerText = title;",
        f"document.getElementById('main-title').innerText = {json.dumps(titulo)};"
    ).replace(
        "document.getElementById('main-desc').innerText = desc;",
        f"document.getElementById('main-desc').innerText = {json.dumps(desc)};"
    )
    
    await render_screenshot_creata(html, output_path)
    
    # Cloud Storage: Upload para Supabase
    storage_url = await upload_to_supabase_storage(output_path, filename)
    return storage_url if storage_url else f"{BACKEND_URL}/outputs/design_mestre/{filename}"

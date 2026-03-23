import asyncio
import os
import re
import random
import httpx
from dotenv import load_dotenv
from telegram import Update, InputMediaPhoto, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes, ConversationHandler
from playwright.async_api import async_playwright
from groq import AsyncGroq
import criador_carrossel_creata_v8 as motor_design

import json
import time

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "COLOQUE_SEU_TOKEN_AQUI")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MEMORIA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.tmp', 'memoria_copys.json')

def salvar_memoria(user_id: int, copy: str):
    """Persiste a última copy do usuário em arquivo JSON (sobrevive a reinicializações)"""
    os.makedirs(os.path.dirname(MEMORIA_PATH), exist_ok=True)
    dados = {}
    if os.path.exists(MEMORIA_PATH):
        try:
            with open(MEMORIA_PATH, 'r', encoding='utf-8') as f:
                dados = json.load(f)
        except Exception:
            dados = {}
    dados[str(user_id)] = copy
    with open(MEMORIA_PATH, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

def carregar_memoria(user_id: int) -> str | None:
    """Recupera a última copy salva para o usuário"""
    if os.path.exists(MEMORIA_PATH):
        try:
            with open(MEMORIA_PATH, 'r', encoding='utf-8') as f:
                dados = json.load(f)
            return dados.get(str(user_id))
        except Exception:
            pass
    return None

def aprender_modelo(content: str, tipo: str = "Geral"):
    """Salva um conteúdo (copy ou design) como modelo preferido do Mestre"""
    os.makedirs(os.path.dirname(MODELOS_PREFERIDOS_PATH), exist_ok=True)
    modelos = []
    if os.path.exists(MODELOS_PREFERIDOS_PATH):
        try:
            with open(MODELOS_PREFERIDOS_PATH, 'r', encoding='utf-8') as f:
                modelos = json.load(f)
        except Exception:
            modelos = []
            
    novo_modelo = {
        "data": time.strftime('%Y-%m-%d %H:%M:%S'),
        "tipo": tipo,
        "conteudo": content
    }
    modelos.append(novo_modelo)
    # Mantém apenas os últimos 20 modelos para não sobrecarregar o contexto
    if len(modelos) > 20: 
        novo_topo = len(modelos) - 20
        modelos = modelos[novo_topo:]
    
    with open(MODELOS_PREFERIDOS_PATH, 'w', encoding='utf-8') as f:
        json.dump(modelos, f, ensure_ascii=False, indent=2)
    return True

def registrar_performance(post_id, tema, tipo, estilo_copy):
    """Cria um registro inicial de performance para um novo post"""
    os.makedirs(os.path.dirname(PERFORMANCE_PATH), exist_ok=True)
    logs = []
    if os.path.exists(PERFORMANCE_PATH):
        try:
            with open(PERFORMANCE_PATH, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        except Exception:
            logs = []
    
    novo_log = {
        "post_id": post_id,
        "tema": tema,
        "tipo": tipo,
        "estilo_copy": estilo_copy,
        "resultado": {
            "likes": 0,
            "salvamentos": 0,
            "ctr": 0.0
        }
    }
    logs.append(novo_log)
    with open(PERFORMANCE_PATH, 'w', encoding='utf-8') as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)

def carregar_contexto(arquivo):
    """Lê um arquivo .md para injetar no cérebro da IA como diretiva de Sistema"""
    caminho = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'referencias', arquivo)
    try:
        if os.path.exists(caminho):
            with open(caminho, 'r', encoding='utf-8') as f:
                return f.read()
    except Exception as e:
         print(f"Erro lendo {arquivo}: {e}")
    return "Nenhum modelo específico encontrado."

async def baixar_imagem(url, caminho):
    """Baixa uma imagem da URL para um caminho local temporário com retentativas"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    for tentativa in range(2):
        try:
            async with httpx.AsyncClient(follow_redirects=True) as client:
                response = await client.get(url, headers=headers, timeout=httpx.Timeout(15.0, connect=10.0))
                if response.status_code == 200:
                    with open(caminho, 'wb') as f:
                        f.write(response.content)
                    return True
                else:
                    print(f"Erro HTTP {response.status_code} na tentativa {tentativa+1}")
        except Exception as e:
            print(f"Erro ao baixar imagem (tentativa {tentativa+1}): {e}")
            await asyncio.sleep(1)
    return False

async def renderizar_post_layout(titulo, descricao, caminho_saida, template="premium_dark", tag="CREATA IA V10"):
    """Renderiza um post via subprocesso isolado (evita conflito com event loop do Telegram)"""
    script_path = os.path.join(os.path.dirname(__file__), 'render_post.py')
    try:
        os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
        titulo_safe = titulo.replace("'", " ").replace('"', ' ')[:80]
        descricao_safe = descricao.replace("'", " ").replace('"', ' ')[:200]
        tag_safe = tag.replace("'", " ").replace('"', ' ')[:50]
        
        proc = await asyncio.create_subprocess_exec(
            'python', script_path, titulo_safe, descricao_safe, caminho_saida, template, tag_safe,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=60.0)
        if proc.returncode == 0 and os.path.exists(caminho_saida):
            print(f"Playwright OK: {stdout.decode().strip()}")
            return True
        else:
            print(f"Playwright erro: {stderr.decode().strip()}")
            return False
    except asyncio.TimeoutError:
        print("Playwright subprocess timeout")
        return False
    except Exception as e:
        print(f"Erro subprocess: {e}")
        return False

PERFORMANCE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.tmp', 'performance_log.json')
MODELOS_PREFERIDOS_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.tmp', 'modelos_preferidos.json')

# Importar o novo Estrategista
from agente_estrategista_v10 import estrategista

# Estados da Máquina de Conversação
ESCOLHENDO_FORMATO_COPY, RECEBENDO_TEMA_COPY = range(2)
ESCOLHENDO_FORMATO_DESIGN, RECEBENDO_TEMA_DESIGN, ESCOLHENDO_ORIGEM_COPY = range(2, 5)
ESCOLHENDO_TIPO_PESQUISA, RECEBENDO_TEMA_PESQUISA = range(5, 7)
RECEBENDO_TEMA_PESQUISA_CHAIN = 7

# NOVO ESTADO V10
RECEBENDO_TEMA_ESTRATEGIA, ESCOLHENDO_OBJETIVO_ESTRATEGIA, ESCOLHENDO_PLATAFORMA_ESTRATEGIA = range(8, 11)
RECEBENDO_ID_FEEDBACK, RECEBENDO_METRICAS_FEEDBACK = range(11, 13)
RECEBENDO_TEMA_INSANO = 13

async def set_menu_commands(app: Application):
    """Seta o autocomplete nativo do Telegram (barra flutuante)"""
    commands = [
        ("estrategia", "🎯 Cérebro V10 - Campanha Completa"),
        ("copy", "Roteirista - Gera textos magnéticos"),
        ("design", "Designer - Cria arte gráfica"),
        ("pesquisa", "Investigador - Pesquisas avançadas"),
        ("carrossel", "Renderiza o HTML V8 em Nuvem"),
        ("radar", "Mostra tendências do nicho"),
        ("feedback", "📈 Enviar resultados de performance"),
        ("modo_insano", "🔥 3 variações completas de uma vez")
    ]
    await app.bot.set_my_commands(commands)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Boas-vindas"""
    await update.message.reply_text(
        f"🏛️ Salve, Mestre!\n\nEu sou o Arquiteto Vivo v3.0, com Menu Interativo.\n"
        "Meus Oito Agentes estão prontos.\n\n👉 Digite / ou selecione abaixo o seu Comando Especialista."
    )

# --- FLUXO 1: COPY ---
async def copy_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Carrossel", callback_data="copy_carrossel"),
         InlineKeyboardButton("Post Estático", callback_data="copy_estatico")],
        [InlineKeyboardButton("Vídeo", callback_data="copy_video"),
         InlineKeyboardButton("Email", callback_data="copy_email")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("✍️ Agente Roteirista na escuta! Pra qual formato escreveremos hoje, Mestre?", reply_markup=reply_markup)
    return ESCOLHENDO_FORMATO_COPY

# --- FLUXO V10: ESTRATÉGIA ---
async def estrategia_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎯 **Cérebro V10 Ativado.**\n\nMestre, qual o TEMA central da campanha que iremos forjar?")
    return RECEBENDO_TEMA_ESTRATEGIA

async def estrategia_receber_tema(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["estrategia_tema"] = update.message.text
    keyboard = [
        [InlineKeyboardButton("💰 Gerar Leads/Venda", callback_data="obj_venda"),
         InlineKeyboardButton("🚀 Engajamento/Viral", callback_data="obj_engajamento")],
        [InlineKeyboardButton("🏛️ Autoridade/Educar", callback_data="obj_autoridade")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🎯 Qual o **OBJETIVO REAL** desta ação?", reply_markup=reply_markup)
    return ESCOLHENDO_OBJETIVO_ESTRATEGIA

async def estrategia_objetivo_escolhido(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["estrategia_objetivo"] = query.data.replace("obj_", "")
    
    keyboard = [
        [InlineKeyboardButton("📸 Instagram", callback_data="plat_instagram"),
         InlineKeyboardButton("💼 LinkedIn", callback_data="plat_linkedin")],
        [InlineKeyboardButton("🎥 TikTok/YouTube", callback_data="plat_tiktok")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="📱 Em qual **PLATAFORMA** iremos dominar hoje?", reply_markup=reply_markup)
    return ESCOLHENDO_PLATAFORMA_ESTRATEGIA

async def estrategia_finalizar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    plataforma = query.data.replace("plat_", "")
    tema = context.user_data.get("estrategia_tema")
    objetivo = context.user_data.get("estrategia_objetivo")
    
    msg = await query.edit_message_text(text=f"🧠 **Arquiteto de Retenção processando...**\nTema: {tema}\nPlataforma: {plataforma}")
    
    # 1. GERAR ESTRATÉGIA
    await msg.edit_text("🧠 **Fase 1: O Cérebro**\nAnalisando psicologia de consumo e regras de funil...")
    est_data = await estrategista.definir_estrategia(tema, objetivo, plataforma)
    context.user_data["estrategia_ativa"] = est_data
    
    res_est = (
        f"✅ **Estratégia Forjada:**\n"
        f"👤 **Persona:** {est_data['persona']}\n"
        f"📊 **Funil:** {est_data['fase_funil']}\n"
        f"🎯 **Ângulo:** {est_data['angulo']}\n"
        f"🔥 **Gancho:** {est_data['gancho']}\n"
        f"🚀 **CTA:** {est_data['cta']}\n\n"
        f"⛓️ **Corrente de Agentes Iniciada...**"
    )
    await msg.edit_text(res_est)
    
    # Inicia a corrente automática
    await campanha_completa_chain(update, context, tema, est_data, plataforma, msg)
    return ConversationHandler.END

async def campanha_completa_chain(update, context, tema, est_data, plataforma, msg_status):
    # 2. PESQUISA
    await msg_status.edit_text(f"{msg_status.text}\n\n🔎 **Fase 2: O Investigador**\nEscavando insights profundos sobre '{tema}'...")
    pesquisa_resultado = await executar_logica_pesquisa(tema, "Rápida")
    
    # 3. COPY (Adaptada por plataforma)
    await msg_status.edit_text(f"{msg_status.text}\n\n✍️ **Fase 3: O Roteirista**\nCustomizando tom de voz para {plataforma}...")
    
    # Contexto V10 para a Copy
    prompt_copy = f"ESTRATÉGIA: {est_data['angulo']}. GANCHO: {est_data['gancho']}. CTA: {est_data['cta']}. PLATAFORMA: {plataforma}."
    copy_resultado = await executar_logica_copy(tema, est_data['tipo_conteudo'], f"{pesquisa_resultado}\n\n{prompt_copy}")
    
    salvar_memoria(update.effective_user.id, copy_resultado)
    
    # 4. DESIGN
    await msg_status.edit_text(f"{msg_status.text}\n\n🎨 **Fase 4: O Designer**\nForjando estética premium...")
    await design_executar_fluxo(update, context, est_data['tipo_conteudo'], copy_resultado, msg_status=msg_status)
async def copy_formato_escolhido(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    formato = query.data.replace("copy_", "").capitalize()
    context.user_data["copy_formato"] = formato
    await query.edit_message_text(text=f"📜 Formato escolhido: **{formato}**.\n\nSobre qual TEMA devemos escrever hoje, Mestre?")
    return RECEBENDO_TEMA_COPY

async def copy_gerar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tema = update.message.text
    formato = context.user_data.get("copy_formato", "Texto")
    msg = await update.message.reply_text(f"🧠 Roteirizando {formato} sobre '{tema}' usando LLaMA 3.3 70B...")
    
    if not GROQ_API_KEY:
         await msg.edit_text("⚠️ Groq API ausente.")
         return ConversationHandler.END
         
    prompt = f"Crie um roteiro/copy fenomenal (formato: {formato}) sobre o tema: {tema}. Use neuroestética e foco incisivo."
    
    try:
        modelos_copy = carregar_contexto('modelos_roteiros.md')
        biblia_panorama = carregar_contexto('panorama_design_2026.md')
        system_base = f"Você é um Roteirista Copywriter brabo, direto. Minimalista, poderoso.\n\nModele os roteiros baseado no Guia Mestre e Estruturas AIDA/PAS abaixo:\n{biblia_panorama}\n\nExemplos de Roteiros:\n{modelos_copy}"
        
        client = AsyncGroq(api_key=GROQ_API_KEY)
        response = await client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_base},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7, max_tokens=1500
        )
        
        copy_final = response.choices[0].message.content
        # Salva em JSON persistente (sobrevive reinicializações do bot)
        salvar_memoria(update.effective_user.id, copy_final)
        context.user_data["ultima_copy"] = copy_final  # mantém também em memória local
        
        await msg.edit_text(f"{copy_final}\n\n*Nota: O Mestre pode gerar a arte digitando /design agora, pois eu lembro desta Copy!*")
        
    except Exception as e:
        await msg.edit_text(f"🔥 Erro no Groq: {e}")
        
    return ConversationHandler.END

# --- FLUXO 2: DESIGN ---
async def design_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Post Estático Ouro", callback_data="design_estatico"),
         InlineKeyboardButton("Produto Comercial", callback_data="design_produto")],
        [InlineKeyboardButton("Story Vertical", callback_data="design_story")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🎨 Diretor de Arte puxando a prancheta.\nQual Formato visual exigiremos das APIs Gráficas?", reply_markup=reply_markup)
    return ESCOLHENDO_FORMATO_DESIGN

async def design_formato_escolhido(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    formato = query.data.replace("design_", "").capitalize()
    
    # Recupera a memória da copy
    user_id = update.effective_user.id if update.effective_user else 0
    memoria_copy = context.user_data.get("ultima_copy") or carregar_memoria(user_id)
    
    if memoria_copy:
         await query.edit_message_text(text=f"🖼️ Formato visual: **{formato}**.\n\nMestre, puxei da minha Memória Neural a Copy da gaveta anterior!\n⏱️ Lendo a Biblioteca `estetica_tokens.md` para emular suas referências visuais...")
         return await design_executar_fluxo(update, context, formato, memoria_copy)
    else:
         keyboard = [
             [InlineKeyboardButton("🔍 Pesquisar Agora", callback_data="origem_pesquisa"),
              InlineKeyboardButton("✍️ Digitar Copy", callback_data="origem_manual")]
         ]
         reply_markup = InlineKeyboardMarkup(keyboard)
         await query.edit_message_text(text=f"🖼️ Formato visual: **{formato}**.\nMestre, minha memória de Roteirista está vazia...\nDeseja que eu **pesquise** um assunto para criar a copy ou você já tem o texto?", reply_markup=reply_markup)
         context.user_data["design_formato"] = formato
         return ESCOLHENDO_ORIGEM_COPY

async def design_origem_escolhida(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    origem = query.data
    formato = context.user_data.get("design_formato", "Post")

    if origem == "origem_pesquisa":
        await query.edit_message_text(text="🔬 **Corrente de Agentes Ativada.**\nQual ASSUNTO devemos pesquisar para fundamentar sua Arte?")
        return RECEBENDO_TEMA_PESQUISA_CHAIN
    else:
        await query.edit_message_text(text=f"✍️ Perfeito. Digite abaixo a Copy ou a Ideia que você quer no seu **{formato}**:")
        return RECEBENDO_TEMA_DESIGN

async def design_chain_trigger(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tema = update.message.text
    formato = context.user_data.get("design_formato", "Post")
    msg = await update.message.reply_text(f"⛓️ **Iniciando Corrente de Agentes...**\n\n1. 🔬 Pesquisando sobre '{tema}'...")
    
    # 1. PESQUISA
    pesquisa_resultado = await executar_logica_pesquisa(tema, "Rápida")
    await msg.edit_text(f"⛓️ **Corrente de Agentes...**\n\n1. ✅ Pesquisa concluída.\n2. ✍️ Criando Copy estratégica...")
    
    # 2. COPY
    copy_resultado = await executar_logica_copy(tema, formato, pesquisa_resultado)
    user_id = update.effective_user.id
    salvar_memoria(user_id, copy_resultado)
    
    await msg.edit_text(f"⛓️ **Corrente de Agentes...**\n\n1. ✅ Pesquisa concluída.\n2. ✅ Copy masterizada.\n3. 🎨 Forjando Design Premium...")
    
    # 3. DESIGN
    await design_executar_fluxo(update, context, formato, copy_resultado, msg_status=msg)
    return ConversationHandler.END

async def executar_logica_pesquisa(tema, tipo):
    prompt = f"Realize uma pesquisa (Estilo: {tipo}) extremamente aprofundada sobre: {tema}. Foco em insights estratégicos para design."
    client = AsyncGroq(api_key=GROQ_API_KEY)
    response = await client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": "Especialista em Pesquisa Digital."}, {"role": "user", "content": prompt}],
        temperature=0.5, max_tokens=1500
    )
    return response.choices[0].message.content

async def executar_logica_copy(tema, formato, contexto_pesquisa):
    prompt = f"Com base na pesquisa: {contexto_pesquisa[:2000]}\n\nCrie uma copy visceral para {formato} sobre {tema}."
    client = AsyncGroq(api_key=GROQ_API_KEY)
    response = await client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": "Copywriter de Elite."}, {"role": "user", "content": prompt}],
        temperature=0.7, max_tokens=1000
    )
    return response.choices[0].message.content

async def design_executar_fluxo(update, context, formato, memoria_copy, msg_status=None):
    try:
         tokens_estetica = carregar_contexto('estetica_tokens.md')[:2000]
         biblia_panorama = carregar_contexto('panorama_design_2026.md')[:2000]
         system_design = (
             "Você é o Diretor de Arte da Agência Creata. Sua missão é ler as diretrizes estéticas abaixo e ESCOLHER o 'Módulo' ou 'Paleta' mais adequado para o tema.\n\n"
             f"BIBLIOTECA DE REFERÊNCIAS:\n{tokens_estetica}\n\n"
             f"BÍBLIA DE DESIGN 2026:\n{biblia_panorama}\n\n"
             "INSTRUÇÃO: Identifique o estilo (ex: Anatomia do Marketing, Solar Clean, etc) que melhor se encaixa na Copy e descreva um prompt visual curto para a IA. FOCO EM PREMIUM AESTHETICS."
         )
         
         client = AsyncGroq(api_key=GROQ_API_KEY)
         groq_response = await asyncio.wait_for(
             client.chat.completions.create(
                 model="llama-3.3-70b-versatile",
                 messages=[
                     {"role": "system", "content": system_design},
                     {"role": "user", "content": f"A Copy é: {str(memoria_copy)[:400]}. Formato: {formato}. Resuma o estilo escolhido e descreva o prompt em 1 parágrafo."}
                 ],
                 temperature=0.6, max_tokens=600
             ),
             timeout=60.0
         )
         
         descricao_arte = groq_response.choices[0].message.content
         import urllib.parse
         import time
         
         # Geração de Post ID V10
         post_id = f"POST_{time.strftime('%Y%m%d_%H%M%S')}"
         tema_log = context.user_data.get("estrategia_tema") or "Tema Manual"
         registrar_performance(post_id, tema_log, formato, "V10_Padrao")
         
         resolucao = "width=1080&height=1080"
         
         prompt_base = f"Professional ad design, premium aesthetics 2026, {descricao_arte}"
         prompt_sanitizado = re.sub(r'[^a-zA-Z0-9\s,]', '', prompt_base)[:600]
         url_imagem = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt_sanitizado)}?{resolucao}&nologo=true&seed=42"
         
         status_text = f"🚀 **Escopo Visual Masterizado:**\nID: `{post_id}`\n\n{descricao_arte}\n\n⏳ Renderizando Pixels..."
         if msg_status:
             await msg_status.edit_text(status_text)
         else:
             await context.bot.send_message(chat_id=update.effective_chat.id, text=status_text)
         
         path_temp = os.path.join(os.getcwd(), "outputs", f"temp_design_{update.effective_chat.id}.png")
         os.makedirs(os.path.dirname(path_temp), exist_ok=True)
         
         sucesso = False
         try:
             sucesso = await asyncio.wait_for(baixar_imagem(url_imagem, path_temp), timeout=45.0)
         except asyncio.TimeoutError:
             print("Timeout na IA de imagem, ativando Playwright...")
             # Extração de parâmetros de design V10
             estrategia_completa = context.user_data.get("estrategia_completa", {})
             template_escolhido = estrategia_completa.get("template", "premium_dark")
             tag_personalizada = estrategia_completa.get("tag", "CREATA IA V10")
             
             if not sucesso:
                 if msg_status: await msg_status.edit_text("⚠️ IA externa instável. Ativando Motor Local...")
                 else: await context.bot.send_message(chat_id=update.effective_chat.id, text="⚠️ IA externa instável. Ativando Motor Local...")
                 
                 titulo_fallback = memoria_copy[:60] if memoria_copy else "Design Creata"
                 # Passando template e tag para o renderizador local
                 sucesso = await renderizar_post_layout(titulo_fallback, descricao_arte[:250], path_temp, template_escolhido, tag_personalizada)
 
         if sucesso:
             with open(path_temp, 'rb') as photo:
                 await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo, caption=f"✨ Sua arte masterizada está pronta!\nID do Post: `{post_id}`")
             if not msg_status: os.remove(path_temp)
         else:
             await context.bot.send_message(chat_id=update.effective_chat.id, text="❌ Falha crítica na renderização.")
         
    except Exception as e:
         await context.bot.send_message(chat_id=update.effective_chat.id, text=f"🔥 Erro no fluxo de design: {e}")
    
    return ConversationHandler.END

async def design_receber_tema_sujo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tema_manual = update.message.text
    formato = context.user_data.get("design_formato_sujo", "Post Estatico")
    await update.message.reply_text(f"⏱️ O Mestre digitou o Tema: '{tema_manual}' para um {formato}.\nLendo Biblioteca Ouro `estetica_tokens.md`...")
    
    try:
        tokens_estetica = carregar_contexto('estetica_tokens.md')[:2000]
        biblia_panorama = carregar_contexto('panorama_design_2026.md')[:2000]
        system_design = f"Você é o Diretor de Arte do Telegram. Crie um prompt visual cirurgico baseado nos guias 2026:\n\n{biblia_panorama}\n\nTokens:\n{tokens_estetica}"
        
        client = AsyncGroq(api_key=GROQ_API_KEY)
        groq_response = await asyncio.wait_for(
            client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_design},
                    {"role": "user", "content": f"Descreva o prompt visual para: {tema_manual[:300]}. Responda em 1 parágrafo curto."}
                ],
                temperature=0.6, max_tokens=600
            ),
            timeout=60.0
        )
        
        descricao_arte = groq_response.choices[0].message.content
        import urllib.parse
        resolucao = "width=1080&height=1080"
        
        # Sanitização Pesada do Prompt
        prompt_base = f"Professional ad design, {descricao_arte}"
        prompt_sanitizado = re.sub(r'[^a-zA-Z0-9\s,]', '', prompt_base)[:600]
        url_imagem = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt_sanitizado)}?{resolucao}&nologo=true&seed=42"
        
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"🚀 **Escopo Visual Masterizado:**\n\n{descricao_arte}\n\n⏳ Renderizando Pixels na Nuvem e baixando para o servidor...")
        
        # Caminho temporário para a imagem
        path_temp = os.path.join(os.getcwd(), "outputs", f"temp_design_manual_{update.effective_chat.id}.png")
        os.makedirs(os.path.dirname(path_temp), exist_ok=True)
        
        sucesso = False
        try:
            sucesso = await asyncio.wait_for(baixar_imagem(url_imagem, path_temp), timeout=45.0)
        except asyncio.TimeoutError:
            print("Timeout na IA de imagem, ativando Playwright...")

        if not sucesso:
            # FALLBACK: Renderização Local com Playwright
            await context.bot.send_message(chat_id=update.effective_chat.id, text="⚠️ Servidor de IA instável. Ativando Motor de Design Local...")
            titulo_fallback = tema_manual[:60] if tema_manual else "Post de Design Masterizado"
            sucesso = await renderizar_post_layout(titulo_fallback, descricao_arte[:250], path_temp)

        if sucesso:
            with open(path_temp, 'rb') as photo:
                await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo, caption="✨ Sua arte masterizada está pronta!")
            os.remove(path_temp)
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="❌ Falha crítica na renderização (IA e Local). Tente um tema mais simples.")
        
    except Exception as e:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"🔥 Erro ao forjar Arte Livre: {e}")
        
    return ConversationHandler.END
    
# --- FLUXO 3: PESQUISA ---
async def pesquisa_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
     keyboard = [
         [InlineKeyboardButton("Pesquisa Avançada", callback_data="pesq_avancada"),
          InlineKeyboardButton("Pesquisa Rápida", callback_data="pesq_rapida")],
         [InlineKeyboardButton("Deep YouTube", callback_data="pesq_youtube")]
     ]
     reply_markup = InlineKeyboardMarkup(keyboard)
     await update.message.reply_text("🔬 Investigador Principal ativo.\nMestre, qual a profundidade e fonte do Sonar de dados de hoje?", reply_markup=reply_markup)
     return ESCOLHENDO_TIPO_PESQUISA

async def pesquisa_tipo_escolhido(update: Update, context: ContextTypes.DEFAULT_TYPE):
     query = update.callback_query
     await query.answer()
     tipo = query.data.replace("pesq_", "").capitalize()
     context.user_data["tipo_pesquisa"] = tipo
     await query.edit_message_text(text=f"📊 Radar calibrado para: **{tipo}**.\nMestre, digite no chat qual o ASSUNTO CIENTÍFICO queremos devorar:")
     return RECEBENDO_TEMA_PESQUISA
     
async def pesquisa_gerar(update: Update, context: ContextTypes.DEFAULT_TYPE):
     tema = update.message.text
     tipo = context.user_data.get("tipo_pesquisa", "Normal")
     msg = await update.message.reply_text(f"🧠 Escavando a nuvem no modo {tipo} sobre: '{tema}'...")
     
     if not GROQ_API_KEY:
         await msg.edit_text("Sem Groq API.")
         return ConversationHandler.END
         
     prompt = f"Realize uma pesquisa (Estilo: {tipo}) extremamente aprofundada, com viés estratégico e referências bibliográficas plausíveis sobre: {tema}."
     
     try:
          contexto_geral = carregar_contexto('modelos_roteiros.md')
          system_pesquisa = f"Especialista em Pesquisa e Neuroestética. Profundo, denso, revelador. Base de Pensamento Analítico:\n{contexto_geral}"
          
          client = AsyncGroq(api_key=GROQ_API_KEY)
          response = await client.chat.completions.create(
                 model="llama-3.3-70b-versatile",
                 messages=[{"role": "system", "content": system_pesquisa}, {"role": "user", "content": prompt}],
                 temperature=0.5, max_tokens=2500
          )
          peso = response.choices[0].message.content
     except Exception as e:
          await msg.edit_text(f"🔥 Erro na Groq API: {e}")
          return ConversationHandler.END
     
     if len(peso) > 4000:
          await msg.delete()
          for i in range(0, len(peso), 4000):
               await update.message.reply_text(peso[i:i+4000])
     else:
          await msg.edit_text(peso)
          
     return ConversationHandler.END

# --- CAROSSEL LEGADO V8 ---
async def cmd_carrossel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text("⏱️ Ligando o motor Playwright no Servidor (V8 Real)...")
    try:
        await motor_design.generate_all_images()
        await msg.edit_text("✅ Arte do Carrossel V8 Renderizada. Compactando para envio...")
        
        caminho_base = "c:/Users/Admin/Desktop/Agente/outputs/carrossel_creata_v8"
        if not os.path.exists(caminho_base): caminho_base = "/app/outputs/carrossel_creata_v8"
             
        fotos = [os.path.join(caminho_base, f"slide_0{i}.png") for i in range(1, 5)]
        media_group = [InputMediaPhoto(media=open(f, 'rb')) for f in fotos if os.path.exists(f)]
                
        if media_group:
            await update.message.reply_media_group(media=media_group)
            await update.message.reply_text("🍷 Padrão Ouro entregue.")
        else:
             await msg.edit_text("❌ Falha crítica: Imagens não encontradas.")
    except Exception as e:
        await msg.edit_text(f"🔥 Erro Render: {e}")

# --- FLUXO V10: FEEDBACK ---
async def feedback_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📈 **Radar de Performance Ativado.**\n\nPor favor, informe o **ID do Post** (ex: `POST_20240317_1530`) para registrarmos os resultados:")
    return RECEBENDO_ID_FEEDBACK

async def feedback_receber_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    post_id = update.message.text.upper().strip()
    
    # Validação Básica
    if not os.path.exists(PERFORMANCE_PATH):
        await update.message.reply_text("❌ Nenhum log de performance encontrado ainda.")
        return ConversationHandler.END
        
    context.user_data["feedback_post_id"] = post_id
    await update.message.reply_text(f"✅ ID `{post_id}` localizado.\n\nAgora, Mestre, informe as métricas separadas por espaço:\n`CURTIDAS SALVAMENTOS CTR` (ex: `120 45 3.5`)")
    return RECEBENDO_METRICAS_FEEDBACK

async def feedback_receber_metricas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        dados = update.message.text.replace(",", ".").split()
        if len(dados) < 3:
            await update.message.reply_text("⚠️ Mestre, preciso de 3 valores: Curtidas, Salvamentos e CTR. Tente novamente:")
            return RECEBENDO_METRICAS_FEEDBACK
            
        likes = int(dados[0])
        salvamentos = int(dados[1])
        ctr = float(dados[2])
        
        post_id = context.user_data.get("feedback_post_id")
        
        # Atualiza o JSON
        with open(PERFORMANCE_PATH, 'r', encoding='utf-8') as f:
            logs = json.load(f)
            
        encontrado = False
        for log in logs:
            if log["post_id"] == post_id:
                log["resultado"] = {
                    "likes": likes,
                    "salvamentos": salvamentos,
                    "ctr": ctr
                }
                encontrado = True
                break
        
        if not encontrado:
            await update.message.reply_text(f"❌ Post ID `{post_id}` não encontrado no banco de dados.")
            return ConversationHandler.END
            
        with open(PERFORMANCE_PATH, 'w', encoding='utf-8') as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)
            
        await update.message.reply_text(f"🚀 **Performance Registrada!**\n\nID: `{post_id}`\n❤️ Likes: {likes}\n💾 Salvamentos: {salvamentos}\n📈 CTR: {ctr}%\n\nO Agente Estrategista acaba de absorver esse conhecimento.")
        
    except Exception as e:
        await update.message.reply_text(f"🔥 Erro ao processar métricas: {e}. Tente novamente:")
        return RECEBENDO_METRICAS_FEEDBACK
        
    return ConversationHandler.END

async def cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE):
     await update.message.reply_text("🚫 Operação Abortada, Mestre.")
     return ConversationHandler.END

async def modo_insano_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔥 **MODO INSANO ATIVADO.**\n\nNeste modo, o Arquiteto irá gerar **3 VARIAÇÕES COMPLETAS** (Pesquisa + Copy + Design) para o seu tema.\n\nMestre, qual o **TEMA EXPLOSIVO** de hoje?")
    return RECEBENDO_TEMA_INSANO

async def modo_insano_receber_tema(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tema = update.message.text
    chat_id = update.effective_chat.id
    plataforma = "Instagram"
    
    msg_aviso = await update.message.reply_text(f"⚡ **Iniciando Processamento em Massa...**\nTema: `{tema}`\n\nIsso pode levar alguns minutos. Sentem-se e apreciem o show.")
    
    try:
        # 1. Gera 3 Estratégias
        await msg_aviso.edit_text("🧠 Concedendo 3 visões estratégicas distintas...")
        variacoes = await estrategista.definir_variacoes(tema, plataforma)
        
        if not variacoes:
            await update.message.reply_text("❌ O Mestre da Estratégia falhou em gerar variações.")
            return ConversationHandler.END
            
        for i, est in enumerate(variacoes, 1):
            await update.message.reply_text(f"🌀 **FORJANDO VARIAÇÃO {i}/3: {est.get('angulo', 'Abordagem Única')}**")
            
            # 2. Pesquisa e Copy em um só passo para agilizar
            client = AsyncGroq(api_key=GROQ_API_KEY)
            prompt_copy = f"Baseado nesta estratégia: {json.dumps(est)}. Gere uma COPY COMPLETA E PERSUASIVA para um post de {plataforma}."
            
            r = await client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": "Roteirista Senior. Gere apenas a COPY final."}, {"role": "user", "content": prompt_copy}],
                temperature=0.7
            )
            copy_final = r.choices[0].message.content
            
            # Salva na memória para o designer e para o usuário
            salvar_memoria(chat_id, copy_final)
            await update.message.reply_text(f"📝 **Copy {i} Gerada:**\n\n{copy_final[:500]}...")
            
            # 3. Design Chain
            context.user_data["estrategia_completa"] = est
            await design_executar_fluxo(update, context, est.get("tipo_conteudo", "Post Estatico"), copy_final)
            
        await update.message.reply_text("✅ **PROCESSO INSANO CONCLUÍDO.**\nAs 3 variações foram forjadas e entregues, Mestre.")

    except Exception as e:
        await update.message.reply_text(f"💥 Explosão no Modo Insano: {e}")
        
    return ConversationHandler.END

# Cérebro Genérico Se Fora de Comando
async def handle_text_generico(update: Update, context: ContextTypes.DEFAULT_TYPE):
     texto_usuario = update.message.text.lower()
     
     # GATILHO DE APRENDIZADO
     gatilhos = ["aprenda", "grave", "adicione como modelo", "modelo", "salve esse", "aprenda esse"]
     if any(g in texto_usuario for g in gatilhos):
          ultima_copy = context.user_data.get("ultima_copy") or carregar_memoria(update.effective_user.id)
          ultima_est = context.user_data.get("estrategia_ativa")
          
          if ultima_copy or ultima_est:
               content_to_learn = f"ESTRATEGIA: {json.dumps(ultima_est)}\nCOPY: {ultima_copy}"
               aprender_modelo(content_to_learn, "Preferência do Mestre")
               await update.message.reply_text("✨ **Conhecimento Absorvido.**\n\nEntendi o padrão, Mestre. Salvei este estilo na minha Biblioteca de Padrões Preferidos e usarei como base para nossas próximas criações.")
               return
          else:
               await update.message.reply_text("⚠️ Mestre, não encontrei nenhum conteúdo recente na minha memória imediata para aprender.")
               return

     msg = await update.message.reply_text("🧠 O Arquiteto captou a ordem livre no ar...")
     
     if not GROQ_API_KEY:
         await msg.edit_text("⚠️ Groq API ausente.")
         return
         
     try:
         regras = carregar_contexto('modelos_roteiros.md')
         visual_tokens = carregar_contexto('estetica_tokens.md')
         biblia_panorama = carregar_contexto('panorama_design_2026.md')
         
         super_system = f"Você é a Cérebro Mestre da Agência Creata. Aja cirurgicamente dominando a BÍBLIA MESTRE DE 2026:\n\n{biblia_panorama}\n\nParâmetros Textuais adicionais:\n{regras}\n\nParâmetros Visuais de Design Ouro:\n{visual_tokens}"
         
         client = AsyncGroq(api_key=GROQ_API_KEY)
         r = await client.chat.completions.create(
             model="llama-3.3-70b-versatile", 
             messages=[
                 {"role": "system", "content": super_system}, 
                 {"role": "user", "content": update.message.text}
             ],
             temperature=0.7, max_tokens=2048
         )
         
         t = r.choices[0].message.content
         if len(t) > 4000:
              await msg.delete()
              for i in range(0, len(t), 4000):
                   await update.message.reply_text(t[i:i+4000])
         else:
              await msg.edit_text(t)
              
     except Exception as e:
         await msg.edit_text(f"🔥 Falha Cognitiva: {e}")

def main():
    if TOKEN == "COLOQUE_SEU_TOKEN_AQUI":
        print("⚠️ AVISO: Configure o TELEGRAM_BOT_TOKEN")
        
    app = Application.builder().token(TOKEN).post_init(set_menu_commands).build()

    # Registra o Fluxo do /copy
    conv_copy = ConversationHandler(
        entry_points=[CommandHandler('copy', copy_start)],
        states={
            ESCOLHENDO_FORMATO_COPY: [CallbackQueryHandler(copy_formato_escolhido, pattern="^copy_")],
            RECEBENDO_TEMA_COPY: [MessageHandler(filters.TEXT & ~filters.COMMAND, copy_gerar)]
        },
        fallbacks=[CommandHandler('cancelar', cancelar)],
        allow_reentry=True
    )
    
    # Registra o Fluxo do /design
    conv_design = ConversationHandler(
        entry_points=[CommandHandler('design', design_start)],
        states={
            ESCOLHENDO_FORMATO_DESIGN: [CallbackQueryHandler(design_formato_escolhido, pattern="^design_")],
            ESCOLHENDO_ORIGEM_COPY: [CallbackQueryHandler(design_origem_escolhida, pattern="^origem_")],
            RECEBENDO_TEMA_DESIGN: [MessageHandler(filters.TEXT & ~filters.COMMAND, design_receber_tema_sujo)],
            RECEBENDO_TEMA_PESQUISA_CHAIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, design_chain_trigger)]
        },
        fallbacks=[CommandHandler('cancelar', cancelar)],
        allow_reentry=True
    )

    # Registra o Fluxo do /pesquisa
    conv_pesq = ConversationHandler(
        entry_points=[CommandHandler('pesquisa', pesquisa_start)],
        states={
            ESCOLHENDO_TIPO_PESQUISA: [CallbackQueryHandler(pesquisa_tipo_escolhido, pattern="^pesq_")],
            RECEBENDO_TEMA_PESQUISA: [MessageHandler(filters.TEXT & ~filters.COMMAND, pesquisa_gerar)]
        },
        fallbacks=[CommandHandler('cancelar', cancelar)],
        allow_reentry=True
    )

    # Registra o Fluxo do /estrategia (V10)
    conv_est = ConversationHandler(
        entry_points=[CommandHandler('estrategia', estrategia_start)],
        states={
            RECEBENDO_TEMA_ESTRATEGIA: [MessageHandler(filters.TEXT & ~filters.COMMAND, estrategia_receber_tema)],
            ESCOLHENDO_OBJETIVO_ESTRATEGIA: [CallbackQueryHandler(estrategia_objetivo_escolhido, pattern="^obj_")],
            ESCOLHENDO_PLATAFORMA_ESTRATEGIA: [CallbackQueryHandler(estrategia_finalizar, pattern="^plat_")]
        },
        fallbacks=[CommandHandler('cancelar', cancelar)],
        allow_reentry=True
    )

    # Registra o Fluxo do /feedback (V10)
    conv_feedback = ConversationHandler(
        entry_points=[CommandHandler('feedback', feedback_start)],
        states={
            RECEBENDO_ID_FEEDBACK: [MessageHandler(filters.TEXT & ~filters.COMMAND, feedback_receber_id)],
            RECEBENDO_METRICAS_FEEDBACK: [MessageHandler(filters.TEXT & ~filters.COMMAND, feedback_receber_metricas)]
        },
        fallbacks=[CommandHandler('cancelar', cancelar)],
        allow_reentry=True
    )

    # Registra o Fluxo do /modo_insano (V10)
    conv_insano = ConversationHandler(
        entry_points=[CommandHandler('modo_insano', modo_insano_start)],
        states={
            RECEBENDO_TEMA_INSANO: [MessageHandler(filters.TEXT & ~filters.COMMAND, modo_insano_receber_tema)]
        },
        fallbacks=[CommandHandler('cancelar', cancelar)],
        allow_reentry=True
    )

    app.add_handler(conv_copy)
    app.add_handler(conv_design)
    app.add_handler(conv_pesq)
    app.add_handler(conv_est)
    app.add_handler(conv_feedback)
    app.add_handler(conv_insano)
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("carrossel", cmd_carrossel))
    app.add_handler(CommandHandler("feedback", lambda u, c: u.message.reply_text("📈 **Módulo de Feedback V10:** Em breve você poderá enviar métricas por aqui!")))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text_generico))
    
    print("📡 Agente Telegram Mestre Iniciado em Nuvem de Conversação. (Ctrl+C para sair)")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()

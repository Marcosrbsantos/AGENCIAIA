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

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "COLOQUE_SEU_TOKEN_AQUI")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

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
    for tentativa in range(3):
        try:
            async with httpx.AsyncClient(follow_redirects=True) as client:
                # Timeout agressivo de 120 segundos para renderização pesada
                response = await client.get(url, headers=headers, timeout=httpx.Timeout(120.0, connect=30.0))
                if response.status_code == 200:
                    with open(caminho, 'wb') as f:
                        f.write(response.content)
                    return True
                else:
                    print(f"Erro HTTP {response.status_code} na tentativa {tentativa+1}")
        except Exception as e:
            print(f"Erro ao baixar imagem (tentativa {tentativa+1}): {e}")
            await asyncio.sleep(2)
    return False

async def renderizar_post_layout(titulo, descricao, caminho_saida):
    """Fallback: Renderiza um post profissional usando Playwright e template HTML"""
    try:
        html_path = "file:///" + os.path.abspath("execution/template_universal.html").replace("\\", "/")
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page(viewport={"width": 1080, "height": 1080})
            await page.goto(html_path)
            # Injeta conteúdo
            await page.evaluate(f"setContent('{titulo.upper()}', '{descricao}')")
            await page.wait_for_timeout(1000)
            await page.screenshot(path=caminho_saida, type="png")
            await browser.close()
        return True
    except Exception as e:
        print(f"Erro na renderização local: {e}")
        return False

# Estados da Máquina de Conversação
ESCOLHENDO_FORMATO_COPY, RECEBENDO_TEMA_COPY = range(2)
ESCOLHENDO_FORMATO_DESIGN, RECEBENDO_TEMA_DESIGN = range(2, 4)
ESCOLHENDO_TIPO_PESQUISA, RECEBENDO_TEMA_PESQUISA = range(4, 6)

async def set_menu_commands(app: Application):
    """Seta o autocomplete nativo do Telegram (barra flutuante)"""
    commands = [
        ("copy", "Roteirista - Gera textos magnéticos"),
        ("design", "Designer - Cria arte gráfica"),
        ("pesquisa", "Investigador - Pesquisas avançadas"),
        ("carrossel", "Renderiza o HTML V8 em Nuvem"),
        ("radar", "Mostra tendências do nicho"),
        ("estrategia", "Ajusta Hook/CTA da campanha")
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

async def copy_formato_escolhido(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    formato = query.data.replace("copy_", "").capitalize()
    context.user_data["copy_formato"] = formato # Salva na memoria local!
    
    await query.edit_message_text(text=f"📜 Formato escolhido: **{formato}**.\nPerfeito. Sobre qual TEMA devemos escrever?")
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
        context.user_data["ultima_copy"] = copy_final # MEMÓRIA INTER-AGENTES SALVA!
        
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
    
    memoria_copy = context.user_data.get("ultima_copy", None)
    
    if memoria_copy:
         await query.edit_message_text(text=f"🖼️ Formato visual: **{formato}**.\n\nMestre, puxei da minha Memória Neural a Copy da gaveta anterior!\n⏱️ Lendo a Biblioteca `estetica_tokens.md` para emular suas referências visuais...")
         
         # Lógica simulada de integração do modelo de referência
         try:
             tokens_estetica = carregar_contexto('estetica_tokens.md')
             biblia_panorama = carregar_contexto('panorama_design_2026.md')
             system_design = f"Você é o Diretor de Arte (Design Agent). Use a copy para idealizar um Prompt Descritivo de Imagem sob AS LEIS EXATAS DO GUIA MESTRE 2026 A SEGUIR:\n\n{biblia_panorama}\n\nE APLIQUE ESTES TOKENS DE ESTILO:\n\n{tokens_estetica}"
             
             client = AsyncGroq(api_key=GROQ_API_KEY)
             response = await client.chat.completions.create(
                 model="llama-3.3-70b-versatile",
                 messages=[
                     {"role": "system", "content": system_design},
                     {"role": "user", "content": f"A Copy é: {memoria_copy}. Formato: {formato}. Qual a estrutura visual exata baseada nas nossas Bíblias?"}
                 ],
                 temperature=0.6, max_tokens=1500
             )
             
             descricao_arte = response.choices[0].message.content
             import urllib.parse
             resolucao = "width=1080&height=1080" # Simplificando para 1:1 para máxima compatibilidade
             
             # Sanitização Pesada do Prompt
             prompt_base = f"Professional ad design, {descricao_arte}"
             prompt_sanitizado = re.sub(r'[^a-zA-Z0-9\s,]', '', prompt_base)[:600]
             url_imagem = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt_sanitizado)}?{resolucao}&nologo=true&seed=42"
             
             await context.bot.send_message(chat_id=update.effective_chat.id, text=f"🚀 **Escopo Visual Masterizado:**\n\n{descricao_arte}\n\n⏳ Renderizando Pixels na Nuvem e baixando para o servidor...")
             
             # Caminho temporário para a imagem
             path_temp = os.path.join(os.getcwd(), "outputs", f"temp_design_{update.effective_chat.id}.png")
             os.makedirs(os.path.dirname(path_temp), exist_ok=True)
             
             sucesso = await baixar_imagem(url_imagem, path_temp)
             
             if not sucesso:
                 # FALLBACK: Renderização Local
                 await context.bot.send_message(chat_id=update.effective_chat.id, text="⚠️ Servidor de IA instável. Ativando Motor de Design Determinístico (Local)...")
                 titulo_fallback = update.message.text[:50] if update.message else "POST DE DESIGN"
                 sucesso = await renderizar_post_layout(titulo_fallback, descricao_arte[:300], path_temp)

             if sucesso:
                 with open(path_temp, 'rb') as photo:
                     await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo, caption="✨ Sua arte masterizada está pronta!")
                 os.remove(path_temp)
             else:
                 await context.bot.send_message(chat_id=update.effective_chat.id, text="❌ Falha crítica na renderização (IA e Local). Tente um tema mais simples.")
             
         except Exception as e:
              await context.bot.send_message(chat_id=update.effective_chat.id, text=f"🔥 Erro ao ler referências de design: {e}")
              
         return ConversationHandler.END
    else:
         await query.edit_message_text(text=f"🖼️ Formato visual: **{formato}**.\nMestre, minha memória de Roteirista está vazia... Digite no chat qual a Copy ou a Ideia que você quer na imagem:")
         return RECEBENDO_TEMA_DESIGN

async def design_receber_tema_sujo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tema_manual = update.message.text
    formato = context.user_data.get("design_formato_sujo", "Post Estatico")
    await update.message.reply_text(f"⏱️ O Mestre digitou o Tema: '{tema_manual}' para um {formato}.\nLendo Biblioteca Ouro `estetica_tokens.md`...")
    
    try:
        tokens_estetica = carregar_contexto('estetica_tokens.md')
        biblia_panorama = carregar_contexto('panorama_design_2026.md')
        system_design = f"Você é o Diretor de Arte do Telegram. Molde o design sob as SEGUINTES REGRAS ABSOLUTAS DO GUIA DE 2026:\n\n{biblia_panorama}\n\nE TOKENS ESPECÍFICOS:\n\n{tokens_estetica}"
        
        client = AsyncGroq(api_key=GROQ_API_KEY)
        response = await client.chat.completions.create(
                 model="llama-3.3-70b-versatile",
                 messages=[
                     {"role": "system", "content": system_design},
                     {"role": "user", "content": f"Descreva o prompt fotográfico cirúrgico para a requisição: {tema_manual}."}
                 ],
                 temperature=0.6, max_tokens=1500
        )
        
        descricao_arte = response.choices[0].message.content
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
        
        sucesso = await baixar_imagem(url_imagem, path_temp)
        
        if not sucesso:
            # FALLBACK: Renderização Local
            await context.bot.send_message(chat_id=update.effective_chat.id, text="⚠️ Servidor de IA instável. Ativando Motor de Design Determinístico (Local)...")
            titulo_fallback = update.message.text[:50] if update.message else "POST DE DESIGN"
            sucesso = await renderizar_post_layout(titulo_fallback, descricao_arte[:300], path_temp)

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

async def cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE):
     await update.message.reply_text("🚫 Operação Abortada, Mestre.")
     return ConversationHandler.END

# Cérebro Genérico Se Fora de Comando
async def handle_text_generico(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
        fallbacks=[CommandHandler('cancelar', cancelar)]
    )
    
    # Registra o Fluxo do /design
    conv_design = ConversationHandler(
        entry_points=[CommandHandler('design', design_start)],
        states={
            ESCOLHENDO_FORMATO_DESIGN: [CallbackQueryHandler(design_formato_escolhido, pattern="^design_")],
            RECEBENDO_TEMA_DESIGN: [MessageHandler(filters.TEXT & ~filters.COMMAND, design_receber_tema_sujo)]
        },
        fallbacks=[CommandHandler('cancelar', cancelar)]
    )

    # Registra o Fluxo do /pesquisa
    conv_pesq = ConversationHandler(
        entry_points=[CommandHandler('pesquisa', pesquisa_start)],
        states={
            ESCOLHENDO_TIPO_PESQUISA: [CallbackQueryHandler(pesquisa_tipo_escolhido, pattern="^pesq_")],
            RECEBENDO_TEMA_PESQUISA: [MessageHandler(filters.TEXT & ~filters.COMMAND, pesquisa_gerar)]
        },
        fallbacks=[CommandHandler('cancelar', cancelar)]
    )

    app.add_handler(conv_copy)
    app.add_handler(conv_design)
    app.add_handler(conv_pesq)
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("carrossel", cmd_carrossel))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text_generico))
    
    print("📡 Agente Telegram Mestre Iniciado em Nuvem de Conversação. (Ctrl+C para sair)")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()

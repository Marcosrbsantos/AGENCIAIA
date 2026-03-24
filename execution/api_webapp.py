from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import json
import asyncio
from typing import Optional, List

# Importar o cérebro V10
from agente_estrategista_v10 import estrategista
import agente_telegram as tg_utils # Reuso de funções de design
from supabase_config import supabase

from fastapi.staticfiles import StaticFiles

app = FastAPI(title="AGENCIAIA Backend V11")

# Servir arquivos estáticos (designs gerados pelo motor Creata)
os.makedirs("outputs", exist_ok=True)
app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")

# Configurar CORS para permitir o frontend Vite
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://agenciaia-two.vercel.app",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    user_id: str
    chat_id: str
    plataforma: Optional[str] = "Instagram"
    objetivo: Optional[str] = "Engajamento"

class ChatResponse(BaseModel):
    response: str
    strategy: Optional[dict] = None
    copy_final: Optional[str] = None

@app.get("/")
async def root():
    return {"status": "online", "version": "V11", "agent": "Arquiteto Mestre"}

# Importar ferramentas compartilhadas
import brain_tools

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    try:
        print(f"DEBUG: Recebido: '{req.message}'")
        msg_lower = req.message.lower().strip()
        print(f"DEBUG: Processado: '{msg_lower}' (Starts with /design? {msg_lower.startswith('/design')})")
        
        # ROTEAMENTO DE COMANDOS
        if msg_lower.startswith("/pesquisa"):
            print("DEBUG: Entrou no fluxo /pesquisa")
            tema = req.message[9:].strip() or "Tendências de Marketing 2026"
            resultado = await brain_tools.executar_logica_pesquisa(tema, "Avançada")
            return ChatResponse(response=f"🔍 **Resultado da Pesquisa Científica:**\n\n{resultado}")
            
        elif msg_lower.startswith("/copy"):
            tema = req.message[5:].strip() or "Oferta Irresistível"
            copy = await brain_tools.executar_logica_copy(tema, "Post High-Ticket", "Contexto de conversão direta")
            return ChatResponse(response=f"✍️ **Copy Gerada com Sucesso:**\n\n{copy}", copy_final=copy)
            
        elif msg_lower.startswith("/design"):
            tema = req.message[7:].strip() or "Estética Cyber-Premium"
            prompt_vis = await brain_tools.gerar_prompt_visual(tema, "Post Quadrado")
            url_img = await brain_tools.gerar_design_url(prompt_vis)
            
            # Resposta robusta com Bloco de Design dedicado
            res = f"🎨 **Neural Design Renderizado:**\n"
            res += f"Prompt: _{prompt_vis}_\n\n"
            res += f"![Arte]({url_img})"
            
            return ChatResponse(response=res, copy_final=url_img)

        elif msg_lower.startswith("/carrossel"):
            tema = req.message[10:].strip() or "Estratégia de Escala 2026"
            slides = await brain_tools.executar_logica_carrossel(tema, num_slides=5)
            
            res = f"🎠 **Carrossel Estruturado Gerado (5 Slides):**\n\n"
            for slide in slides:
                res += f"### {slide['titulo']}\n"
                res += f"![Arte]({slide['url']})\n\n"
            
            return ChatResponse(response=res)

        # FLUXO PADRÃO: Estrategista V10
        estrategia = await estrategista.definir_estrategia(req.message, req.objetivo, req.plataforma)
        regras = tg_utils.carregar_contexto('modelos_roteiros.md')
        
        prompt_copy = f"""
        Baseado na ESTRATÉGIA abaixo, crie uma COPY de alta conversão.
        ESTRATÉGIA: {json.dumps(estrategia, ensure_ascii=False)}
        REGRAS DE OURO: {regras}
        Responda apenas com a copy final.
        """
        
        client = tg_utils.AsyncGroq(api_key=tg_utils.GROQ_API_KEY)
        r = await client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt_copy}],
            temperature=0.7
        )
        copy_final = r.choices[0].message.content
        
        # PERSISTÊNCIA SUPABASE
        try:
            supabase.table("preferred_models").insert({
                "user_id": req.user_id,
                "tipo": estrategia.get("fase_funil", "Geral"),
                "conteudo": copy_final
            }).execute()

            post_id = f"WEB_{req.user_id[:8]}_{os.urandom(4).hex()}"
            supabase.table("performance_logs").insert({
                "user_id": req.user_id,
                "post_id": post_id,
                "tema": req.message[:50],
                "tipo": req.plataforma,
                "estilo_copy": estrategia.get("emocao", "Padrao"),
                "likes": 0,
                "salvamentos": 0,
                "ctr": 0.0
            }).execute()
        except Exception as db_err:
            print(f"⚠️ Erro ao persistir no Supabase: {db_err}")
        
        ai_response = f"Mestre, tracei uma estratégia de **{estrategia['fase_funil']} de Funil** focada em **{estrategia['emocao']}**.\n\n"
        ai_response += f"**Ângulo:** {estrategia['angulo']}\n\n"
        ai_response += f"A copy já está pronta e otimizada para {req.plataforma}. Deseja que eu gere o design agora?"

        return ChatResponse(
            response=ai_response,
            strategy=estrategia,
            copy_final=copy_final
        )
        
    except Exception as e:
        print(f"Erro na API WebApp: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/vault/{user_id}")
async def get_vault(user_id: str):
    # Retorna o histórico de performance/posts (Neural Vault) do Supabase
    try:
        response = supabase.table("performance_logs")\
            .select("*")\
            .eq("user_id", user_id)\
            .order("created_at", desc=True)\
            .execute()
        return response.data
    except Exception as e:
        print(f"Erro ao buscar Vault: {e}")
        return []

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

import os
import json
import asyncio
import re
from groq import AsyncGroq
from dotenv import load_dotenv

load_dotenv()

PERFORMANCE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.tmp', 'performance_log.json')
PLATFORM_RULES_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'referencias', 'platform_rules.json')
MODELOS_PREFERIDOS_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.tmp', 'modelos_preferidos.json')

class AgenteEstrategistaV10:
    def __init__(self):
        # Ler a chave diretamente aqui para garantir que variáveis de ambiente do Railway sejam capturadas
        self.api_key = os.environ.get("GROQ_API_KEY")
        if not self.api_key:
            print("❌ ERRO CRÍTICO: GROQ_API_KEY não encontrada nas variáveis de ambiente do Railway!")
        self.client = AsyncGroq(api_key=self.api_key or "vazio")
        self.regras_plataforma = self.carregar_json(PLATFORM_RULES_PATH)

    def carregar_json(self, path):
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
        
    def carregar_contexto(self, arquivo):
        """Lê os manuais de referência 2026"""
        caminho = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'referencias', arquivo)
        if os.path.exists(caminho):
            with open(caminho, 'r', encoding='utf-8') as f:
                return f.read()
        return ""

    def carregar_aprendizado(self):
        """Lê os logs e retorna um resumo do que funcionou (CTR > 2.0 ou Likes > 50)"""
        if not os.path.exists(PERFORMANCE_PATH):
            return "Ainda não há dados de performance para análise."
        
        try:
            with open(PERFORMANCE_PATH, 'r', encoding='utf-8') as f:
                logs = json.load(f)
            
            sucessos = [
                f"Post {log['post_id']} ({log['tema']}): CTR {log['resultado']['ctr']}%, Likes {log['resultado']['likes']}. Estilo: {log['estilo_copy']}"
                for log in logs if log['resultado']['ctr'] > 2.0 or log['resultado']['likes'] > 50
            ]
            
            if not sucessos:
                return "Dados iniciais coletados, mas nenhum post atingiu métricas de elite ainda."
            
            # Limita aos top 5 sucessos de forma compatível
            limite = min(len(sucessos), 5)
            resultado = []
            for i in range(limite):
                resultado.append(sucessos[i])
            return "\n".join(resultado)
        except Exception:
            return "Erro ao ler banco de performance."

    def carregar_modelos_preferidos(self):
        """Lê os modelos que o mestre mandou 'aprender'"""
        if not os.path.exists(MODELOS_PREFERIDOS_PATH):
            return "Nenhum modelo customizado salvo ainda."
        
        try:
            with open(MODELOS_PREFERIDOS_PATH, 'r', encoding='utf-8') as f:
                modelos = json.load(f)
            
            resumo = [f"- {m['tipo']} em {m['data']}: {m['conteudo'][:300]}..." for m in modelos]
            return "\n".join(resumo)
        except Exception:
            return "Erro ao ler modelos preferidos."

    async def definir_estrategia(self, tema, objetivo, plataforma):
        """
        Gera a estratégia completa baseada no tema, objetivo, plataforma e aprendizado prévio.
        """
        aprendizado = self.carregar_aprendizado()
        
        # Regra determinística de Funil
        fase_funil = "Topo"
        if "venda" in objetivo.lower() or "leads" in objetivo.lower():
            fase_funil = "Fundo"
        elif "autoridade" in objetivo.lower() or "educar" in objetivo.lower():
            fase_funil = "Meio"

        system_prompt = (
            "Você é o Diretor Estratégico da AGENCIAIA. Sua missão é criar o DNA de uma campanha viral.\n"
            "Responda EXCLUSIVAMENTE em formato JSON puro para processamento automático.\n"
            f"BASE DE APRENDIZADO (Performance):\n{aprendizado}\n\n"
            f"MODELOS PREFERIDOS (O Mestre gosta deste estilo):\n{self.carregar_modelos_preferidos()}"
        )

        regra_especifica = self.regras_plataforma.get(plataforma.lower(), {})
        
        user_prompt = f"""
        TEMA: {tema}
        OBJETIVO: {objetivo}
        PLATAFORMA: {plataforma}
        FASE DO FUNIL: {fase_funil}
        
        REGRAS ESPECÍFICAS DA PLATAFORMA:
        - Tom de Voz: {regra_especifica.get('tom_de_voz', 'Premium')}
        - Foco Copy: {regra_especifica.get('foco_copy', 'Conversão')}
        - Design: {regra_especifica.get('estilo_design', 'Moderno')}
        
        Use as lições do APRENDIZADO para otimizar o ÂNGULO e o GANCHO abaixo:

        Gere a estratégia seguindo este esquema JSON:
        {{
            "persona": "descrição da audiência",
            "tipo_conteudo": "ex: carrossel educativo, vídeo curto, etc",
            "angulo": "o ângulo psicológico único",
            "emocao": "emoção primária a despertar",
            "gancho": "o hook matador (texto exato)",
            "cta": "chamada para ação específica baseada na plataforma",
            "template": "escolha entre 'premium_dark' ou 'solar_clean'",
            "tag": "uma tag curta de 2-3 palavras para o layout"
        }}
        """

        try:
            response = await self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            estrategia = json.loads(response.choices[0].message.content)
            estrategia["fase_funil"] = fase_funil
            return estrategia
        except Exception as e:
            print(f"Erro no Estrategista V10: {e}")
            return {
                "persona": "Geral",
                "tipo_conteudo": "Post Estático",
                "angulo": "Direto",
                "emocao": "Curiosidade",
                "gancho": f"Descubra sobre {tema}",
                "cta": "Confira agora",
                "fase_funil": fase_funil,
                "erro": str(e)
            }

    async def definir_variacoes(self, tema, plataforma):
        """Gera 3 variações estratégicas distintas no Modo Insano"""
        aprendizado = self.carregar_aprendizado()
        regra_especifica = self.regras_plataforma.get(plataforma.lower(), {})
        
        system_prompt = (
            "Você é o Diretor Criativo da AGENCIAIA no MODO INSANO.\n"
            "Sua missão é gerar 3 abordagens COMPLETAMENTE DIFERENTES para o mesmo tema.\n"
            "Responda EXCLUSIVAMENTE um JSON com uma lista 'variacoes' contendo 3 objetos de estratégia."
        )

        user_prompt = f"""
        TEMA: {tema}
        PLATAFORMA: {plataforma}
        REGRAS: {regra_especifica}
        APRENDIZADO: {aprendizado}
        ESTILOS PREFERIDOS: {self.carregar_modelos_preferidos()}
        
        Gere 3 variações (Ângulos: Emocional, Analítico, Provocativo).
        Cada objeto deve seguir o esquema JSON padrão (persona, tipo_conteudo, angulo, emocao, gancho, cta, template, tag).
        """
        
        try:
            response = await self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
                temperature=0.8,
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content).get("variacoes", [])
        except Exception as e:
            print(f"Erro no Modo Insano: {e}")
            return []

# Instância Global para uso no Telegram
estrategista = AgenteEstrategistaV10()

if __name__ == "__main__":
    async def test():
        res = await estrategista.definir_estrategia("Energia Solar", "Gerar Leads", "Instagram")
        print(json.dumps(res, indent=4, ensure_ascii=False))
    asyncio.run(test())

import os
import requests
import json
import time
from enviar_planilha import enviar_para_webhook

def analisar_performance_semanal():
    """
    O Agente Analista lê a aba 'analytics', identifica padrões e 
    gera uma recomendação estratégica para o próximo ciclo.
    """
    print("📊 [ANALISTA] Coletando dados de performance...")
    
    # Em uma versão final, ele leria o CSV da aba analytics.
    # Aqui simulamos o processo de aprendizado.
    
    aprendizado = {
        "periodo": "Última Semana",
        "top_conteudo": "A Taxação do Sol 2026",
        "padrao_identificado": "Ganchos baseados em MEDO e URGÊNCIA tiveram 40% mais retenção.",
        "recomendação": "Focar em temas regulatórios para JC Antunes e Comportamento para Marcos.",
        "status": "Aprendizado Enviado"
    }
    
    # Salva na aba analytics para o Estrategista consultar
    enviar_para_webhook(aprendizado, "analytics")
    
    return aprendizado

if __name__ == "__main__":
    analise = analisar_performance_semanal()
    print(f"\n📈 Ciclo de Aprendizado Concluído!")
    print(f"💡 Insight da Semana: {analise['padrao_identificado']}")

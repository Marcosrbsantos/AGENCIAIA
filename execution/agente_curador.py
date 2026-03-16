import os
import requests
import json
from enviar_planilha import enviar_para_webhook

def classificar_ideia(tema):
    """
    Lógica de Curadoria: Filtra e classifica a ideia para o perfil e formato ideal.
    """
    tema_lower = tema.lower()
    
    # Lógica Condicional do Curador
    if any(k in tema_lower for k in ["solar", "painel", "energia", "economia", "fotovolt", "aneel"]):
        perfil = "jcantunes"
        # Se for sobre economia ou lei -> Post/Carrossel Instagram
        if any(k in tema_lower for k in ["taxa", "lei", "economia", "valor"]):
            formato = "Carrossel Instagram"
            prioridade = 9
        else:
            formato = "Post Instagram"
            prioridade = 7
    elif any(k in tema_lower for k in ["marketing", "tecnologia", "ia", "comportamento", "psicologia", "vício"]):
        perfil = "marcos"
        # Se for técnico/profundo -> YouTube
        if any(k in tema_lower for k in ["história", "guia", "como funciona", "ciência"]):
            formato = "YouTube (Longo)"
            prioridade = 8
        else:
            formato = "Reels/Shorts"
            prioridade = 10
    else:
        perfil = "marcos" # Padrão
        formato = "Story Instagram"
        prioridade = 5

    return {
        "tema": tema,
        "perfil": perfil,
        "formato": formato,
        "nota_relevancia": prioridade,
        "status": "Curadoria Concluída"
    }

def executar_curadoria(lista_temas):
    """Processa uma lista de temas brutos do Radar"""
    print(f"📚 [CURADOR] Iniciando curadoria de {len(lista_temas)} temas...")
    
    for tema in lista_temas:
        resultado = classificar_ideia(tema)
        print(f"✅ Classificado: {resultado['perfil']} -> {resultado['formato']}")
        enviar_para_webhook(resultado, "ideias")

if __name__ == "__main__":
    # Teste de Curadoria
    temas_teste = [
        "Novas baterias de sódio para energia solar",
        "Como a dopamina afeta sua produtividade no marketing",
        "A queda nos preços dos painéis fotovoltaicos em 2025"
    ]
    executar_curadoria(temas_teste)

import time
import os
import sys

# Garante que as importações locais funcionem
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agente_radar import buscar_tendencias
from agente_curador import classificar_ideia
from agente_pesquisador import aprofundar_ideia
from agente_estrategista import decidir_estrategia
from agente_roteirista import produzir_conteudo_final
from agente_design import criar_design_automatico
from agente_compositor import compor_post_final
from agente_planejador import organizar_agenda
from agente_analista import analisar_performance_semanal
from enviar_planilha import enviar_para_webhook

def despertar_exodia_consolidado(perfil_teste):
    print(f"\n🏛️ [ARQUITETO] Iniciando Ciclo CONSOLIDADO para: {perfil_teste.upper()}\n" + "="*50)
    
    # 1. RADAR (Busca)
    print("🛰️ Agente 1: Buscando tendências...")
    ideias_brutas = buscar_tendencias(perfil_teste)
    if not ideias_brutas:
        print("❌ Nenhuma ideia encontrada no radar.")
        return
    
    # 2 & 3. CURADOR (Seleciona a melhor)
    ideia_bruta = ideias_brutas[0]['tema']
    print(f"📚 Agente 3: Curando tema -> {ideia_bruta}")
    curadoria = classificar_ideia(ideia_bruta) # Este ainda envia para Ideas, o que é OK para o Radar
    tema = curadoria['tema']
    formato = curadoria['formato']
    
    # 4. PESQUISADOR (Gera Dossiê) - MODO SILENCIOSO (enviar=False)
    print("🔎 Agente 2: Gerando dossiê estratégico...")
    contexto = aprofundar_ideia(tema, perfil_teste, enviar=False)
    
    # 5. ESTRATEGISTA (Define Hook/CTA) - MODO SILENCIOSO
    print("🎯 Agente 4: Traçando engenharia de retenção...")
    estrategia = decidir_estrategia(tema, perfil_teste, formato, contexto, enviar=False)
    
    # 6. ROTEIRISTA (Escreve) - MODO SILENCIOSO
    print("✍️ Agente 5: Escrevendo roteiro final...")
    roteiro = produzir_conteudo_final(tema, perfil_teste, formato, estrategia, contexto, enviar=False)
    
    # 7. DESIGN (Visual) - MODO SILENCIOSO
    print("🎨 Agente 6: Criando conceito visual...")
    design_url_raw = criar_design_automatico(tema, perfil_teste, roteiro[:100], enviar=False)
    
    # 7.1 COMPOSITOR (Arte Final)
    print("🖌️ Agente 9: Compondo arte final com texto...")
    output_filename = f"post_{perfil_teste}_{int(time.time())}.png"
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "outputs", output_filename)
    arte_final_path = compor_post_final(tema, perfil_teste, design_url_raw, output_path)
    
    # 8. SUPER PAYLOAD (O "Combo" final em linha única)
    print("🚀 Agente Mestre: Consolidando em linha única...")
    payload_mestre = {
        "tema": tema,
        "perfil": perfil_teste,
        "data": time.strftime("%d/%m/%Y"),
        "status": "Pronto para Produção",
        "formato": formato,
        "contexto": contexto,
        "estrategia_gancho_cta": estrategia,
        "conteudo": roteiro,
        "link_drive": arte_final_path if arte_final_path else design_url_raw,
        "nota_relevancia": 10
    }
    
    # Envia TUDO de uma vez para a aba 'ideias' (que agora deve ter as colunas extras)
    enviar_para_webhook(payload_mestre, "ideias")
    
    print("\n" + "="*50 + f"\n✅ CICLO CONSOLIDADO CONCLUÍDO! Tudo em uma única linha.\n")

if __name__ == "__main__":
    perfil = sys.argv[1] if len(sys.argv) > 1 else "jcantunes"
    despertar_exodia_consolidado(perfil)

import time
import os
from agente_radar import buscar_tendencias
from agente_curador import classificar_ideia
from agente_pesquisador import aprofundar_ideia
from agente_estrategista import decidir_estrategia
from agente_roteirista import produzir_conteudo_final
from agente_design import criar_design_automatico
from agente_planejador import organizar_agenda
from agente_analista import analisar_performance_semanal

def despertar_exodia(perfil_teste):
    print(f"\n🏛️ [ARQUITETO] Iniciando Ciclo de Produção para: {perfil_teste.upper()}\n" + "="*50)
    
    # 1. RADAR (Busca)
    print("🛰️ Agente 1: Buscando tendências...")
    ideias_brutas = buscar_tendencias(perfil_teste)
    if not ideias_brutas:
        print("❌ Nenhuma ideia encontrada no radar.")
        return
    
    # 2 & 3. CURADOR (Seleciona a melhor)
    ideia_bruta = ideias_brutas[0]['tema']
    print(f"📚 Agente 3: Curando tema -> {ideia_bruta}")
    curadoria = classificar_ideia(ideia_bruta)
    tema = curadoria['tema']
    formato = curadoria['formato']
    
    # 4. PESQUISADOR (Gera Dossiê)
    print("🔎 Agente 2: Gerando dossiê de inteligência...")
    contexto = aprofundar_ideia(tema, perfil_teste)
    
    # 5. ESTRATEGISTA (Define Hook/CTA)
    print("🎯 Agente 4: Traçando estratégia de retenção...")
    estrategia = decidir_estrategia(tema, perfil_teste, formato, contexto)
    
    # 6. ROTEIRISTA (Escreve)
    print("✍️ Agente 5: Escrevendo roteiro final...")
    roteiro = produzir_conteudo_final(tema, perfil_teste, formato, estrategia, contexto)
    
    # 7. DESIGN (Visual)
    print("🎨 Agente 6: Gerando artes...")
    design = criar_design_automatico(tema, perfil_teste, roteiro[:100])
    
    # 8. PLANEJADOR (Agenda)
    print("📅 Agente 7: Organizando calendário...")
    agenda = organizar_agenda(tema, perfil_teste, "Automático", formato)
    
    # 9. ANALISTA (Aprendizado)
    print("📊 Agente 8: Analisando ciclo...")
    analise = analisar_performance_semanal()
    
    print("\n" + "="*50 + f"\n✅ CICLO CONCLUÍDO COM SUCESSO! Confira sua planilha, Mestre.\n")

if __name__ == "__main__":
    # Testaremos um ciclo para cada perfil
    despertar_exodia("jcantunes") # Teste Solar
    time.sleep(5)
    despertar_exodia("marcos")    # Teste Personal

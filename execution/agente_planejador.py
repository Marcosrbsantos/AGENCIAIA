import os
import requests
import json
import time
from enviar_planilha import enviar_para_webhook

def organizar_agenda(tema, perfil_id, plataforma, formato):
    """
    O Agente Planejador define a data/hora e organiza o arquivamento.
    Como operamos em stack grátis, ele dispara gatilhos para o Make.com 
    que faz a conexão real com Google Drive e Calendar.
    """
    print(f"📅 [PLANEJADOR] Organizando agenda para: {tema}")
    
    # Lógica de horários padrão Brasil
    agora = time.time()
    # Simula agendamento para daqui a 2 dias às 11:00 ou 18:00
    dia_publicacao = time.strftime("%d/%m/%Y", time.localtime(agora + 172800)) 
    hora_publicacao = "11:00" if perfil_id == "jcantunes" else "18:00"

    payload = {
        "data": dia_publicacao,
        "hora": hora_publicacao,
        "perfil": perfil_id,
        "plataforma": plataforma,
        "formato": formato,
        "tema": tema,
        "status": "Agendado",
        "pasta_drive": f"/ArquitetoVivo/{perfil_id.upper()}/{formato.replace(' ', '_')}/"
    }
    
    # Salva na aba calendario
    enviar_para_webhook(payload, "calendario")
    
    return payload

if __name__ == "__main__":
    # Teste de Planejamento
    t = "Estratégia de Retenção para 2026"
    p = "marcos"
    plt = "YouTube"
    f = "Vídeo Longo"
    
    resultado = organizar_agenda(t, p, plt, f)
    print(f"\n✅ Conteúdo Agendado: {resultado['data']} às {resultado['hora']}")

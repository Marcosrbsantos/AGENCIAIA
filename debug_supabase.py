from execution.supabase_config import supabase
try:
    # Tenta listar tabelas ou verificar se 'chats' existe
    res = supabase.table("chats").select("*").limit(1).execute()
    print("Table 'chats' check:", res.data)
    
    res_msg = supabase.table("messages").select("*").limit(1).execute()
    print("Table 'messages' check:", res_msg.data)
    
except Exception as e:
    print(f"Erro ao acessar Supabase: {e}")

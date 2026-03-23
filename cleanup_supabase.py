from execution.supabase_config import supabase
try:
    # Deleta tudo de mensagens primeiro (FK)
    res1 = supabase.table("messages").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
    print("Delete messages:", res1)
    
    # Deleta tudo de chats
    res2 = supabase.table("chats").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
    print("Delete chats:", res2)
    
    # Verifica se sumiu
    final = supabase.table("chats").select("*").execute()
    print("Final chats count:", len(final.data))
    
except Exception as e:
    print(f"Erro no cleanup: {e}")

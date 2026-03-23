from execution.supabase_config import supabase
try:
    res = supabase.table("performance_logs").select("*").limit(1).execute()
    print("Conexão Supabase OK!")
    print(res.data)
except Exception as e:
    print(f"Erro na conexão Supabase: {e}")

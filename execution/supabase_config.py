import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Carregar variáveis de ambiente do diretório pai (raiz do projeto)
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(env_path)

url: str = os.environ.get("VITE_SUPABASE_URL")
key: str = os.environ.get("VITE_SUPABASE_ANON_KEY")

if not url or not key:
    print("⚠️ Supabase URL ou Key não encontrados no .env")

supabase: Client = create_client(url, key)

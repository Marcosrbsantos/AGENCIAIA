import sys
import os
import time

# Adiciona o diretório de execução ao path para importar a config
sys.path.append(os.path.join(os.getcwd(), 'execution'))
from supabase_config import supabase

def test_supabase_upload():
    bucket_name = "agenciaia-designs"
    test_filename = f"verify_cloud_{int(time.time())}.txt"
    temp_path = "temp_test.txt"
    
    with open(temp_path, "w") as f:
        f.write("VALIDAÇÃO AGENCIAIA V11 SAAS")
        
    try:
        print(f"🚀 Iniciando teste de conexão Cloud: {bucket_name}")
        
        # 1. Tentar upload
        with open(temp_path, "rb") as f:
            supabase.storage.from_(bucket_name).upload(
                path=test_filename,
                file=f,
                file_options={"upsert": "true"}
            )
        print("✅ Upload realizado com sucesso!")
        
        # 2. Obter URL pública
        url = supabase.storage.from_(bucket_name).get_public_url(test_filename)
        print(f"🔗 URL Pública: {url}")
        
    except Exception as e:
        print(f"❌ Falha no teste: {e}")
        print("DICA: Verifique se você criou o bucket 'agenciaia-designs' como PUBLIC e rodou o SQL das Policies.")
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == "__main__":
    test_supabase_upload()

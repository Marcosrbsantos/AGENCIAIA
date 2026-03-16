import os
import requests
import yt_dlp
import json
from dotenv import load_dotenv

load_dotenv()
GROQ_KEY = os.getenv("GROQ_API_KEY")

NICHO = "Criatividade"

print(f"🕵️ Buscando vídeos sobre: {NICHO}")

# 1. Puxando dados diretamente pelo yt-dlp
ydl_opts = {
    'extract_flat': 'in_playlist',
    'quiet': True,
    'no_warnings': True,
}
search_query = f"ytsearch3:{NICHO} #shorts"

videos = []
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info_dict = ydl.extract_info(search_query, download=False)
    if 'entries' in info_dict:
        videos = info_dict['entries']

if not videos:
    print("Nenhum vídeo encontrado.")
    exit()

video_alvo = videos[0]
print(f"✅ Vídeo Viral Encontrado: {video_alvo.get('title')} (Autor: {video_alvo.get('uploader')}) - {video_alvo.get('view_count')} views")

# Configurando as variáveis como esperado
video_alvo['url_video'] = video_alvo.get('url')
video_alvo['titulo'] = video_alvo.get('title')
video_alvo['autor'] = video_alvo.get('uploader')
video_alvo['visualizacoes'] = video_alvo.get('view_count')

# 2. Baixando o Áudio
print("⏳ Baixando áudio...")
opts = {
    'format': 'bestaudio/best',
    'outtmpl': 'alvo.%(ext)s',
    'quiet': True
}
with yt_dlp.YoutubeDL(opts) as ydl:
    info = ydl.extract_info(video_alvo['url_video'], download=True)
    extencao = info.get('ext', 'm4a')
    
audio_path = f"alvo.{extencao}"

# 3. Transcrevendo no Groq (Whisper)
print(f"🧠 Transcrevendo {audio_path} com Groq Whisper...")
url = "https://api.groq.com/openai/v1/audio/transcriptions"
headers = {
    "Authorization": f"Bearer {GROQ_KEY}"
}
files = {
    'file': (audio_path, open(audio_path, 'rb')),
    'model': (None, 'whisper-large-v3-turbo'),
    'response_format': (None, 'verbose_json')
}
res = requests.post(url, headers=headers, files=files)

transcricao = res.json()
print("\n📝 TRANSCRIÇÃO SEGUNDO A SEGUNDO:")
if 'segments' in transcricao:
    for seg in transcricao['segments']:
        print(f"[{seg['start']:.2f} - {seg['end']:.2f}] {seg['text']}")
else:
    print(transcricao)

# Salvar metadata para o LLM pensar
with open('transcricao.txt', 'w', encoding='utf-8') as f:
    f.write(f"Autor: {video_alvo['autor']}\nTitulo: {video_alvo['titulo']}\nViews: {video_alvo['visualizacoes']}\n\n")
    if 'segments' in transcricao:
        for seg in transcricao['segments']:
            f.write(f"[{seg['start']:.2f} - {seg['end']:.2f}] {seg['text']}\n")

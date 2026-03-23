# Imagem Oficial da Microsoft para Python e Playwright
# Usamos a versao jammy (Ubuntu 22.04 LTS) pre-carregada com Chromium para evitar dor de cabeca de fontes quebrando em Linux
FROM mcr.microsoft.com/playwright/python:v1.42.0-jammy

# Setar a pasta principal de trabalho
WORKDIR /app

# Instalar dependencias nativas do sistema (caso o U2Net/Rembg pecise compilar algo em C/C++)
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    x11-apps \
    && rm -rf /var/lib/apt/lists/*

# Copiar apenas os requerimentos limpos
COPY requirements_cloud.txt .

# Instalar as bibliotecas de Inteligencia Artificial (Groq, Gemini, U2Net-Rembg)
RUN pip install --no-cache-dir -r requirements_cloud.txt

# Baixar o modelo U2Net previamente para acelerar os renders de fotografia no Docker
RUN mkdir -p ~/.u2net \
    && curl -L https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx -o ~/.u2net/u2net.onnx

# Instalar fontes do sistema (Inter) para o HTML renderizar com precisao milimetrica
RUN apt-get update && apt-get install -y fonts-inter && rm -rf /var/lib/apt/lists/*

# Copiar todo o fluxo da Agencia
COPY . .

# Caso queiramos expor a porta da api futuramente 
EXPOSE 8000

# Inicia a API WebApp automaticamente ao subir o contêiner
CMD ["python", "execution/api_webapp.py"]

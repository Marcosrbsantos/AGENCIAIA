# Arquiteto de Design - Script de Sincronização GitHub
Write-Host "🚀 Iniciando Sincronização Master com GitHub..." -ForegroundColor Cyan

# Verifica se o Git está no PATH, senão usa o caminho absoluto
$gitPath = "C:\Program Files\Git\cmd\git.exe"
if (!(Test-Path $gitPath)) {
    $gitPath = "git"
}

# Verifica se a CLI do GitHub está no PATH
$ghPath = "C:\Program Files\GitHub CLI\gh.exe"
if (!(Test-Path $ghPath)) {
    $ghPath = "gh"
}

Write-Host "🔐 Passo 1: Autenticação (Siga as instruções na tela)..." -ForegroundColor Yellow
& $ghPath auth login --hostname github.com -p https -w

Write-Host "📦 Passo 2: Sincronizando arquivos..." -ForegroundColor Yellow
& $gitPath add .
& $gitPath commit -m "feat: estabilização do bot com motor duplo IA + Playwright e redundância de renderização" -allow-empty

Write-Host "📤 Passo 3: Subindo para a Nuvem (Main)..." -ForegroundColor Yellow
& $gitPath push -u origin main

Write-Host "✅ Sincronização Concluída, Mestre! Seu código está seguro." -ForegroundColor Green

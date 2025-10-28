# Create AI Agent on n8n
# PowerShell script for Windows

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 69) -ForegroundColor Cyan
Write-Host "🤖 Creating AI Agent on n8n" -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 69) -ForegroundColor Cyan
Write-Host ""

# Check if n8n is running
Write-Host "📋 Checking if n8n is running..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5678" -TimeoutSec 5 -UseBasicParsing
    Write-Host "✅ n8n is running at http://localhost:5678" -ForegroundColor Green
} catch {
    Write-Host "❌ Cannot connect to n8n at http://localhost:5678" -ForegroundColor Red
    Write-Host "   Please start n8n first!" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "   Start n8n with:" -ForegroundColor Cyan
    Write-Host "   docker run -it --rm -p 5678:5678 n8nio/n8n" -ForegroundColor White
    exit 1
}

# Check if Python is installed
Write-Host ""
Write-Host "🐍 Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.8+ first." -ForegroundColor Red
    exit 1
}

# Check if .env file exists
Write-Host ""
Write-Host "🔑 Checking API keys..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "✅ .env file found" -ForegroundColor Green
} else {
    Write-Host "❌ .env file not found!" -ForegroundColor Red
    Write-Host "   Please copy .env.example to .env and add your API keys" -ForegroundColor Yellow
    exit 1
}

# Install dependencies if needed
Write-Host ""
Write-Host "📦 Checking dependencies..." -ForegroundColor Yellow
Write-Host "   This may take a moment..." -ForegroundColor Gray

$requirements = @(
    "python-dotenv",
    "requests",
    "openai",
    "chromadb",
    "langchain",
    "langchain-openai"
)

foreach ($package in $requirements) {
    $installed = pip show $package 2>$null
    if (-not $installed) {
        Write-Host "   Installing $package..." -ForegroundColor Gray
        pip install $package --quiet
    }
}
Write-Host "✅ All dependencies ready" -ForegroundColor Green

# Run the agent creation script
Write-Host ""
Write-Host "🚀 Creating your AI agent..." -ForegroundColor Yellow
Write-Host ""

python create_agent_local.py

Write-Host ""
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 69) -ForegroundColor Cyan
Write-Host "✨ Script completed!" -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 69) -ForegroundColor Cyan

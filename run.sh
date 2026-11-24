#!/usr/bin/env bash

# ==========================================
# TEXTFORGE AI - SCRIPT DE INICIALIZAÇÃO
# Version: 1.0.0
# ==========================================

set -e

# Diretório raiz do projeto
PROJECT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

cd "$PROJECT_DIR"

echo ""
echo "=========================================="
echo "          TEXTFORGE AI v1.0.0"
echo "=========================================="
echo ""

# Verificar ambiente virtual
if [ ! -d "venv" ]; then
    echo "[INFO] Ambiente virtual não encontrado."
    echo "[INFO] Criando ambiente virtual..."

    python3 -m venv venv
fi

# Ativar ambiente virtual
source venv/bin/activate

echo "[OK] Ambiente virtual ativado."

# Verificar dependências
if ! python -c "import streamlit, groq, dotenv" >/dev/null 2>&1; then
    echo "[INFO] Instalando dependências..."

    python -m pip install -r requirements.txt
fi

echo "[OK] Dependências verificadas."

# Verificar arquivo de configuração
if [ ! -f ".env" ]; then
    echo ""
    echo "[AVISO] Arquivo .env não encontrado."
    echo "Configure sua chave GROQ_API_KEY no arquivo .env"
    echo "Utilize o arquivo .env.example como referência."
    echo ""
    exit 1
fi

echo "[OK] Arquivo de configuração encontrado."

# Iniciar aplicação
echo ""
echo "[INFO] Iniciando TextForge AI..."
echo "[INFO] Para encerrar, pressione CTRL+C."
echo ""

exec streamlit run app.py

#!/usr/bin/env bash
# Script para inicialização do cetam lab tea
echo "=========================================================="
echo "  🚀 INICIANDO CETAM LAB TEA (MVP)"
echo "  Laboratório de Informática / Acessibilidade Touchless"
echo "=========================================================="

# Checa se o Python está disponível
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não foi encontrado. Por favor instale o Python 3."
    exit 1
fi

# Inicia o servidor Python
python3 app.py

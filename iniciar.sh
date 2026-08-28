#!/usr/bin/env bash
# ==============================================================================
# PROJETO CETAM LAB TEA // INTERFACE HOLOGRÁFICA TOUCHLESS
# CETAM - Centro de Educação Tecnológica do Amazonas
# IBC - Instituto Benjamin Constant
# ==============================================================================
# Script de Inicialização Automatizada para Ubuntu Linux
# Verifica dependências de sistema, Python e ambiente antes da inicialização.
# ==============================================================================

set -e

# Cores para feedback no terminal
VERDE='\033[0;32m'
CIANO='\033[0;36m'
AMARELO='\033[1;33m'
VERMELHO='\033[0;31m'
NEGRITO='\033[1m'
NC='\033[0m' # Sem cor

echo -e "${CIANO}================================================================${NC}"
echo -e "${CIANO}  🚀 CETAM - CENTRO DE EDUCAÇÃO TECNOLÓGICA DO AMAZONAS         ${NC}"
echo -e "${CIANO}  🏛️ IBC - INSTITUTO BENJAMIN CONSTANT                          ${NC}"
echo -e "${CIANO}  ✨ INICIANDO CETAM LAB TEA // INTERFACE TOUCHLESS (MVP)       ${NC}"
echo -e "${CIANO}================================================================${NC}"

# Diretório base do script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# ------------------------------------------------------------------------------
# 1. VERIFICAÇÃO DE DEPENDÊNCIAS DO SISTEMA OPERACIONAL (UBUNTU/DEBIAN)
# ------------------------------------------------------------------------------
echo -e "\n${NEGRITO}[1/4] Verificando dependências do sistema Linux Ubuntu...${NC}"

PACOTES_SISTEMA_FALTANDO=()

# Checa Python 3
if ! command -v python3 &> /dev/null; then
    PACOTES_SISTEMA_FALTANDO+=("python3")
fi

# Checa PIP
if ! command -v pip3 &> /dev/null && ! python3 -m pip --version &> /dev/null; then
    PACOTES_SISTEMA_FALTANDO+=("python3-pip")
fi

# Checa suporte a Ambiente Virtual (venv)
if ! python3 -c "import venv" &> /dev/null; then
    PACOTES_SISTEMA_FALTANDO+=("python3-venv")
fi

# Checa cURL
if ! command -v curl &> /dev/null; then
    PACOTES_SISTEMA_FALTANDO+=("curl")
fi

# Checa se há algum navegador instalado no sistema
TEM_NAVEGADOR=false
for BROWSER in google-chrome google-chrome-stable chromium-browser chromium firefox brave-browser xdg-open; do
    if command -v "$BROWSER" &> /dev/null; then
        TEM_NAVEGADOR=true
        break
    fi
done

if [ "$TEM_NAVEGADOR" = false ]; then
    echo -e "${AMARELO}⚠️ Nenhum navegador web gráfico foi detectado.${NC}"
    PACOTES_SISTEMA_FALTANDO+=("chromium-browser")
fi

# Se houver pacotes faltando, instala via APT solicitando credencial sudo
if [ ${#PACOTES_SISTEMA_FALTANDO[@]} -gt 0 ]; then
    echo -e "${AMARELO}⚠️ Foram identificadas dependências ausentes no sistema:${NC} ${PACOTES_SISTEMA_FALTANDO[*]}"
    echo -e "${AMARELO}🔑 Solicitando credenciais de administrador (sudo) para instalar os componentes necessários...${NC}\n"
    
    sudo apt-get update -y
    sudo apt-get install -y "${PACOTES_SISTEMA_FALTANDO[@]}"
    echo -e "${VERDE}✓ Dependências do sistema instaladas com sucesso!${NC}"
else
    echo -e "${VERDE}✓ Todos os softwares base do sistema Ubuntu estão presentes.${NC}"
fi

# ------------------------------------------------------------------------------
# 2. CONFIGURAÇÃO DO AMBIENTE VIRTUAL PYTHON (ISOLAMENTO E COMPATIBILIDADE)
# ------------------------------------------------------------------------------
echo -e "\n${NEGRITO}[2/4] Verificando ambiente Python e bibliotecas...${NC}"

VENV_DIR="$SCRIPT_DIR/.venv"

if [ ! -d "$VENV_DIR" ] || [ ! -f "$VENV_DIR/bin/activate" ]; then
    echo -e "${CIANO}⚙️ Criando ambiente virtual Python isolado (.venv)...${NC}"
    python3 -m venv "$VENV_DIR"
fi

# Ativa o ambiente virtual
source "$VENV_DIR/bin/activate"

# Garante pip atualizado no venv
pip install --upgrade pip --quiet

# ------------------------------------------------------------------------------
# 3. VERIFICAÇÃO E INSTALAÇÃO DE PACOTES PYTHON (FastAPI, Uvicorn, Pydantic)
# ------------------------------------------------------------------------------
echo -e "\n${NEGRITO}[3/4] Validando bibliotecas Python (FastAPI, Uvicorn, Pydantic)...${NC}"

PYTHON_DEPS_FALTANDO=false

if ! python3 -c "import fastapi, uvicorn, pydantic" &> /dev/null; then
    PYTHON_DEPS_FALTANDO=true
fi

if [ "$PYTHON_DEPS_FALTANDO" = true ]; then
    echo -e "${CIANO}📥 Instalando bibliotecas do servidor web...${NC}"
    if [ -f "$SCRIPT_DIR/requirements.txt" ]; then
        pip install -r "$SCRIPT_DIR/requirements.txt"
    else
        pip install "fastapi>=0.100.0" "uvicorn>=0.22.0" "pydantic>=2.0.0"
    fi
    echo -e "${VERDE}✓ Bibliotecas Python instaladas com sucesso!${NC}"
else
    echo -e "${VERDE}✓ Todas as bibliotecas Python necessárias estão prontas.${NC}"
fi

# ------------------------------------------------------------------------------
# 4. DIAGNÓSTICO DE PERIFÉRICOS (WEBCAM)
# ------------------------------------------------------------------------------
echo -e "\n${NEGRITO}[4/4] Verificando dispositivo de câmera...${NC}"
if ls /dev/video* &> /dev/null; then
    echo -e "${VERDE}✓ Webcam detectada no sistema (/dev/video).${NC}"
else
    echo -e "${AMARELO}⚠️ Nenhuma câmera USB (/dev/video*) foi encontrada no momento.${NC}"
    echo -e "${AMARELO}   (Conecte a webcam para usar a visão computacional no ar).${NC}"
fi

# ------------------------------------------------------------------------------
# 5. EXECUÇÃO DA APLICAÇÃO
# ------------------------------------------------------------------------------
echo -e "\n${CIANO}================================================================${NC}"
echo -e "${VERDE}  🚀 TUDO PRONTO! INICIANDO SERVIDOR CETAM LAB TEA...${NC}"
echo -e "${CIANO}  Acesse no navegador: ${NEGRITO}http://localhost:8000${NC}"
echo -e "${CIANO}  Pressione ${NEGRITO}[Ctrl + C]${CIANO} neste terminal para encerrar.${NC}"
echo -e "${CIANO}================================================================${NC}\n"

# Executa o servidor Python com o ambiente virtual
exec python3 app.py

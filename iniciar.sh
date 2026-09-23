#!/usr/bin/env bash
# ==============================================================================
# PROJETO CETAM LAB TEA // INTERFACE HOLOGRÁFICA TOUCHLESS
# CETAM - Centro de Educação Tecnológica do Amazonas
# IBC - Instituto Benjamin Constant
# ==============================================================================
# Script de Inicialização Automatizada com Suporte 100% Offline (Rede Local)
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
echo -e "${CIANO}  ✨ CETAM LAB TEA // INTERFACE TOUCHLESS (100% OFFLINE)        ${NC}"
echo -e "${CIANO}================================================================${NC}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# ------------------------------------------------------------------------------
# 1. VERIFICAÇÃO DE DEPENDÊNCIAS DO SISTEMA OPERACIONAL
# ------------------------------------------------------------------------------
echo -e "\n${NEGRITO}[1/5] Verificando dependências do sistema Linux Ubuntu...${NC}"

PACOTES_SISTEMA_FALTANDO=()

if ! command -v python3 &> /dev/null; then
    PACOTES_SISTEMA_FALTANDO+=("python3")
fi

if ! command -v pip3 &> /dev/null && ! python3 -m pip --version &> /dev/null; then
    PACOTES_SISTEMA_FALTANDO+=("python3-pip")
fi

if ! python3 -c "import venv" &> /dev/null; then
    PACOTES_SISTEMA_FALTANDO+=("python3-venv")
fi

if ! command -v curl &> /dev/null; then
    PACOTES_SISTEMA_FALTANDO+=("curl")
fi

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

if [ ${#PACOTES_SISTEMA_FALTANDO[@]} -gt 0 ]; then
    echo -e "${AMARELO}⚠️ Dependências de sistema ausentes:${NC} ${PACOTES_SISTEMA_FALTANDO[*]}"
    echo -e "${AMARELO}🔑 Instalando componentes via apt (requer conexão à web nesta primeira execução)...${NC}\n"
    
    sudo apt-get update -y
    sudo apt-get install -y "${PACOTES_SISTEMA_FALTANDO[@]}"
    echo -e "${VERDE}✓ Dependências do sistema instaladas com sucesso!${NC}"
else
    echo -e "${VERDE}✓ Todos os softwares base do sistema Ubuntu estão presentes.${NC}"
fi

# ------------------------------------------------------------------------------
# 2. CONFIGURAÇÃO DO AMBIENTE VIRTUAL PYTHON
# ------------------------------------------------------------------------------
echo -e "\n${NEGRITO}[2/5] Verificando ambiente Python e bibliotecas...${NC}"

VENV_DIR="$SCRIPT_DIR/.venv"

if [ ! -d "$VENV_DIR" ] || [ ! -f "$VENV_DIR/bin/activate" ]; then
    echo -e "${CIANO}⚙️ Criando ambiente virtual Python isolado (.venv)...${NC}"
    python3 -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"

PYTHON_DEPS_FALTANDO=false
if ! python3 -c "import fastapi, uvicorn, pydantic" &> /dev/null; then
    PYTHON_DEPS_FALTANDO=true
fi

if [ "$PYTHON_DEPS_FALTANDO" = true ]; then
    echo -e "${CIANO}📥 Instalando bibliotecas do servidor web (FastAPI, Uvicorn, Pydantic)...${NC}"
    pip install --upgrade pip --quiet || true
    if [ -f "$SCRIPT_DIR/requirements.txt" ]; then
        pip install -r "$SCRIPT_DIR/requirements.txt"
    else
        pip install "fastapi>=0.100.0" "uvicorn>=0.22.0" "pydantic>=2.0.0"
    fi
    echo -e "${VERDE}✓ Bibliotecas Python instaladas com sucesso!${NC}"
else
    echo -e "${VERDE}✓ Todas as bibliotecas Python necessárias estão prontas e isoladas.${NC}"
fi

# ------------------------------------------------------------------------------
# 3. VERIFICAÇÃO DE RECURSOS OFFLINE (MEDIAPIPE, WASM, FONTES, PICTOGRAMAS)
# ------------------------------------------------------------------------------
echo -e "\n${NEGRITO}[3/5] Validando recursos estáticos locais (100% Offline)...${NC}"

OFFLINE_OK=true
if [ ! -f "$SCRIPT_DIR/static/vendor/mediapipe/camera_utils/camera_utils.js" ] || \
   [ ! -f "$SCRIPT_DIR/static/vendor/mediapipe/hands/hands.js" ] || \
   [ ! -f "$SCRIPT_DIR/static/vendor/mediapipe/hands/hands_solution_simd_wasm_bin.wasm" ] || \
   [ ! -f "$SCRIPT_DIR/static/fonts/fonts.css" ]; then
    OFFLINE_OK=false
fi

if [ "$OFFLINE_OK" = false ]; then
    echo -e "${AMARELO}⚠️ Recursos locais para funcionamento offline ausentes ou incompletos.${NC}"
    echo -e "${CIANO}📥 Executando download único de empacotamento offline (MediaPipe + Fontes)...${NC}"
    python3 "$SCRIPT_DIR/download_offline_assets.py"
    echo -e "${VERDE}✓ Recursos offline empacotados com sucesso!${NC}"
else
    echo -e "${VERDE}✓ Recursos offline presentes (MediaPipe WASM/TFLite, Fontes e Pictogramas).${NC}"
    echo -e "${VERDE}  O sistema funcionará plenamente sem qualquer dependência da internet.${NC}"
fi

# ------------------------------------------------------------------------------
# 4. DIAGNÓSTICO DE PERIFÉRICOS (WEBCAM)
# ------------------------------------------------------------------------------
echo -e "\n${NEGRITO}[4/5] Verificando dispositivo de câmera...${NC}"
if ls /dev/video* &> /dev/null; then
    echo -e "${VERDE}✓ Webcam detectada no sistema (/dev/video).${NC}"
else
    echo -e "${AMARELO}⚠️ Nenhuma câmera USB (/dev/video*) foi encontrada no momento.${NC}"
    echo -e "${AMARELO}   (Conecte a webcam para usar a visão computacional no ar).${NC}"
fi

# ------------------------------------------------------------------------------
# 5. VERIFICAÇÃO DE RESILIÊNCIA DE PORTA DE REDE (FALLBACK AUTOMÁTICO)
# ------------------------------------------------------------------------------
PORTA_PADRAO=8080
PORTA_FINAL=$PORTA_PADRAO

# Testa disponibilidade da porta utilizando Python (independente de netstat/lsof/ss)
PORTA_FINAL=$(python3 -c "
import socket
def is_port_in_use(port, host='0.0.0.0'):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((host, port))
            return False
        except OSError:
            return True

start = $PORTA_PADRAO
for p in range(start, start + 50):
    if not is_port_in_use(p):
        print(p)
        break
else:
    print($PORTA_PADRAO)
")

if [ "$PORTA_FINAL" -ne "$PORTA_PADRAO" ]; then
    echo -e "\n${AMARELO}⚠️ AVISO DE RESILIÊNCIA: A porta $PORTA_PADRAO já está em uso por outro processo.${NC}"
    echo -e "${VERDE}✓ Fallback ativado com sucesso! Usando porta livre: ${NEGRITO}$PORTA_FINAL${NC}"
fi

# ------------------------------------------------------------------------------
# 6. EXECUÇÃO DA APLICAÇÃO
# ------------------------------------------------------------------------------
echo -e "\n${CIANO}================================================================${NC}"
echo -e "${VERDE}  🚀 TUDO PRONTO! INICIANDO SERVIDOR CETAM LAB TEA...${NC}"
echo -e "${CIANO}  Acesse no navegador: ${NEGRITO}http://localhost:${PORTA_FINAL}${NC}"
echo -e "${CIANO}  Modo de operação: ${VERDE}${NEGRITO}AUTÔNOMO / 100% OFFLINE (REDE LOCAL)${NC}"
echo -e "${CIANO}  Pressione ${NEGRITO}[Ctrl + C]${CIANO} neste terminal para encerrar.${NC}"
echo -e "${CIANO}================================================================${NC}\n"

exec python3 app.py --port "$PORTA_FINAL"

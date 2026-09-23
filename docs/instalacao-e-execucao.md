# 🚀 Guia de Instalação & Operação em Rede Local

## Requisitos de Sistema

* **Sistema Operacional**: Ubuntu Linux 20.04+, Debian 11+, Windows 10/11 ou macOS.
* **Hardware Mínimo**:
  * Processador Dual-Core 2.0 GHz (i3 / Celeron ou equivalente).
  * 4 GB de Memória RAM.
  * Webcam USB básica (720p ou 1080p).
* **Software Necessário**:
  * Python 3.8 ou superior.
  * Navegador Web moderno com suporte a WebGL e WebRTC (Google Chrome, Chromium, Firefox, Brave ou Edge).

---

## Inicialização Rápida no Linux (Ubuntu/Debian)

O projeto inclui um script automatizado que valida dependências, cria ambiente virtual e inicializa a aplicação:

```bash
cd /caminho/do/projeto/maos-livres
chmod +x iniciar.sh
./iniciar.sh
```

---

## Inicialização Manual com Python

Caso prefira executar manualmente:

```bash
# 1. Criar e ativar ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Executar o servidor
python3 app.py
```

Acesse no navegador:
* Local: `http://localhost:8080`
* Na rede local da sala: `http://<IP_DO_COMPUTADOR>:8080`

---

## Operação em Rede Local Fechada (100% Offline / Sem Internet)

O sistema foi arquitetado para funcionar de forma plena em ambientes de intranet e redes educacionais ou clínicas isoladas:
* **MediaPipe Hands & Camera Utils Locais**: Todos os scripts JS, binários WebAssembly (`.wasm`), modelos neurais TFLite (`hand_landmark_full.tflite` e `hand_landmark_lite.tflite`) e pacotes de assets empacotados (`.data`, `.binarypb`) estão localizados em `static/vendor/mediapipe/`.
* **Fontes Embutidas**: As famílias *Orbitron*, *Rajdhani* e *Share Tech Mono* estão localizadas em `static/fonts/` com CSS próprio, dispensando qualquer chamada aos servidores do Google Fonts.
* **Pictogramas ARASAAC Locais**: Os 16 pictogramas de CAA estão armazenados localmente em `static/pictograms/`.
* **Sons Holográficos Nativos**: Todos os beeps e efeitos de feedback utilizam a Web Audio API sintetizada pelo navegador (sem download de áudios externos).

### Verificação de Prontidão Offline
Para validar que todos os assets locais estão integrados e prontos para uso desconectado:
```bash
python3 test_offline_readiness.py
```
Esse teste simula todas as rotas e confirma que nenhum recurso faz requisição para a internet externa.

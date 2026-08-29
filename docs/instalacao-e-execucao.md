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
* Local: `http://localhost:8000`
* Na rede local da sala: `http://<IP_DO_COMPUTADOR>:8000`

---

## Operação em Rede Local Fechada (Sem Acesso à Web)

* Todos os pictogramas ARASAAC estão armazenados localmente em `static/pictograms/`.
* O backend serve tanto a interface quanto as imagens e a persistência de logs de forma autônoma.

# ✦ Mãos Livres // JARVIS Assist TEA ✦
### Interface Holográfica Touchless com Visão Computacional para Apoio a Pessoas no Espectro Autista

> **Projeto MVP desenvolvido para o Curso Técnico em Manutenção e Suporte em Informática**  
> Inspirado na estética HUD holográfica do JARVIS e no conceito de interação no ar (*Barehands* / MediaPipe).

---

## 🌟 Visão Geral do Projeto

Este projeto é um **Laboratório de Interação Sem Toque (Touchless)** projetado para ser operado por um profissional de psicologia/saúde no acolhimento de pessoas com Transtorno do Espectro Autista (TEA) e outras neurodivergências.

A aplicação captura a imagem da webcam e a exibe em **tela cheia em modo espelho (Realidade Aumentada)**, distribuindo simultaneamente **4 Decks Holográficos nos 4 cantos da tela**, garantindo autonomia total para a pessoa no espectro autista sem depender de abas ou mouse:
* 🧘 **Canto Superior Esquerdo:** Sensorial & Conforto (Verde/Ciano)
* 💧 **Canto Inferior Esquerdo:** Necessidades Básicas (Esmeralda)
* ⚡ **Canto Superior Direito:** Expressão Rápida (Âmbar)
* 🌀 **Canto Inferior Direito:** Calmaria & Apoio (Púrpura / Respiração 4-4-4)
* 🎯 **Centro da Tela:** Livre para o reflexo do usuário, com mira holográfica e telemetria em tempo real.

---

## 🚀 Como Executar

### Opção 1: Com Servidor Python (Recomendado)
Oferece API para gravação de logs da sessão e carregamento dinâmico de cartões JSON.

```bash
# Executar o script de inicialização
./iniciar.sh

# Ou diretamente via Python:
python3 app.py
```
Acesse no navegador: **`http://localhost:8000`**

### Opção 2: Standalone (Direto no Navegador)
Basta dar dois cliques no arquivo [`index.html`](file:///home/marcelo/projetos/py/maos-livres/index.html) e abrir no Google Chrome, Brave, Edge ou Firefox (permitir acesso à webcam quando solicitado).

---

## 🖐️ Como Interagir no Ar (Barehands)

| Gesto / Ação | Movimento Real da Mão | Ação no Sistema |
| :--- | :--- | :--- |
| **Mira / Cursor** | Ponta do Dedo Indicador | Move a mira holográfica neon e destaca o cartão com iluminação. |
| **Acionar Cartão / Botão** | Fazer gesto de Pinça (Polegar + Indicador) sobre o item | Dispara o acionamento imediato com som sci-fi e sintetizador de voz. |
| **Mover Janela Holográfica** | Fazer gesto de Pinça sobre a barra superior | Segura e arrasta a janela holográfica pelo ar para reposicionar. |
| **Atalho do Profissional** | Pressionar tecla `[P]` | Abre a gaveta lateral com histórico da sessão e calibração de sensibilidade. |

---

## 📁 Estrutura de Arquivos

* [`index.html`](file:///home/marcelo/projetos/py/maos-livres/index.html): Interface web completa, HUD futurista, integração MediaPipe Hands e sintetizadores de voz/áudio.
* [`app.py`](file:///home/marcelo/projetos/py/maos-livres/app.py): Servidor web em Python (FastAPI/Uvicorn) com API REST para logs e cartões.
* [`cards.json`](file:///home/marcelo/projetos/py/maos-livres/cards.json): Base de dados das categorias e frases de Comunicação Aumentativa e Alternativa (CAA).
* [`iniciar.sh`](file:///home/marcelo/projetos/py/maos-livres/iniciar.sh): Script de execução simplificada para Linux/Mac.
* [`GUIA_DIDATICO_CURSO_TECNICO.md`](file:///home/marcelo/projetos/py/maos-livres/GUIA_DIDATICO_CURSO_TECNICO.md): Roteiro pedagógico completo com conceitos de hardware, visão computacional e acessibilidade.
* [`inspirado-holograma-jarvis.png`](file:///home/marcelo/projetos/py/maos-livres/inspirado-holograma-jarvis.png): Imagem de referência da interface flutuante.

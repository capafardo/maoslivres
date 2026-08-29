# ✦ cetam lab tea ✦
### Interface Holográfica Touchless com Visão Computacional para Apoio a Pessoas no Espectro Autista

> **Projeto MVP desenvolvido para o Curso Técnico em Manutenção e Suporte em Informática - CETAM**  
> *CETAM - Centro de Educação Tecnológica do Amazonas* | *IBC - Instituto Benjamin Constant*  
> Interface espacial nos 4 quadrantes para acessibilidade (*Barehands* / MediaPipe / ARASAAC CAA).

---

![Screenshot Conceitual do Projeto](screenshot-conceitual.png)

---

## 📚 Documentação Técnica Completa

Toda a documentação detalhada do projeto está centralizada na pasta [`docs/`](docs/):

* [📑 **Sumário Executivo e Visão Geral**](docs/index.md)
* [🏛️ **Arquitetura Técnica & Pipeline de IA**](docs/arquitetura.md)
* [🖼️ **Comunicação Aumentativa e Alternativa (CAA) & ARASAAC**](docs/comunicacao-caa-arasaac.md)
* [🖐️ **Visão Computacional, Gestos & Filtros Espaciais**](docs/gestos-e-visao-computacional.md)
* [👩‍🏫 **Guia do Profissional & Mediador**](docs/guia-do-profissional.md)
* [🔌 **Referência da API & Endpoints FastAPI**](docs/api-e-rotas.md)
* [🚀 **Guia de Instalação & Operação em Rede Local**](docs/instalacao-e-execucao.md)

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
Basta dar dois cliques no arquivo [`index.html`](index.html) e abrir no Google Chrome, Brave, Edge ou Firefox (permitir acesso à webcam quando solicitado).

---

## 🖐️ Como Interagir no Ar & Atalhos

| Gesto / Ação | Movimento Real da Mão / Teclado | Ação no Sistema |
| :--- | :--- | :--- |
| **Mira / Cursor** | Ponta do Dedo Indicador | Move a mira holográfica neon e destaca o cartão com iluminação. |
| **Acionar Cartão / Botão** | Fazer gesto de Pinça (Polegar + Indicador) sobre o item | Dispara o acionamento imediato com som sci-fi e sintetizador de voz. |
| **Mover Janela Holográfica** | Fazer gesto de Pinça sobre a barra superior | Segura e arrasta a janela holográfica pelo ar para reposicionar. |
| **Alternar Modo CAA [M]** | Pressionar tecla `[M]` ou botão no HUD | Alterna entre **Modo Pictogramas (ARASAAC)** e **Modo Texto (Padrão)**. |
| **Painel do Profissional [P]** | Pressionar tecla `[P]` ou botão no HUD | Abre a gaveta lateral com histórico da sessão, Modo Eco e calibrações. |
| **Alternar Terminal HUD [L]** | Pressionar tecla `[L]` | Alterna a visibilidade do stream de manifestações central na tela. |

---

## 🛡️ Estabilidade, Filtros & Recursos Clínicos

* **Filtro de Foco no Aluno Principal:** Algoritmo que calcula proximidade, escala da mão e continuidade temporal, descartando movimentos de mediadores ou pessoas ao fundo da sala.
* **Cooldown de 10 Segundos:** Após uma seleção, o sistema bloqueia novos disparos acidentais por 10 segundos com contagem regressiva visual no cursor e no banner.
* **Estabilização de Pinça (~120ms):** Exige confirmação estável de gesto contínuo, eliminando 100% dos falsos positivos causados por ruído ou acenos rápidos.
* **Modo Eco Inteligente:** Alterna dinamicamente para MediaPipe Lite e otimiza a pipeline de GPU para computadores básicos garantindo 60 FPS fluidos.

---

## 📁 Estrutura de Arquivos

* [`index.html`](index.html): Interface web completa, HUD futurista, integração MediaPipe Hands, modos CAA/Texto e áudio.
* [`app.py`](app.py): Servidor web em Python (FastAPI/Uvicorn) com API REST e montagem de arquivos estáticos offline.
* [`screenshot-conceitual.png`](screenshot-conceitual.png): Screenshot conceitual em alta definição da interface touchless e CAA.
* [`docs/`](docs/): Pasta completa de documentação técnica, pedagógica e arquitetural.
* [`static/pictograms/`](static/pictograms/): Catálogo local de 16 pictogramas oficiais ARASAAC para uso offline.
* [`cards.json`](cards.json): Base de dados das categorias, frases e mapeamento dos pictogramas ARASAAC.
* [`iniciar.sh`](iniciar.sh): Script de execução simplificada para Linux/Mac.
* [`GUIA_DIDATICO_CURSO_TECNICO.md`](GUIA_DIDATICO_CURSO_TECNICO.md): Roteiro pedagógico completo com conceitos de hardware, visão computacional e acessibilidade.


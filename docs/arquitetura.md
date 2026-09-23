# 🏛️ Arquitetura Técnica & Pipeline de IA

## Visão Geral do Sistema

O **CETAM LAB TEA** é composto por uma arquitetura cliente-servidor leve, concebida para execução em redes locais isoladas (intranet / offline) com baixo consumo de recursos de hardware.

```
┌─────────────────────────────────────────────────────────────┐
│                    NAVEGADOR CLIENTE                        │
│                                                             │
│  ┌─────────────────┐   Webcam Video   ┌──────────────────┐  │
│  │ Espelho AR (Vid)│ ───────────────> │ MediaPipe Hands  │  │
│  └─────────────────┘                  │ (2 Mãos / 3D)    │  │
│           │                           └──────────────────┘  │
│           │                                    │            │
│           ▼                                    ▼            │
│  ┌─────────────────┐                  ┌──────────────────┐  │
│  │ Canvas HUD 60FPS│ <─────────────── │ Filtro Espacial  │  │
│  │ (Retícula/Mãos) │   Cursor + Pinch │ & Lock Temporal  │  │
│  └─────────────────┘                  └──────────────────┘  │
│           │                                    │            │
│           ▼                                    ▼            │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ Decks dos 4 Quadrantes (CSS3 3D / ARASAAC / Texto)     │  │
│  └───────────────────────────────────────────────────────┘  │
│           │                                                 │
│           ▼                                                 │
│  ┌─────────────────┐                  ┌──────────────────┐  │
│  │ Web Speech Synth│                  │ Cooldown Manager │  │
│  │ (Voz PT-BR)     │                  │ (10s Anti-Spam)  │  │
│  └─────────────────┘                  └──────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                               ▲
                    HTTP / REST API (FastAPI)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                    SERVIDOR LOCAL FASTAPI                   │
│                                                             │
│  - /api/cards  (Leitura/Gravação de Cartões)                │
│  - /api/logs   (Registro e Histórico de Manifestações)      │
│  - /static     (Vendor MediaPipe WASM/TFLite, Fontes e CAA) │
└─────────────────────────────────────────────────────────────┘
```

## Componentes Técnicos

1. **Front-End Holográfico (`index.html`)**:
   * **Espelho AR de Fundo**: WebRTC (`navigator.mediaDevices.getUserMedia`) renderizado com inversão horizontal (`scaleX(-1)`) e contraste adaptativo.
   * **Canvas HUD de Telemetria**: Renderização a 60 FPS da malha de 21 pontos das mãos e cursor de mira espacial.
   * **Motor de Áudio Dual**:
     * Síntese de Voz Web Speech API em Português do Brasil (`pt-BR`).
     * Síntese de Áudio Construtiva via Web Audio API (tons senoidais puros para beeps e chimes agradáveis sem sobrecarga sensorial).

2. **Back-End de Persistência e Serviços (`app.py`)**:
   * Desenvolvido em **Python 3 / FastAPI** de altíssima performance assíncrona.
   * Não requer bancos de dados complexos: utiliza JSON estruturado (`cards.json` e `logs_sessao.json`) com gravação atômica.
   * Servidor estático dedicado para os pictogramas ARASAAC em `static/pictograms/`.

#!/usr/bin/env python3
"""
MÃOS LIVRES - cetam lab tea
Servidor Web e API em Python para a Interface Holográfica de Apoio a Pessoas no Espectro Autista.

Curso Técnico em Manutenção e Suporte em Informática / Laboratório de Apoio TEA.
"""

import sys
import os
import json
import socket
import webbrowser
from datetime import datetime
from typing import List, Optional
from pathlib import Path

try:
    from fastapi import FastAPI, HTTPException, Request
    from fastapi.staticfiles import StaticFiles
    from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel
    import uvicorn
except ImportError:
    print("FastAPI / Uvicorn não encontrados. Por favor instale: pip install fastapi uvicorn")
    raise

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
STATIC_DIR.mkdir(exist_ok=True)
CARDS_FILE = BASE_DIR / "cards.json"
LOGS_FILE = BASE_DIR / "logs_sessao.json"

app = FastAPI(
    title="cetam lab tea",
    description="Sistema de Interface Holográfica Touchless com Visão Computacional para Apoio a Alunos com TEA",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Modelos de Dados
class LogEvent(BaseModel):
    card_id: Optional[str] = "custom"
    label: str
    texto: str
    categoria: Optional[str] = "Geral"
    tipo: Optional[str] = "neutro"
    icone: Optional[str] = "💬"
    pictograma: Optional[str] = None
    timestamp: Optional[str] = None
    origem: Optional[str] = "gesto_mao"

class CardItem(BaseModel):
    id: str
    label: str
    texto: str
    tipo: str = "neutro"
    icone: str = "💬"
    cor_custom: Optional[str] = None
    pictograma: Optional[str] = None
    arasaac_id: Optional[str] = None

class CategoryItem(BaseModel):
    id: str
    nome: str
    icone: str
    cor: str
    posicao: Optional[str] = None
    cards: List[CardItem]

class CardsPayload(BaseModel):
    categories: List[CategoryItem]


def load_cards() -> dict:
    if not CARDS_FILE.exists():
        default_data = {
            "categories": [
                {
                    "id": "sensorial",
                    "nome": "Sensorial & Conforto",
                    "icone": "🧘",
                    "cor": "#00f0ff",
                    "cards": [
                        { "id": "s1", "label": "Estou Confortável", "texto": "Estou me sentindo confortável e bem no ambiente.", "tipo": "sucesso", "icone": "🟢" },
                        { "id": "s2", "label": "Muito Barulho", "texto": "O ambiente está muito barulhento, peço para diminuir o som.", "tipo": "alerta", "icone": "🔊" },
                        { "id": "s3", "label": "Muita Luz", "texto": "A iluminação está forte para mim, peço para ajustar a luz.", "tipo": "alerta", "icone": "💡" },
                        { "id": "s4", "label": "Preciso de Pausa", "texto": "Estou sobrecarregado, necessito de um momento de descanso.", "tipo": "urgente", "icone": "🛑" }
                    ]
                }
            ]
        }
        save_cards(default_data)
        return default_data
    with open(CARDS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_cards(data: dict):
    with open(CARDS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_logs() -> list:
    if not LOGS_FILE.exists():
        return []
    try:
        with open(LOGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_logs(logs: list):
    with open(LOGS_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)


@app.get("/", response_class=HTMLResponse)
async def get_index():
    index_file = BASE_DIR / "index.html"
    if not index_file.exists():
        raise HTTPException(status_code=404, detail="index.html não encontrado")
    return FileResponse(index_file, headers={"Cache-Control": "no-cache, no-store, must-revalidate", "Pragma": "no-cache"})

@app.get("/api/cards")
async def get_cards():
    """Retorna a lista de categorias e cartões de comunicação."""
    return load_cards()

@app.post("/api/cards")
async def update_cards(payload: CardsPayload):
    """Atualiza a lista de cartões (permitindo ao psicólogo/profissional personalizar)."""
    data = payload.model_dump() if hasattr(payload, "model_dump") else payload.dict()
    save_cards(data)
    return {"status": "success", "message": "Cartões atualizados com sucesso"}

@app.get("/api/logs")
@app.get("/api/log")
async def get_logs():
    """Retorna o histórico de manifestações e interações da sessão."""
    return load_logs()

@app.post("/api/logs")
@app.post("/api/log")
async def add_log(event: LogEvent):
    """Registra uma nova interação do usuário (via gesto ou clique)."""
    logs = load_logs()
    event_dict = event.model_dump() if hasattr(event, "model_dump") else event.dict()
    if not event_dict.get("timestamp"):
        event_dict["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logs.append(event_dict)
    save_logs(logs)
    print(f"[{event_dict['timestamp']}] Manifestação registrada: [{event_dict.get('categoria')}] {event_dict.get('label')} -> \"{event_dict.get('texto')}\"")
    return {"status": "success", "logged": event_dict}

@app.delete("/api/logs")
async def clear_logs():
    """Limpa os registros da sessão atual."""
    save_logs([])
    return {"status": "success", "message": "Histórico de logs reiniciado"}

@app.get("/inspirado-holograma-jarvis.png")
async def get_reference_image():
    img_path = BASE_DIR / "inspirado-holograma-jarvis.png"
    if img_path.exists():
        return FileResponse(img_path)
    raise HTTPException(status_code=404, detail="Imagem não encontrada")


def is_port_in_use(port: int, host: str = "0.0.0.0") -> bool:
    """Verifica se uma porta de rede já está ocupada no host."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((host, port))
            return False
        except OSError:
            return True

def find_available_port(start_port: int = 8080, max_attempts: int = 50, host: str = "0.0.0.0") -> int:
    """Busca sequencialmente a próxima porta TCP disponível."""
    for p in range(start_port, start_port + max_attempts):
        if not is_port_in_use(p, host):
            return p
    return start_port


def run(host: str = "0.0.0.0", port: int = 8080, open_browser: bool = True):
    if is_port_in_use(port, host):
        nova_porta = find_available_port(start_port=port, host=host)
        print("!" * 70)
        print(f"⚠️  RESILIÊNCIA: A porta {port} já está em uso por outro serviço!")
        print(f"🔄 Redirecionando automaticamente para a porta livre: {nova_porta}")
        print("!" * 70)
        port = nova_porta

    print("=" * 70)
    print("🚀 cetam lab tea (100% Offline / Intranet)")
    print("   Laboratório de Informática / Acessibilidade Touchless")
    print(f"   Servidor rodando em: http://localhost:{port}")
    print(f"   Acesse na rede local em: http://0.0.0.0:{port}")
    print("=" * 70)
    
    if open_browser:
        try:
            webbrowser.open(f"http://localhost:{port}")
        except Exception:
            pass

    uvicorn.run(app, host=host, port=port, log_level="info")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Executar servidor cetam lab tea")
    parser.add_argument("--port", type=int, default=8080, help="Porta HTTP (padrão: 8080)")
    parser.add_argument("--no-browser", action="store_true", help="Não abrir o navegador automaticamente")
    args = parser.parse_args()
    
    run(port=args.port, open_browser=not args.no_browser)

#!/usr/bin/env python3
"""
Teste de Verificação de Prontidão Offline (Offline Readiness Test)
Inicia o servidor FastAPI em uma porta de teste e valida via urllib.request
se todos os assets necessários para o MediaPipe, Fontes e Pictogramas respondem HTTP 200.
"""

import sys
import time
import threading
import urllib.request
import urllib.error
import uvicorn
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

RESOURCES_TO_CHECK = [
    # Página Principal
    ("/", 200),
    
    # API
    ("/api/cards", 200),
    ("/api/logs", 200),
    
    # Scripts do MediaPipe
    ("/static/vendor/mediapipe/camera_utils/camera_utils.js", 200),
    ("/static/vendor/mediapipe/hands/hands.js", 200),
    ("/static/vendor/mediapipe/hands/hands_solution_packed_assets_loader.js", 200),
    ("/static/vendor/mediapipe/hands/hands_solution_simd_wasm_bin.js", 200),
    ("/static/vendor/mediapipe/hands/hands_solution_wasm_bin.js", 200),
    
    # Binários e Modelos do MediaPipe
    ("/static/vendor/mediapipe/hands/hands_solution_simd_wasm_bin.wasm", 200),
    ("/static/vendor/mediapipe/hands/hands_solution_wasm_bin.wasm", 200),
    ("/static/vendor/mediapipe/hands/hand_landmark_full.tflite", 200),
    ("/static/vendor/mediapipe/hands/hand_landmark_lite.tflite", 200),
    ("/static/vendor/mediapipe/hands/hands.binarypb", 200),
    ("/static/vendor/mediapipe/hands/hands_solution_packed_assets.data", 200),

    # Folha de Estilos e Fontes Locais
    ("/static/fonts/fonts.css", 200),
    ("/static/fonts/orbitron-400.woff2", 200),
    ("/static/fonts/rajdhani-500.woff2", 200),
    ("/static/fonts/share-tech-mono-400.woff2", 200),

    # Pictogramas ARASAAC
    ("/static/pictograms/s1_confortavel.png", 200),
    ("/static/pictograms/n1_agua.png", 200),
    ("/static/pictograms/e1_sim.png", 200),
    ("/static/pictograms/c1_respirar.png", 200),
]

def run_server():
    from app import app
    config = uvicorn.Config(app=app, host="127.0.0.1", port=8999, log_level="warning")
    server = uvicorn.Server(config)
    server.run()

def run_tests():
    print("🚀 Subindo servidor de testes temporário na porta 8999...")
    srv_thread = threading.Thread(target=run_server, daemon=True)
    srv_thread.start()

    # Aguarda o servidor responder
    base_url = "http://127.0.0.1:8999"
    ready = False
    for _ in range(20):
        try:
            with urllib.request.urlopen(base_url, timeout=1) as resp:
                if resp.status == 200:
                    ready = True
                    break
        except Exception:
            time.sleep(0.2)

    if not ready:
        print("❌ Não foi possível iniciar o servidor de testes.")
        return 1

    print("🧪 Verificando entrega de todos os recursos locais...")
    failed = 0
    for path, expected_status in RESOURCES_TO_CHECK:
        url = f"{base_url}{path}"
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=5) as resp:
                status = resp.status
                content = resp.read()
                size = len(content)
                ct = resp.headers.get("Content-Type", "")
                if status == expected_status and size > 0:
                    print(f"  ✓ OK: {path} [{status}] ({size:,} bytes, {ct})")
                else:
                    print(f"  ❌ FALHA: {path} status {status}, tamanho {size}")
                    failed += 1
        except urllib.error.HTTPError as e:
            print(f"  ❌ HTTP ERROR {e.code} em {path}")
            failed += 1
        except Exception as e:
            print(f"  ❌ ERRO em {path}: {e}")
            failed += 1

    # Testa se o index.html contém referências remotas HTTP/HTTPS
    try:
        with urllib.request.urlopen(f"{base_url}/", timeout=5) as resp:
            html = resp.read().decode("utf-8")
            import re
            remote_matches = re.findall(r'(https?://[^\s"\'<>]+)', html)
            # Ignora schema de xml se houver
            remote_matches = [m for m in remote_matches if not m.startswith("http://www.w3.org")]
            if remote_matches:
                print("\n❌ ERRO: O index.html servido ainda contém URLs remotas:")
                for m in remote_matches:
                    print(f"    - {m}")
                failed += len(remote_matches)
            else:
                print("\n✓ index.html verificado: NENHUMA dependência externa encontrada.")
    except Exception as e:
        print(f"❌ Erro ao validar index.html: {e}")
        failed += 1

    if failed == 0:
        print("\n🎉 TODOS OS TESTES PASSARAM COM SUCESSO! APLICAÇÃO 100% PRONTA PARA OPERAÇÃO OFFLINE.")
        return 0
    else:
        print(f"\n❌ {failed} testes falharam.")
        return 1

if __name__ == "__main__":
    sys.exit(run_tests())

#!/usr/bin/env python3
"""
Script de Download e Empacotamento de Recursos Offline
Garante que todo o MediaPipe Hands, Camera Utils e Fontes Google estejam
armazenados localmente no diretório static/ para operação 100% autônoma.
"""

import os
import sys
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
VENDOR_DIR = STATIC_DIR / "vendor" / "mediapipe"
FONTS_DIR = STATIC_DIR / "fonts"

MEDIAPIPE_VERSION = "0.4.1675469240"
CAMERA_UTILS_VERSION = "0.3.1675466862"

CAMERA_UTILS_FILES = [
    "camera_utils.js",
]

HANDS_FILES = [
    "hands.js",
    "hands.binarypb",
    "hands_solution_packed_assets.data",
    "hands_solution_packed_assets_loader.js",
    "hands_solution_simd_wasm_bin.data",
    "hands_solution_simd_wasm_bin.js",
    "hands_solution_simd_wasm_bin.wasm",
    "hands_solution_wasm_bin.js",
    "hands_solution_wasm_bin.wasm",
    "hand_landmark_full.tflite",
    "hand_landmark_lite.tflite",
]

FONTS_MAPPING = [
    {
        "family": "Orbitron",
        "weight": "400",
        "style": "normal",
        "filename": "orbitron-400.woff2",
        "url": "https://fonts.gstatic.com/s/orbitron/v35/yMJRMIlzdpvBhQQL_Qq7dy0.woff2"
    },
    {
        "family": "Orbitron",
        "weight": "600",
        "style": "normal",
        "filename": "orbitron-600.woff2",
        "url": "https://fonts.gstatic.com/s/orbitron/v35/yMJRMIlzdpvBhQQL_Qq7dy0.woff2"
    },
    {
        "family": "Orbitron",
        "weight": "800",
        "style": "normal",
        "filename": "orbitron-800.woff2",
        "url": "https://fonts.gstatic.com/s/orbitron/v35/yMJRMIlzdpvBhQQL_Qq7dy0.woff2"
    },
    {
        "family": "Rajdhani",
        "weight": "500",
        "style": "normal",
        "filename": "rajdhani-500.woff2",
        "url": "https://fonts.gstatic.com/s/rajdhani/v17/LDI2apCSOBg7S-QT7pb0EPOreec.woff2"
    },
    {
        "family": "Rajdhani",
        "weight": "600",
        "style": "normal",
        "filename": "rajdhani-600.woff2",
        "url": "https://fonts.gstatic.com/s/rajdhani/v17/LDI2apCSOBg7S-QT7pbYF_Oreec.woff2"
    },
    {
        "family": "Rajdhani",
        "weight": "700",
        "style": "normal",
        "filename": "rajdhani-700.woff2",
        "url": "https://fonts.gstatic.com/s/rajdhani/v17/LDI2apCSOBg7S-QT7pa8FvOreec.woff2"
    },
    {
        "family": "Share Tech Mono",
        "weight": "400",
        "style": "normal",
        "filename": "share-tech-mono-400.woff2",
        "url": "https://fonts.gstatic.com/s/sharetechmono/v16/J7aHnp1uDWRBEqV98dVQztYldFcLowEF.woff2"
    }
]

def download_file(url: str, dest_path: Path):
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    if dest_path.exists() and dest_path.stat().st_size > 0:
        print(f"  [OK] Já presente: {dest_path.name} ({dest_path.stat().st_size:,} bytes)")
        return
    
    print(f"  [BAIXANDO] {dest_path.name} de {url}...")
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp, open(dest_path, "wb") as f:
        while chunk := resp.read(65536):
            f.write(chunk)
    print(f"  ✓ Salvo: {dest_path.name} ({dest_path.stat().st_size:,} bytes)")

def setup_mediapipe():
    print("\n📦 1. Configurando MediaPipe Camera Utils...")
    camera_dir = VENDOR_DIR / "camera_utils"
    for f in CAMERA_UTILS_FILES:
        url = f"https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils@{CAMERA_UTILS_VERSION}/{f}"
        download_file(url, camera_dir / f)

    print("\n📦 2. Configurando MediaPipe Hands (JS, WASM, Modelos TFLite)...")
    hands_dir = VENDOR_DIR / "hands"
    for f in HANDS_FILES:
        url = f"https://cdn.jsdelivr.net/npm/@mediapipe/hands@{MEDIAPIPE_VERSION}/{f}"
        download_file(url, hands_dir / f)

def setup_fonts():
    print("\n🎨 3. Configurando Fontes Locais (Orbitron, Rajdhani, Share Tech Mono)...")
    FONTS_DIR.mkdir(parents=True, exist_ok=True)
    
    for font in FONTS_MAPPING:
        dest = FONTS_DIR / font["filename"]
        download_file(font["url"], dest)

    css_content = """/* Fontes locais empacotadas para operação 100% offline */

@font-face {
  font-family: 'Orbitron';
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url('/static/fonts/orbitron-400.woff2') format('woff2');
}

@font-face {
  font-family: 'Orbitron';
  font-style: normal;
  font-weight: 600;
  font-display: swap;
  src: url('/static/fonts/orbitron-600.woff2') format('woff2');
}

@font-face {
  font-family: 'Orbitron';
  font-style: normal;
  font-weight: 800;
  font-display: swap;
  src: url('/static/fonts/orbitron-800.woff2') format('woff2');
}

@font-face {
  font-family: 'Rajdhani';
  font-style: normal;
  font-weight: 500;
  font-display: swap;
  src: url('/static/fonts/rajdhani-500.woff2') format('woff2');
}

@font-face {
  font-family: 'Rajdhani';
  font-style: normal;
  font-weight: 600;
  font-display: swap;
  src: url('/static/fonts/rajdhani-600.woff2') format('woff2');
}

@font-face {
  font-family: 'Rajdhani';
  font-style: normal;
  font-weight: 700;
  font-display: swap;
  src: url('/static/fonts/rajdhani-700.woff2') format('woff2');
}

@font-face {
  font-family: 'Share Tech Mono';
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url('/static/fonts/share-tech-mono-400.woff2') format('woff2');
}
"""
    css_path = FONTS_DIR / "fonts.css"
    with open(css_path, "w", encoding="utf-8") as f:
        f.write(css_content)
    print(f"  ✓ Arquivo de estilos gerado: {css_path.name}")

def verify_all():
    print("\n🔍 4. Verificando integridade dos recursos...")
    all_ok = True
    
    # Checa camera_utils
    cam_file = VENDOR_DIR / "camera_utils" / "camera_utils.js"
    if not cam_file.exists() or cam_file.stat().st_size == 0:
        print(f"  ❌ Faltando: {cam_file}")
        all_ok = False
        
    # Checa hands
    for f in HANDS_FILES:
        path = VENDOR_DIR / "hands" / f
        # hands_solution_simd_wasm_bin.data can be 0 bytes by design in the npm package
        if not path.exists():
            print(f"  ❌ Faltando: {path}")
            all_ok = False
            
    # Checa fontes
    for font in FONTS_MAPPING:
        path = FONTS_DIR / font["filename"]
        if not path.exists() or path.stat().st_size == 0:
            print(f"  ❌ Faltando: {path}")
            all_ok = False
            
    css_path = FONTS_DIR / "fonts.css"
    if not css_path.exists() or css_path.stat().st_size == 0:
        print(f"  ❌ Faltando: {css_path}")
        all_ok = False

    if all_ok:
        print("\n✅ SUCESSO: Todos os recursos locais estão devidamente empacotados e prontos!")
        print("   A aplicação pode operar de forma plena em rede local isolada (sem acesso à web).")
    else:
        print("\n❌ ERRO: Alguns recursos não puderam ser verificados.")
        sys.exit(1)

if __name__ == "__main__":
    setup_mediapipe()
    setup_fonts()
    verify_all()

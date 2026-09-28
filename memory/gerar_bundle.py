"""Gera /app/ELO_BEAUTY_CARE_PROJETO_COMPLETO.py — projeto inteiro em um único arquivo autoextraível."""

import os
from pathlib import Path

RAIZ = Path("/app")
SAIDA = RAIZ / "ELO_BEAUTY_CARE_PROJETO_COMPLETO.py"

INCLUIR_RAIZ = ["README.md", "INTEGRACAO_WHATSAPP.md", "auth_testing.md", ".gitignore"]
INCLUIR_DIRS = ["backend", "frontend", ".vscode"]
EXCLUIR_DIRS = {"node_modules", "__pycache__", ".pytest_cache", ".ruff_cache", ".git", "build", "dist"}
EXCLUIR_ARQUIVOS = {".env", "yarn.lock", "package-lock.json", "README.md"}  # README do frontend (CRA) fica de fora
EXTENSOES_TEXTO = {".py", ".js", ".jsx", ".css", ".json", ".md", ".html", ".txt", ".ini", ".example", ".gitignore", ".cfg", ".toml", ".svg", ".ico"}


def coletar() -> list[Path]:
    arquivos = [RAIZ / a for a in INCLUIR_RAIZ if (RAIZ / a).exists()]
    for d in INCLUIR_DIRS:
        for caminho in sorted((RAIZ / d).rglob("*")):
            if not caminho.is_file():
                continue
            if any(parte in EXCLUIR_DIRS for parte in caminho.relative_to(RAIZ).parts):
                continue
            if caminho.name in EXCLUIR_ARQUIVOS and caminho.parent != RAIZ:
                continue
            arquivos.append(caminho)
    return arquivos


def main() -> None:
    partes = []
    total = 0
    for caminho in coletar():
        rel = caminho.relative_to(RAIZ).as_posix()
        try:
            conteudo = caminho.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            print("pulando binário:", rel)
            continue
        assert "'''" not in conteudo, f"{rel} contém ''' — ajuste o delimitador"
        partes.append(f"===== FILE: {rel} =====\n{conteudo}")
        total += 1
        print(f"  + {rel}")

    corpo = "\n".join(partes)
    if corpo.endswith("\\"):
        corpo += "\n"

    cabecalho = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ELO BEAUTY CARE — PROJETO COMPLETO EM UM ÚNICO ARQUIVO
======================================================
React (frontend) + FastAPI (backend) + MongoDB + IA Claude Sonnet 4.5 + Google Auth + WhatsApp.

COMO USAR
---------
1. Salve este arquivo em qualquer pasta do seu computador.
2. Abra um terminal nessa pasta e rode:

       python ELO_BEAUTY_CARE_PROJETO_COMPLETO.py

   (opcional: informe a pasta de destino →  python ELO_BEAUTY_CARE_PROJETO_COMPLETO.py minha-pasta)

3. A pasta  elo-beauty-care/  será criada com toda a estrutura ({total} arquivos):
       backend/   frontend/   .vscode/   README.md   INTEGRACAO_WHATSAPP.md ...
4. Abra a pasta no VS Code e siga o README.md ("Rodando no VS Code (local)").

Cada arquivo do projeto aparece abaixo, na íntegra, precedido de uma linha
"===== FILE: caminho/do/arquivo =====" — você também pode ler/copiar direto daqui.
"""

import sys
from pathlib import Path

MARCADOR = "===== FILE: "
DESTINO_PADRAO = "elo-beauty-care"


def extrair(destino: Path) -> int:
    blocos = ARQUIVOS.split(MARCADOR)[1:]
    for bloco in blocos:
        cabecalho, _, conteudo = bloco.partition("\\n")
        caminho_rel = cabecalho.replace("=====", "").strip()
        if conteudo.endswith("\\n"):
            conteudo = conteudo[:-1]  # remove o separador entre arquivos
        alvo = destino / caminho_rel
        alvo.parent.mkdir(parents=True, exist_ok=True)
        alvo.write_text(conteudo, encoding="utf-8")
        print("  +", caminho_rel)
    return len(blocos)


def main() -> None:
    destino = Path(sys.argv[1] if len(sys.argv) > 1 else DESTINO_PADRAO).resolve()
    if destino.exists() and any(destino.iterdir()):
        resposta = input(f"A pasta {{destino}} já existe e não está vazia. Sobrescrever arquivos? [s/N] ")
        if resposta.strip().lower() not in ("s", "sim", "y", "yes"):
            print("Cancelado.")
            return
    destino.mkdir(parents=True, exist_ok=True)
    print(f"Extraindo para {{destino}} ...")
    n = extrair(destino)
    print(f"\\nPronto! {{n}} arquivos criados.")
    print("Próximos passos:")
    print(f"  1. cd {{destino}}")
    print("  2. Copie backend/.env.example → backend/.env e frontend/.env.example → frontend/.env e preencha")
    print("  3. Siga o README.md para instalar dependências e rodar backend (8001) e frontend (3000)")


ARQUIVOS = r\'\'\'
'''
    rodape = "\n'''\n\n\nif __name__ == \"__main__\":\n    main()\n"

    SAIDA.write_text(cabecalho + corpo + rodape, encoding="utf-8")
    print(f"\\nGerado: {SAIDA} ({total} arquivos, {SAIDA.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()

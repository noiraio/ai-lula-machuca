"""Gera /app/CODIGO_COMPLETO.md — cada arquivo do projeto em sua própria seção, pronto para copiar/colar no VS Code."""

from pathlib import Path

RAIZ = Path("/app")
LOCAL = RAIZ / "memory" / "local-frontend"
SAIDA = RAIZ / "CODIGO_COMPLETO.md"

LANG = {".py": "python", ".js": "javascript", ".jsx": "jsx", ".css": "css", ".json": "json", ".html": "html", ".md": "markdown", ".txt": "text", ".ini": "ini", ".example": "bash"}

# (título da seção, [(caminho no projeto, origem)])
SECOES = [
    ("1. Raiz do projeto", [
        ("README.md", RAIZ / "README.md"),
        ("INTEGRACAO_WHATSAPP.md", RAIZ / "INTEGRACAO_WHATSAPP.md"),
        (".gitignore", RAIZ / ".gitignore"),
        (".vscode/launch.json", RAIZ / ".vscode/launch.json"),
        (".vscode/settings.json", RAIZ / ".vscode/settings.json"),
        (".vscode/extensions.json", RAIZ / ".vscode/extensions.json"),
    ]),
    ("2. Backend — configuração", [
        ("backend/requirements.txt", RAIZ / "backend/requirements.txt"),
        ("backend/.env.example", RAIZ / "backend/.env.example"),
        ("backend/pytest.ini", RAIZ / "backend/pytest.ini"),
        ("backend/server.py", RAIZ / "backend/server.py"),
    ]),
    ("3. Backend — app/ (núcleo)", [
        ("backend/app/__init__.py", RAIZ / "backend/app/__init__.py"),
        ("backend/app/config.py", RAIZ / "backend/app/config.py"),
        ("backend/app/db.py", RAIZ / "backend/app/db.py"),
        ("backend/app/crud.py", RAIZ / "backend/app/crud.py"),
        ("backend/app/dependencies.py", RAIZ / "backend/app/dependencies.py"),
    ]),
    ("4. Backend — app/schemas/", [(f"backend/app/schemas/{n}", RAIZ / f"backend/app/schemas/{n}") for n in
        ["__init__.py", "usuario.py", "agendamento.py", "servico.py", "insumo.py", "profissional.py", "estoque.py", "financeiro.py", "debito.py", "lembrete.py", "ai.py"]]),
    ("5. Backend — app/services/", [(f"backend/app/services/{n}", RAIZ / f"backend/app/services/{n}") for n in
        ["__init__.py", "auth.py", "ai.py", "lembretes.py", "whatsapp.py"]]),
    ("6. Backend — app/routers/", [(f"backend/app/routers/{n}", RAIZ / f"backend/app/routers/{n}") for n in
        ["__init__.py", "auth.py", "agendamentos.py", "servicos.py", "insumos.py", "profissionais.py", "estoque.py", "financeiro.py", "dashboard.py", "debitos.py", "lembretes.py", "ai.py"]]),
    ("7. Frontend — configuração (versão local simplificada)", [
        ("frontend/package.json", LOCAL / "package.json"),
        ("frontend/craco.config.js", LOCAL / "craco.config.js"),
        ("frontend/jsconfig.json", RAIZ / "frontend/jsconfig.json"),
        ("frontend/.env.example", RAIZ / "frontend/.env.example"),
        ("frontend/.gitignore", RAIZ / "frontend/.gitignore"),
        ("frontend/public/index.html", LOCAL / "index.html"),
    ]),
    ("8. Frontend — src/ (núcleo)", [
        ("frontend/src/index.js", RAIZ / "frontend/src/index.js"),
        ("frontend/src/App.js", RAIZ / "frontend/src/App.js"),
        ("frontend/src/App.css", RAIZ / "frontend/src/App.css"),
        ("frontend/src/index.css", RAIZ / "frontend/src/index.css"),
        ("frontend/src/lib/api.js", RAIZ / "frontend/src/lib/api.js"),
        ("frontend/src/context/AuthContext.jsx", RAIZ / "frontend/src/context/AuthContext.jsx"),
        ("frontend/src/context/ToastContext.jsx", RAIZ / "frontend/src/context/ToastContext.jsx"),
    ]),
    ("9. Frontend — src/components/", [(f"frontend/src/components/{n}", RAIZ / f"frontend/src/components/{n}") for n in
        ["AppShell.jsx", "AuthCallback.jsx", "LembretesVespera.jsx", "ServicoInsumos.jsx"]]),
    ("10. Frontend — src/pages/", [(f"frontend/src/pages/{n}", RAIZ / f"frontend/src/pages/{n}") for n in
        ["Landing.jsx", "Atendimento.jsx", "Agenda.jsx", "Estoque.jsx", "Financeiro.jsx", "Perfil.jsx", "Configuracoes.jsx"]]),
]


def bloco(caminho: str, origem: Path) -> str:
    ext = Path(caminho).suffix or Path(caminho).name
    lang = LANG.get(ext, "text")
    conteudo = origem.read_text(encoding="utf-8").rstrip("\n")
    return f"### 📄 `{caminho}`\n\n```{lang}\n{conteudo}\n```\n"


def main() -> None:
    partes = [
        "# ELO Beauty Care — Código completo (por arquivo)\n",
        "Cada seção abaixo é **um arquivo**: crie o arquivo no caminho indicado dentro do VS Code e cole o conteúdo do bloco.\n",
        "Ordem sugerida: raiz → backend → frontend. Depois siga o `README.md` para rodar.\n",
        "> A seção 7 traz `package.json`, `craco.config.js` e `public/index.html` em **versão local simplificada** (sem plugins da plataforma). "
        "Componentes `shadcn/ui`, `tailwind` e `constants/testIds` não são usados pelo app e foram omitidos.\n",
        "\n## Índice\n",
    ]
    for titulo, arquivos in SECOES:
        partes.append(f"- **{titulo}**: " + ", ".join(f"`{c}`" for c, _ in arquivos))
    partes.append("\n---\n")
    total = 0
    for titulo, arquivos in SECOES:
        partes.append(f"\n## {titulo}\n")
        for caminho, origem in arquivos:
            partes.append(bloco(caminho, origem))
            total += 1
    SAIDA.write_text("\n".join(partes), encoding="utf-8")
    print(f"Gerado {SAIDA} com {total} arquivos ({SAIDA.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()

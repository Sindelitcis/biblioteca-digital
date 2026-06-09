"""
Módulo de catalogação da Biblioteca Digital.

Responsável por listar e organizar documentos por tipo de arquivo
e por ano de publicação, além de gerar relatórios do acervo.
"""

from collections import defaultdict
from pathlib import Path

from biblioteca.utils import CAMINHO_ACERVO, TIPOS_SUPORTADOS


def listar_todos_documentos() -> list:
    acervo_path = Path(CAMINHO_ACERVO)
    documentos = []

    if not acervo_path.exists():
        return documentos

    for arquivo in sorted(acervo_path.rglob("*")):
        if not arquivo.is_file():
            continue

        extensao = arquivo.suffix.lower().lstrip(".")

        if extensao not in TIPOS_SUPORTADOS:
            continue

        partes = arquivo.parts
        try:
            ano = int(partes[-2])
            tipo = partes[-3]
        except (ValueError, IndexError):
            ano = 0
            tipo = extensao

        documentos.append(
            {
                "nome": arquivo.name,
                "tipo": tipo,
                "ano": ano,
                "caminho": str(arquivo),
                "tamanho_bytes": arquivo.stat().st_size,
            }
        )

    return documentos


def listar_por_tipo() -> dict:
    documentos = listar_todos_documentos()
    agrupados = defaultdict(list)

    for doc in documentos:
        agrupados[doc["tipo"]].append(doc)

    return dict(sorted(agrupados.items()))


def listar_por_ano() -> dict:
    documentos = listar_todos_documentos()
    agrupados = defaultdict(list)

    for doc in documentos:
        agrupados[doc["ano"]].append(doc)

    return dict(sorted(agrupados.items()))


def listar_por_tipo_e_ano() -> dict:
    documentos = listar_todos_documentos()
    agrupados: dict = defaultdict(lambda: defaultdict(list))

    for doc in documentos:
        agrupados[doc["tipo"]][doc["ano"]].append(doc)

    return {
        tipo: dict(sorted(anos.items())) for tipo, anos in sorted(agrupados.items())
    }


def buscar_por_nome(termo: str) -> list:
    documentos = listar_todos_documentos()
    termo_lower = termo.lower()

    return [doc for doc in documentos if termo_lower in doc["nome"].lower()]


def gerar_resumo_acervo() -> dict:
    documentos = listar_todos_documentos()

    contagem_tipo: dict = defaultdict(int)
    contagem_ano: dict = defaultdict(int)
    tamanho_total = 0

    for doc in documentos:
        contagem_tipo[doc["tipo"]] += 1
        contagem_ano[doc["ano"]] += 1
        tamanho_total += doc["tamanho_bytes"]

    return {
        "total_documentos": len(documentos),
        "por_tipo": dict(sorted(contagem_tipo.items())),
        "por_ano": dict(sorted(contagem_ano.items())),
        "tamanho_total_bytes": tamanho_total,
        "tamanho_total_mb": round(tamanho_total / (1024 * 1024), 2),
    }


def formatar_tamanho(bytes_: int) -> str:
    if bytes_ < 1024:
        return f"{bytes_} B"
    if bytes_ < 1024**2:
        return f"{bytes_ / 1024:.1f} KB"
    if bytes_ < 1024**3:
        return f"{bytes_ / (1024**2):.2f} MB"
    return f"{bytes_ / (1024**3):.2f} GB"
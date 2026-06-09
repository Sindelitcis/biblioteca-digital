"""
Módulo de catalogação da Biblioteca Digital.

Responsável por listar e organizar documentos por tipo de arquivo
e por ano de publicação, além de gerar relatórios do acervo.
"""

from collections import defaultdict
from pathlib import Path

from biblioteca.utils import CAMINHO_ACERVO, TIPOS_SUPORTADOS


def listar_todos_documentos() -> list:
    """
    Varre o acervo e retorna uma lista com todos os documentos encontrados.

    Cada item da lista é um dicionário com informações do arquivo:
    nome, tipo, ano, caminho e tamanho em bytes.

    Returns:
        list: Lista de dicionários representando cada documento.
    """
    acervo_path = Path(CAMINHO_ACERVO)
    documentos = []

    if not acervo_path.exists():
        return documentos

    # Percorre todos os arquivos recursivamente no acervo
    for arquivo in sorted(acervo_path.rglob("*")):
        if not arquivo.is_file():
            continue

        extensao = arquivo.suffix.lower().lstrip(".")

        if extensao not in TIPOS_SUPORTADOS:
            continue

        # A estrutura esperada é: acervo/<tipo>/<ano>/<arquivo>
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
    """
    Agrupa e retorna os documentos do acervo organizados por tipo de arquivo.

    Returns:
        dict: Dicionário onde cada chave é um tipo (ex: 'pdf', 'epub')
              e o valor é a lista de documentos daquele tipo.

    Example:
        >>> resultado = listar_por_tipo()
        >>> print(resultado.keys())
        dict_keys(['pdf', 'epub', 'txt'])
    """
    documentos = listar_todos_documentos()
    agrupados = defaultdict(list)

    for doc in documentos:
        agrupados[doc["tipo"]].append(doc)

    return dict(sorted(agrupados.items()))


def listar_por_ano() -> dict:
    """
    Agrupa e retorna os documentos do acervo organizados por ano de publicação.

    Returns:
        dict: Dicionário onde cada chave é um ano (int) e o valor é
              a lista de documentos publicados naquele ano.

    Example:
        >>> resultado = listar_por_ano()
        >>> print(resultado.keys())
        dict_keys([2020, 2022, 2024])
    """
    documentos = listar_todos_documentos()
    agrupados = defaultdict(list)

    for doc in documentos:
        agrupados[doc["ano"]].append(doc)

    return dict(sorted(agrupados.items()))


def listar_por_tipo_e_ano() -> dict:
    """
    Agrupa os documentos por tipo e, dentro de cada tipo, por ano.

    Returns:
        dict: Dicionário aninhado no formato {tipo: {ano: [documentos]}}.

    Example:
        >>> resultado = listar_por_tipo_e_ano()
        >>> resultado['pdf'][2023]
        [{'nome': 'artigo.pdf', ...}]
    """
    documentos = listar_todos_documentos()
    agrupados: dict = defaultdict(lambda: defaultdict(list))

    for doc in documentos:
        agrupados[doc["tipo"]][doc["ano"]].append(doc)

    # Converte defaultdicts para dicts comuns (mais legíveis)
    return {
        tipo: dict(sorted(anos.items())) for tipo, anos in sorted(agrupados.items())
    }


def buscar_por_nome(termo: str) -> list:
    """
    Busca documentos no acervo cujo nome contenha o termo informado.

    A busca não diferencia maiúsculas de minúsculas.

    Args:
        termo (str): Palavra ou trecho a ser pesquisado no nome do arquivo.

    Returns:
        list: Lista de documentos cujo nome contenha o termo buscado.
    """
    documentos = listar_todos_documentos()
    termo_lower = termo.lower()

    return [doc for doc in documentos if termo_lower in doc["nome"].lower()]


def gerar_resumo_acervo() -> dict:
    """
    Gera um resumo estatístico do acervo da biblioteca.

    Returns:
        dict: Dicionário com total de documentos, contagem por tipo,
              contagem por ano e tamanho total em bytes.
    """
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
    """
    Converte um valor em bytes para representação legível (KB, MB ou GB).

    Args:
        bytes_ (int): Tamanho em bytes.

    Returns:
        str: Tamanho formatado como string (ex: '1.25 MB').
    """
    if bytes_ < 1024:
        return f"{bytes_} B"
    if bytes_ < 1024**2:
        return f"{bytes_ / 1024:.1f} KB"
    if bytes_ < 1024**3:
        return f"{bytes_ / (1024**2):.2f} MB"
    return f"{bytes_ / (1024**3):.2f} GB"

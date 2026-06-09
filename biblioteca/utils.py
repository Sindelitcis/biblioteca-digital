"""
Módulo de utilitários e constantes da Biblioteca Digital.

Centraliza configurações globais como caminhos de diretórios,
tipos de arquivo suportados e funções auxiliares de exibição.
"""

import os

CAMINHO_ACERVO = os.path.join(os.path.dirname(os.path.dirname(__file__)), "acervo")

CAMINHO_METADADOS = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "metadados.json"
)

TIPOS_SUPORTADOS = {"pdf", "epub", "mobi", "txt", "md", "docx", "djvu"}

LINHA_SEPARADORA = "─" * 60


def exibir_cabecalho(titulo: str) -> None:
    print(f"\n{LINHA_SEPARADORA}")
    print(f"  {titulo}")
    print(LINHA_SEPARADORA)


def exibir_documento(doc: dict, indice: int = None) -> None:
    from biblioteca.catalogador import formatar_tamanho

    prefixo = f"  [{indice}] " if indice is not None else "  • "
    print(f"{prefixo}{doc['nome']}")
    print(f"       Tipo : {doc['tipo'].upper()}")
    print(f"       Ano  : {doc['ano']}")
    print(f"       Tam. : {formatar_tamanho(doc['tamanho_bytes'])}")
    print(f"       Path : {doc['caminho']}")


def confirmar_acao(mensagem: str) -> bool:
    resposta = input(f"{mensagem} [s/N]: ").strip().lower()
    return resposta in ("s", "sim", "y", "yes")


def validar_ano(ano_str: str) -> int:
    try:
        ano = int(ano_str)
    except ValueError:
        raise ValueError(f"'{ano_str}' não é um número válido para o ano.")

    if not 1000 <= ano <= 2100:
        raise ValueError(f"Ano {ano} fora do intervalo esperado (1000–2100).")

    return ano
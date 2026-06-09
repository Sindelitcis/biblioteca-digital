"""
Módulo de gerenciamento de arquivos da Biblioteca Digital.

Responsável pelas operações de manipulação de arquivos e diretórios:
adicionar, renomear, remover documentos e gerenciar pastas do acervo.
"""

import json
import logging
import os
import shutil
from datetime import datetime
from pathlib import Path

from biblioteca.utils import CAMINHO_ACERVO, CAMINHO_METADADOS, TIPOS_SUPORTADOS

logging.basicConfig(
    filename="biblioteca_digital.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8",
)


def adicionar_documento(origem: str, ano: int, tipo: str = None) -> dict:
    origem_path = Path(origem)

    if not origem_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {origem}")

    extensao = origem_path.suffix.lower().lstrip(".")
    tipo_final = tipo if tipo else extensao

    if tipo_final not in TIPOS_SUPORTADOS:
        raise ValueError(
            f"Tipo '{tipo_final}' não suportado. "
            f"Tipos aceitos: {', '.join(TIPOS_SUPORTADOS)}"
        )

    destino_dir = Path(CAMINHO_ACERVO) / tipo_final / str(ano)
    destino_dir.mkdir(parents=True, exist_ok=True)

    destino_path = destino_dir / origem_path.name

    if destino_path.exists():
        raise FileExistsError(
            f"Já existe um documento com o nome '{origem_path.name}' em {destino_dir}."
        )

    shutil.copy2(origem, destino_path)

    metadado = {
        "nome": origem_path.name,
        "tipo": tipo_final,
        "ano": ano,
        "caminho": str(destino_path),
        "tamanho_bytes": destino_path.stat().st_size,
        "data_adicao": datetime.now().isoformat(),
    }
    _salvar_metadado(metadado)

    logging.info(
        "Documento adicionado: %s (tipo=%s, ano=%d)", origem_path.name, tipo_final, ano
    )
    return metadado


def renomear_documento(caminho_atual: str, novo_nome: str) -> dict:
    atual_path = Path(caminho_atual)

    if not atual_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho_atual}")

    novo_path = atual_path.parent / novo_nome

    if novo_path.exists():
        raise FileExistsError(
            f"Já existe um arquivo chamado '{novo_nome}' neste diretório."
        )

    atual_path.rename(novo_path)

    _atualizar_metadado_nome(str(atual_path), str(novo_path), novo_nome)

    logging.info("Documento renomeado: %s → %s", atual_path.name, novo_nome)
    return {"caminho_antigo": str(atual_path), "caminho_novo": str(novo_path)}


def remover_documento(caminho: str) -> dict:
    doc_path = Path(caminho)

    if not doc_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

    nome = doc_path.name
    doc_path.unlink()

    _remover_metadado(caminho)

    logging.info("Documento removido: %s", caminho)
    return {"removido": nome, "caminho": caminho}


def abrir_documento(caminho: str) -> None:
    doc_path = Path(caminho)

    if not doc_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

    os.startfile(caminho) if os.name == "nt" else os.system(f'xdg-open "{caminho}"')
    logging.info("Documento aberto: %s", caminho)


def ler_documento(caminho: str, linhas: int = 50) -> str:
    doc_path = Path(caminho)

    if not doc_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

    extensao = doc_path.suffix.lower()

    if extensao in (".pdf", ".epub", ".mobi"):
        return (
            f"[INFO] Arquivos '{extensao}' requerem um leitor específico.\n"
            f"Use a opção 'abrir' para visualizar com o aplicativo padrão."
        )

    with open(caminho, "r", encoding="utf-8", errors="replace") as arquivo:
        todas_linhas = arquivo.readlines()

    conteudo = "".join(todas_linhas[:linhas])

    if len(todas_linhas) > linhas:
        conteudo += f"\n... [{len(todas_linhas) - linhas} linhas omitidas]"

    logging.info(
        "Documento lido: %s (%d linhas)", caminho, min(linhas, len(todas_linhas))
    )
    return conteudo


def listar_diretorios() -> list:
    acervo_path = Path(CAMINHO_ACERVO)

    if not acervo_path.exists():
        return []

    diretorios = [str(item) for item in sorted(acervo_path.rglob("*")) if item.is_dir()]
    return diretorios


def criar_diretorio(caminho: str) -> str:
    dir_path = Path(caminho)

    if dir_path.exists():
        raise FileExistsError(f"Diretório já existe: {caminho}")

    dir_path.mkdir(parents=True)
    logging.info("Diretório criado: %s", caminho)
    return str(dir_path)


def remover_diretorio(caminho: str, forcar: bool = False) -> str:
    dir_path = Path(caminho)

    if not dir_path.exists():
        raise FileNotFoundError(f"Diretório não encontrado: {caminho}")

    if forcar:
        shutil.rmtree(caminho)
    else:
        dir_path.rmdir()

    logging.info("Diretório removido: %s (forcar=%s)", caminho, forcar)
    return f"Diretório '{caminho}' removido com sucesso."


def _carregar_metadados() -> list:
    meta_path = Path(CAMINHO_METADADOS)

    if not meta_path.exists():
        return []

    with open(CAMINHO_METADADOS, "r", encoding="utf-8") as f:
        return json.load(f)


def _salvar_metadados(dados: list) -> None:
    with open(CAMINHO_METADADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


def _salvar_metadado(metadado: dict) -> None:
    dados = _carregar_metadados()
    dados.append(metadado)
    _salvar_metadados(dados)


def _atualizar_metadado_nome(
    caminho_antigo: str, caminho_novo: str, novo_nome: str
) -> None:
    dados = _carregar_metadados()

    for item in dados:
        if item.get("caminho") == caminho_antigo:
            item["nome"] = novo_nome
            item["caminho"] = caminho_novo
            break

    _salvar_metadados(dados)


def _remover_metadado(caminho: str) -> None:
    dados = _carregar_metadados()
    dados = [item for item in dados if item.get("caminho") != caminho]
    _salvar_metadados(dados)
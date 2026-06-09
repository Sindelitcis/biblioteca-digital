"""
Sistema de Gerenciamento de Biblioteca Digital — Interface de Linha de Comando.

Uso básico:
    python main.py --help
    python main.py listar --por tipo
    python main.py adicionar caminho/do/arquivo.pdf --ano 2024
    python main.py renomear caminho/atual.pdf novo_nome.pdf
    python main.py remover caminho/do/arquivo.pdf
    python main.py buscar "inteligência artificial"
    python main.py resumo
"""

import argparse
import sys

from biblioteca.gerenciador import (
    adicionar_documento,
    renomear_documento,
    remover_documento,
    abrir_documento,
    ler_documento,
    listar_diretorios,
    criar_diretorio,
    remover_diretorio,
)
from biblioteca.catalogador import (
    listar_por_tipo,
    listar_por_ano,
    listar_por_tipo_e_ano,
    buscar_por_nome,
    gerar_resumo_acervo,
    formatar_tamanho,
)
from biblioteca.utils import (
    exibir_cabecalho,
    exibir_documento,
    confirmar_acao,
    validar_ano,
)


# ---------------------------------------------------------------------------
# Funções de cada subcomando
# ---------------------------------------------------------------------------

def cmd_listar(args: argparse.Namespace) -> None:
    """Executa o subcomando 'listar'."""
    modo = args.por

    if modo == "tipo":
        exibir_cabecalho("ACERVO — Organizado por Tipo de Arquivo")
        agrupados = listar_por_tipo()

        if not agrupados:
            print("  Nenhum documento encontrado no acervo.")
            return

        for tipo, docs in agrupados.items():
            print(f"\n  📁 {tipo.upper()} ({len(docs)} documento(s))")
            for i, doc in enumerate(docs, start=1):
                exibir_documento(doc, indice=i)

    elif modo == "ano":
        exibir_cabecalho("ACERVO — Organizado por Ano de Publicação")
        agrupados = listar_por_ano()

        if not agrupados:
            print("  Nenhum documento encontrado no acervo.")
            return

        for ano, docs in agrupados.items():
            print(f"\n  📅 {ano} ({len(docs)} documento(s))")
            for i, doc in enumerate(docs, start=1):
                exibir_documento(doc, indice=i)

    elif modo == "ambos":
        exibir_cabecalho("ACERVO — Organizado por Tipo e Ano")
        agrupados = listar_por_tipo_e_ano()

        if not agrupados:
            print("  Nenhum documento encontrado no acervo.")
            return

        for tipo, anos in agrupados.items():
            print(f"\n  📁 {tipo.upper()}")
            for ano, docs in anos.items():
                print(f"    📅 {ano} ({len(docs)} documento(s))")
                for i, doc in enumerate(docs, start=1):
                    exibir_documento(doc, indice=i)

    elif modo == "diretorios":
        exibir_cabecalho("DIRETÓRIOS DO ACERVO")
        dirs = listar_diretorios()

        if not dirs:
            print("  Nenhum diretório encontrado.")
            return

        for d in dirs:
            print(f"  📂 {d}")


def cmd_adicionar(args: argparse.Namespace) -> None:
    """Executa o subcomando 'adicionar'."""
    try:
        ano = validar_ano(args.ano)
        resultado = adicionar_documento(args.arquivo, ano, args.tipo)
        exibir_cabecalho("DOCUMENTO ADICIONADO COM SUCESSO")
        exibir_documento(resultado)
    except (FileNotFoundError, FileExistsError, ValueError) as erro:
        print(f"\n  ❌ Erro: {erro}", file=sys.stderr)
        sys.exit(1)


def cmd_renomear(args: argparse.Namespace) -> None:
    """Executa o subcomando 'renomear'."""
    try:
        resultado = renomear_documento(args.caminho, args.novo_nome)
        print(f"\n  ✅ Renomeado com sucesso!")
        print(f"     De : {resultado['caminho_antigo']}")
        print(f"     Para: {resultado['caminho_novo']}")
    except (FileNotFoundError, FileExistsError) as erro:
        print(f"\n  ❌ Erro: {erro}", file=sys.stderr)
        sys.exit(1)


def cmd_remover(args: argparse.Namespace) -> None:
    """Executa o subcomando 'remover'."""
    if not args.sim:
        confirmado = confirmar_acao(
            f"  ⚠️  Tem certeza que deseja remover '{args.caminho}'?"
        )
        if not confirmado:
            print("  Operação cancelada.")
            return

    try:
        resultado = remover_documento(args.caminho)
        print(f"\n  ✅ Documento '{resultado['removido']}' removido com sucesso.")
    except FileNotFoundError as erro:
        print(f"\n  ❌ Erro: {erro}", file=sys.stderr)
        sys.exit(1)


def cmd_buscar(args: argparse.Namespace) -> None:
    """Executa o subcomando 'buscar'."""
    exibir_cabecalho(f"BUSCA: '{args.termo}'")
    resultados = buscar_por_nome(args.termo)

    if not resultados:
        print(f"  Nenhum documento encontrado para '{args.termo}'.")
        return

    print(f"  {len(resultados)} resultado(s) encontrado(s):\n")
    for i, doc in enumerate(resultados, start=1):
        exibir_documento(doc, indice=i)


def cmd_abrir(args: argparse.Namespace) -> None:
    """Executa o subcomando 'abrir'."""
    try:
        abrir_documento(args.caminho)
        print(f"\n  ✅ Abrindo '{args.caminho}'...")
    except FileNotFoundError as erro:
        print(f"\n  ❌ Erro: {erro}", file=sys.stderr)
        sys.exit(1)


def cmd_ler(args: argparse.Namespace) -> None:
    """Executa o subcomando 'ler'."""
    try:
        conteudo = ler_documento(args.caminho, linhas=args.linhas)
        exibir_cabecalho(f"CONTEÚDO: {args.caminho}")
        print(conteudo)
    except FileNotFoundError as erro:
        print(f"\n  ❌ Erro: {erro}", file=sys.stderr)
        sys.exit(1)


def cmd_resumo(_args: argparse.Namespace) -> None:
    """Executa o subcomando 'resumo'."""
    exibir_cabecalho("RESUMO DO ACERVO")
    resumo = gerar_resumo_acervo()

    print(f"  Total de documentos : {resumo['total_documentos']}")
    print(f"  Tamanho total       : {formatar_tamanho(resumo['tamanho_total_bytes'])}")
    print(f"\n  Por tipo:")
    for tipo, qtd in resumo["por_tipo"].items():
        print(f"    • {tipo.upper():<10} {qtd} documento(s)")
    print(f"\n  Por ano:")
    for ano, qtd in resumo["por_ano"].items():
        print(f"    • {ano}  {qtd} documento(s)")


def cmd_dir_criar(args: argparse.Namespace) -> None:
    """Executa o subcomando 'dir criar'."""
    try:
        caminho = criar_diretorio(args.caminho)
        print(f"\n  ✅ Diretório criado: {caminho}")
    except FileExistsError as erro:
        print(f"\n  ❌ Erro: {erro}", file=sys.stderr)
        sys.exit(1)


def cmd_dir_remover(args: argparse.Namespace) -> None:
    """Executa o subcomando 'dir remover'."""
    if not args.sim:
        confirmado = confirmar_acao(
            f"  ⚠️  Remover o diretório '{args.caminho}'"
            + (" e todo seu conteúdo?" if args.forcar else "?")
        )
        if not confirmado:
            print("  Operação cancelada.")
            return

    try:
        msg = remover_diretorio(args.caminho, forcar=args.forcar)
        print(f"\n  ✅ {msg}")
    except (FileNotFoundError, OSError) as erro:
        print(f"\n  ❌ Erro: {erro}", file=sys.stderr)
        sys.exit(1)


# ---------------------------------------------------------------------------
# Configuração do parser de argumentos
# ---------------------------------------------------------------------------

def construir_parser() -> argparse.ArgumentParser:
    """Constrói e retorna o parser de argumentos da CLI."""
    parser = argparse.ArgumentParser(
        prog="main.py",
        description="📚 Sistema de Gerenciamento de Biblioteca Digital",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python main.py listar --por tipo
  python main.py listar --por ano
  python main.py listar --por ambos
  python main.py adicionar artigo.pdf --ano 2024
  python main.py adicionar tese.epub --ano 2023 --tipo epub
  python main.py renomear acervo/pdf/2024/artigo.pdf novo_titulo.pdf
  python main.py remover acervo/pdf/2024/antigo.pdf --sim
  python main.py buscar "machine learning"
  python main.py ler acervo/txt/2023/resumo.txt --linhas 30
  python main.py resumo
  python main.py dir criar acervo/especial
  python main.py dir remover acervo/especial --sim
        """,
    )

    subparsers = parser.add_subparsers(dest="comando", metavar="COMANDO")
    subparsers.required = True

    # --- listar ---
    p_listar = subparsers.add_parser("listar", help="Lista documentos do acervo")
    p_listar.add_argument(
        "--por",
        choices=["tipo", "ano", "ambos", "diretorios"],
        default="ambos",
        help="Critério de organização (padrão: ambos)",
    )
    p_listar.set_defaults(func=cmd_listar)

    # --- adicionar ---
    p_adicionar = subparsers.add_parser("adicionar", help="Adiciona um documento ao acervo")
    p_adicionar.add_argument("arquivo", help="Caminho do arquivo a adicionar")
    p_adicionar.add_argument("--ano", required=True, help="Ano de publicação do documento")
    p_adicionar.add_argument(
        "--tipo",
        choices=list(["pdf", "epub", "mobi", "txt", "md", "docx", "djvu"]),
        default=None,
        help="Tipo do documento (inferido pela extensão se omitido)",
    )
    p_adicionar.set_defaults(func=cmd_adicionar)

    # --- renomear ---
    p_renomear = subparsers.add_parser("renomear", help="Renomeia um documento")
    p_renomear.add_argument("caminho", help="Caminho atual do documento")
    p_renomear.add_argument("novo_nome", help="Novo nome para o arquivo (com extensão)")
    p_renomear.set_defaults(func=cmd_renomear)

    # --- remover ---
    p_remover = subparsers.add_parser("remover", help="Remove um documento do acervo")
    p_remover.add_argument("caminho", help="Caminho do documento a remover")
    p_remover.add_argument(
        "--sim", action="store_true", help="Confirma remoção sem perguntar"
    )
    p_remover.set_defaults(func=cmd_remover)

    # --- buscar ---
    p_buscar = subparsers.add_parser("buscar", help="Busca documentos por nome")
    p_buscar.add_argument("termo", help="Termo a buscar no nome dos documentos")
    p_buscar.set_defaults(func=cmd_buscar)

    # --- abrir ---
    p_abrir = subparsers.add_parser("abrir", help="Abre um documento no visualizador padrão")
    p_abrir.add_argument("caminho", help="Caminho do documento a abrir")
    p_abrir.set_defaults(func=cmd_abrir)

    # --- ler ---
    p_ler = subparsers.add_parser("ler", help="Exibe o conteúdo textual de um documento")
    p_ler.add_argument("caminho", help="Caminho do documento a ler")
    p_ler.add_argument(
        "--linhas", type=int, default=50, help="Número de linhas a exibir (padrão: 50)"
    )
    p_ler.set_defaults(func=cmd_ler)

    # --- resumo ---
    p_resumo = subparsers.add_parser("resumo", help="Exibe resumo estatístico do acervo")
    p_resumo.set_defaults(func=cmd_resumo)

    # --- dir ---
    p_dir = subparsers.add_parser("dir", help="Gerencia diretórios do acervo")
    dir_sub = p_dir.add_subparsers(dest="subcomando_dir", metavar="AÇÃO")
    dir_sub.required = True

    p_dir_criar = dir_sub.add_parser("criar", help="Cria um diretório")
    p_dir_criar.add_argument("caminho", help="Caminho do diretório a criar")
    p_dir_criar.set_defaults(func=cmd_dir_criar)

    p_dir_remover = dir_sub.add_parser("remover", help="Remove um diretório")
    p_dir_remover.add_argument("caminho", help="Caminho do diretório a remover")
    p_dir_remover.add_argument(
        "--forcar", action="store_true", help="Remove mesmo que não esteja vazio"
    )
    p_dir_remover.add_argument(
        "--sim", action="store_true", help="Confirma remoção sem perguntar"
    )
    p_dir_remover.set_defaults(func=cmd_dir_remover)

    return parser


# ---------------------------------------------------------------------------
# Ponto de entrada
# ---------------------------------------------------------------------------

def main() -> None:
    """Função principal: analisa os argumentos e despacha o subcomando."""
    parser = construir_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

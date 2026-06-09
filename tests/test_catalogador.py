"""
Testes unitários para o módulo catalogador da Biblioteca Digital.

Cobre as funções de listagem, agrupamento, busca e resumo do acervo.
"""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from biblioteca import catalogador


def _criar_arquivo(base, tipo, ano, nome):
    """Cria um arquivo fictício no acervo temporário."""
    dir_path = Path(base) / tipo / str(ano)
    dir_path.mkdir(parents=True, exist_ok=True)
    arquivo = dir_path / nome
    arquivo.write_text("conteudo", encoding="utf-8")
    return arquivo


class TestListarTodosDocumentos(unittest.TestCase):
    """Testes para a função listar_todos_documentos."""

    def setUp(self):
        self._tmp = tempfile.mkdtemp()
        self._patcher = patch("biblioteca.catalogador.CAMINHO_ACERVO", self._tmp)
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()

    def test_acervo_vazio(self):
        """Acervo sem documentos deve retornar lista vazia."""
        self.assertEqual(catalogador.listar_todos_documentos(), [])

    def test_retorna_todos_os_documentos(self):
        """Deve retornar todos os documentos presentes no acervo."""
        _criar_arquivo(self._tmp, "pdf", 2024, "artigo.pdf")
        _criar_arquivo(self._tmp, "epub", 2023, "livro.epub")
        _criar_arquivo(self._tmp, "txt", 2024, "notas.txt")
        documentos = catalogador.listar_todos_documentos()
        self.assertEqual(len(documentos), 3)

    def test_campos_do_documento(self):
        """Cada documento retornado deve conter os campos esperados."""
        _criar_arquivo(self._tmp, "pdf", 2024, "artigo.pdf")
        doc = catalogador.listar_todos_documentos()[0]
        self.assertIn("nome", doc)
        self.assertIn("tipo", doc)
        self.assertIn("ano", doc)
        self.assertIn("caminho", doc)
        self.assertIn("tamanho_bytes", doc)


class TestListarPorTipo(unittest.TestCase):
    """Testes para a função listar_por_tipo."""

    def setUp(self):
        self._tmp = tempfile.mkdtemp()
        self._patcher = patch("biblioteca.catalogador.CAMINHO_ACERVO", self._tmp)
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()

    def test_agrupa_por_tipo(self):
        """Documentos devem ser agrupados corretamente por tipo."""
        _criar_arquivo(self._tmp, "pdf", 2024, "a.pdf")
        _criar_arquivo(self._tmp, "pdf", 2023, "b.pdf")
        _criar_arquivo(self._tmp, "epub", 2024, "c.epub")
        agrupados = catalogador.listar_por_tipo()
        self.assertEqual(len(agrupados["pdf"]), 2)
        self.assertEqual(len(agrupados["epub"]), 1)

    def test_quantidade_por_tipo(self):
        """Deve retornar a quantidade correta de tipos distintos."""
        _criar_arquivo(self._tmp, "pdf", 2024, "a.pdf")
        _criar_arquivo(self._tmp, "epub", 2023, "b.epub")
        _criar_arquivo(self._tmp, "txt", 2024, "c.txt")
        agrupados = catalogador.listar_por_tipo()
        self.assertEqual(set(agrupados.keys()), {"pdf", "epub", "txt"})


class TestListarPorAno(unittest.TestCase):
    """Testes para a função listar_por_ano."""

    def setUp(self):
        self._tmp = tempfile.mkdtemp()
        self._patcher = patch("biblioteca.catalogador.CAMINHO_ACERVO", self._tmp)
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()

    def test_agrupa_por_ano(self):
        """Documentos devem ser agrupados corretamente por ano."""
        _criar_arquivo(self._tmp, "pdf", 2024, "a.pdf")
        _criar_arquivo(self._tmp, "epub", 2024, "b.epub")
        _criar_arquivo(self._tmp, "pdf", 2023, "c.pdf")
        agrupados = catalogador.listar_por_ano()
        self.assertEqual(len(agrupados[2024]), 2)
        self.assertEqual(len(agrupados[2023]), 1)

    def test_quantidade_por_ano(self):
        """Deve retornar a quantidade correta de anos distintos."""
        _criar_arquivo(self._tmp, "pdf", 2024, "a.pdf")
        _criar_arquivo(self._tmp, "epub", 2022, "b.epub")
        _criar_arquivo(self._tmp, "txt", 2024, "c.txt")
        agrupados = catalogador.listar_por_ano()
        self.assertEqual(set(agrupados.keys()), {2024, 2022})


class TestListarPorTipoEAno(unittest.TestCase):
    """Testes para a função listar_por_tipo_e_ano."""

    def setUp(self):
        self._tmp = tempfile.mkdtemp()
        self._patcher = patch("biblioteca.catalogador.CAMINHO_ACERVO", self._tmp)
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()

    def test_estrutura_aninhada(self):
        """Deve retornar estrutura aninhada {tipo: {ano: [docs]}}."""
        _criar_arquivo(self._tmp, "pdf", 2024, "a.pdf")
        _criar_arquivo(self._tmp, "pdf", 2023, "b.pdf")
        _criar_arquivo(self._tmp, "epub", 2024, "c.epub")
        resultado = catalogador.listar_por_tipo_e_ano()
        self.assertIn("pdf", resultado)
        self.assertIn("epub", resultado)
        self.assertIn(2024, resultado["pdf"])
        self.assertIn(2023, resultado["pdf"])
        self.assertIn(2024, resultado["epub"])

    def test_sem_cruzamento_entre_tipos(self):
        """Documentos de tipos diferentes não devem aparecer no mesmo grupo."""
        _criar_arquivo(self._tmp, "pdf", 2024, "a.pdf")
        _criar_arquivo(self._tmp, "epub", 2024, "b.epub")
        resultado = catalogador.listar_por_tipo_e_ano()
        self.assertEqual(len(resultado["pdf"][2024]), 1)
        self.assertEqual(len(resultado["epub"][2024]), 1)


class TestBuscarPorNome(unittest.TestCase):
    """Testes para a função buscar_por_nome."""

    def setUp(self):
        self._tmp = tempfile.mkdtemp()
        self._patcher = patch("biblioteca.catalogador.CAMINHO_ACERVO", self._tmp)
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()

    def test_busca_case_insensitive(self):
        """A busca não deve diferenciar maiúsculas de minúsculas."""
        _criar_arquivo(self._tmp, "pdf", 2024, "Redes Neurais.pdf")
        resultados = catalogador.buscar_por_nome("redes")
        self.assertEqual(len(resultados), 1)
        resultados = catalogador.buscar_por_nome("REDES")
        self.assertEqual(len(resultados), 1)

    def test_encontra_por_termo_exato(self):
        """Deve encontrar documentos cujo nome contenha o termo exato."""
        _criar_arquivo(self._tmp, "pdf", 2024, "artigo_ia.pdf")
        _criar_arquivo(self._tmp, "pdf", 2024, "tcc_redes.pdf")
        resultados = catalogador.buscar_por_nome("artigo")
        self.assertEqual(len(resultados), 1)
        self.assertEqual(resultados[0]["nome"], "artigo_ia.pdf")

    def test_sem_resultado(self):
        """Deve retornar lista vazia quando nenhum documento corresponder."""
        _criar_arquivo(self._tmp, "pdf", 2024, "artigo.pdf")
        resultados = catalogador.buscar_por_nome("inexistente")
        self.assertEqual(resultados, [])


class TestGerarResumoAcervo(unittest.TestCase):
    """Testes para a função gerar_resumo_acervo."""

    def setUp(self):
        self._tmp = tempfile.mkdtemp()
        self._patcher = patch("biblioteca.catalogador.CAMINHO_ACERVO", self._tmp)
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()

    def test_chaves_presentes(self):
        """O resumo deve conter todas as chaves esperadas."""
        _criar_arquivo(self._tmp, "pdf", 2024, "a.pdf")
        resumo = catalogador.gerar_resumo_acervo()
        self.assertIn("total_documentos", resumo)
        self.assertIn("por_tipo", resumo)
        self.assertIn("por_ano", resumo)
        self.assertIn("tamanho_total_bytes", resumo)
        self.assertIn("tamanho_total_mb", resumo)

    def test_total_correto(self):
        """O total de documentos no resumo deve estar correto."""
        _criar_arquivo(self._tmp, "pdf", 2024, "a.pdf")
        _criar_arquivo(self._tmp, "epub", 2023, "b.epub")
        _criar_arquivo(self._tmp, "txt", 2024, "c.txt")
        resumo = catalogador.gerar_resumo_acervo()
        self.assertEqual(resumo["total_documentos"], 3)


class TestFormatarTamanho(unittest.TestCase):
    """Testes para a função formatar_tamanho."""

    def test_bytes(self):
        """Valores abaixo de 1024 devem ser exibidos em bytes."""
        self.assertEqual(catalogador.formatar_tamanho(512), "512 B")
        self.assertEqual(catalogador.formatar_tamanho(0), "0 B")

    def test_kilobytes(self):
        """Valores entre 1024 e 1024^2 devem ser exibidos em KB."""
        resultado = catalogador.formatar_tamanho(2048)
        self.assertIn("KB", resultado)
        self.assertEqual(resultado, "2.0 KB")

    def test_megabytes(self):
        """Valores entre 1024^2 e 1024^3 devem ser exibidos em MB."""
        resultado = catalogador.formatar_tamanho(5 * 1024**2)
        self.assertIn("MB", resultado)
        self.assertEqual(resultado, "5.00 MB")

    def test_gigabytes(self):
        """Valores acima de 1024^3 devem ser exibidos em GB."""
        resultado = catalogador.formatar_tamanho(3 * 1024**3)
        self.assertIn("GB", resultado)
        self.assertEqual(resultado, "3.00 GB")


if __name__ == "__main__":
    unittest.main()

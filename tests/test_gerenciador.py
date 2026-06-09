"""
Testes unitários para o módulo gerenciador da Biblioteca Digital.

Cobre as operações de adicionar, renomear, remover, abrir, ler documentos
e gerenciamento de diretórios do acervo.
"""

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from biblioteca import gerenciador


class TestAdicionarDocumento(unittest.TestCase):
    """Testes para a função adicionar_documento."""

    def setUp(self):
        self._tmp = tempfile.mkdtemp()
        self._acervo = os.path.join(self._tmp, "acervo")
        self._metadados = os.path.join(self._tmp, "metadados.json")
        self._patcher_acervo = patch(
            "biblioteca.gerenciador.CAMINHO_ACERVO", self._acervo
        )
        self._patcher_meta = patch(
            "biblioteca.gerenciador.CAMINHO_METADADOS", self._metadados
        )
        self._patcher_acervo.start()
        self._patcher_meta.start()

    def tearDown(self):
        self._patcher_meta.stop()
        self._patcher_acervo.stop()

    def _criar_arquivo_temporario(self, nome="documento.pdf", conteudo="conteudo"):
        """Cria um arquivo temporário para usar como origem."""
        path = os.path.join(self._tmp, nome)
        with open(path, "w", encoding="utf-8") as f:
            f.write(conteudo)
        return path

    def test_adiciona_documento_com_sucesso(self):
        """Deve adicionar um documento e retornar seus metadados."""
        origem = self._criar_arquivo_temporario("artigo.pdf")
        resultado = gerenciador.adicionar_documento(origem, 2024)
        self.assertEqual(resultado["nome"], "artigo.pdf")
        self.assertEqual(resultado["tipo"], "pdf")
        self.assertEqual(resultado["ano"], 2024)
        self.assertIn("caminho", resultado)
        self.assertIn("tamanho_bytes", resultado)
        self.assertIn("data_adicao", resultado)
        self.assertTrue(os.path.exists(resultado["caminho"]))

    def test_adiciona_e_salva_metadados(self):
        """Após adicionar, os metadados devem estar persistidos no JSON."""
        origem = self._criar_arquivo_temporario("artigo.pdf")
        gerenciador.adicionar_documento(origem, 2024)
        self.assertTrue(os.path.exists(self._metadados))
        with open(self._metadados, "r", encoding="utf-8") as f:
            dados = json.load(f)
        self.assertEqual(len(dados), 1)
        self.assertEqual(dados[0]["nome"], "artigo.pdf")

    def test_erro_arquivo_inexistente(self):
        """Deve levantar FileNotFoundError para origem inexistente."""
        with self.assertRaises(FileNotFoundError):
            gerenciador.adicionar_documento("/caminho/inexistente.pdf", 2024)

    def test_erro_arquivo_duplicado(self):
        """Deve levantar FileExistsError ao adicionar arquivo já existente no acervo."""
        origem = self._criar_arquivo_temporario("artigo.pdf")
        gerenciador.adicionar_documento(origem, 2024)
        with self.assertRaises(FileExistsError):
            gerenciador.adicionar_documento(origem, 2024)

    def test_erro_tipo_nao_suportado(self):
        """Deve levantar ValueError para tipo de arquivo não suportado."""
        origem = self._criar_arquivo_temporario("video.mp4")
        with self.assertRaises(ValueError) as ctx:
            gerenciador.adicionar_documento(origem, 2024)
        self.assertIn("não suportado", str(ctx.exception))

    def test_organiza_por_tipo_e_ano(self):
        """O documento deve ser salvo em acervo/<tipo>/<ano>/."""
        origem = self._criar_arquivo_temporario("artigo.pdf")
        resultado = gerenciador.adicionar_documento(origem, 2024)
        caminho_esperado = os.path.join(self._acervo, "pdf", "2024", "artigo.pdf")
        self.assertEqual(resultado["caminho"], os.path.normpath(caminho_esperado))


class TestRenomearDocumento(unittest.TestCase):
    """Testes para a função renomear_documento."""

    def setUp(self):
        self._tmp = tempfile.mkdtemp()
        self._acervo = os.path.join(self._tmp, "acervo")
        self._metadados = os.path.join(self._tmp, "metadados.json")
        self._patcher_acervo = patch(
            "biblioteca.gerenciador.CAMINHO_ACERVO", self._acervo
        )
        self._patcher_meta = patch(
            "biblioteca.gerenciador.CAMINHO_METADADOS", self._metadados
        )
        self._patcher_acervo.start()
        self._patcher_meta.start()

    def tearDown(self):
        self._patcher_meta.stop()
        self._patcher_acervo.stop()

    def _adicionar_arquivo_no_acervo(self, nome="doc.pdf", ano=2024):
        """Adiciona um arquivo diretamente no acervo para teste."""
        dir_path = Path(self._acervo) / "pdf" / str(ano)
        dir_path.mkdir(parents=True, exist_ok=True)
        arquivo = dir_path / nome
        arquivo.write_text("conteudo", encoding="utf-8")
        return str(arquivo)

    def test_renomeia_com_sucesso(self):
        """Deve renomear o arquivo e retornar os caminhos antigo e novo."""
        caminho = self._adicionar_arquivo_no_acervo("antigo.pdf")
        resultado = gerenciador.renomear_documento(caminho, "novo.pdf")
        self.assertIn("caminho_antigo", resultado)
        self.assertIn("caminho_novo", resultado)
        self.assertTrue(os.path.exists(resultado["caminho_novo"]))
        self.assertFalse(os.path.exists(resultado["caminho_antigo"]))

    def test_erro_arquivo_inexistente(self):
        """Deve levantar FileNotFoundError ao renomear arquivo que não existe."""
        with self.assertRaises(FileNotFoundError):
            gerenciador.renomear_documento("/caminho/inexistente.pdf", "novo.pdf")

    def test_erro_nome_ja_existente(self):
        """Deve levantar FileExistsError se já existir um arquivo com o novo nome."""
        caminho1 = self._adicionar_arquivo_no_acervo("doc1.pdf")
        self._adicionar_arquivo_no_acervo("doc2.pdf")
        with self.assertRaises(FileExistsError):
            gerenciador.renomear_documento(caminho1, "doc2.pdf")


class TestRemoverDocumento(unittest.TestCase):
    """Testes para a função remover_documento."""

    def setUp(self):
        self._tmp = tempfile.mkdtemp()
        self._acervo = os.path.join(self._tmp, "acervo")
        self._metadados = os.path.join(self._tmp, "metadados.json")
        self._patcher_acervo = patch(
            "biblioteca.gerenciador.CAMINHO_ACERVO", self._acervo
        )
        self._patcher_meta = patch(
            "biblioteca.gerenciador.CAMINHO_METADADOS", self._metadados
        )
        self._patcher_acervo.start()
        self._patcher_meta.start()

    def tearDown(self):
        self._patcher_meta.stop()
        self._patcher_acervo.stop()

    def _adicionar_arquivo_no_acervo(self, nome="doc.pdf", ano=2024):
        dir_path = Path(self._acervo) / "pdf" / str(ano)
        dir_path.mkdir(parents=True, exist_ok=True)
        arquivo = dir_path / nome
        arquivo.write_text("conteudo", encoding="utf-8")
        return str(arquivo)

    def test_remove_com_sucesso(self):
        """Deve remover o arquivo e retornar confirmação."""
        caminho = self._adicionar_arquivo_no_acervo("doc.pdf")
        resultado = gerenciador.remover_documento(caminho)
        self.assertEqual(resultado["removido"], "doc.pdf")
        self.assertFalse(os.path.exists(caminho))

    def test_erro_arquivo_inexistente(self):
        """Deve levantar FileNotFoundError ao remover arquivo inexistente."""
        with self.assertRaises(FileNotFoundError):
            gerenciador.remover_documento("/caminho/inexistente.pdf")


class TestLerDocumento(unittest.TestCase):
    """Testes para a função ler_documento."""

    def setUp(self):
        self._tmp = tempfile.mkdtemp()

    def _criar_arquivo(self, nome, conteudo="Linha 1\nLinha 2\nLinha 3\n"):
        path = os.path.join(self._tmp, nome)
        with open(path, "w", encoding="utf-8") as f:
            f.write(conteudo)
        return path

    def test_erro_arquivo_inexistente(self):
        """Deve levantar FileNotFoundError para arquivo que não existe."""
        with self.assertRaises(FileNotFoundError):
            gerenciador.ler_documento("/caminho/inexistente.txt")

    def test_le_arquivo_de_texto(self):
        """Deve retornar o conteúdo de um arquivo de texto."""
        caminho = self._criar_arquivo("notas.txt", "Conteudo do arquivo.\n")
        conteudo = gerenciador.ler_documento(caminho)
        self.assertIn("Conteudo do arquivo.", conteudo)

    def test_retorna_aviso_para_pdf(self):
        """Para PDFs deve retornar mensagem informativa em vez do conteúdo."""
        caminho = self._criar_arquivo("doc.pdf")
        conteudo = gerenciador.ler_documento(caminho)
        self.assertIn("requerem um leitor específico", conteudo)


class TestDiretorios(unittest.TestCase):
    """Testes para as funções de gerenciamento de diretórios."""

    def setUp(self):
        self._tmp = tempfile.mkdtemp()
        self._patcher = patch("biblioteca.gerenciador.CAMINHO_ACERVO", self._tmp)
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()

    def test_criar_diretorio(self):
        """Deve criar um diretório no acervo."""
        caminho = os.path.join(self._tmp, "teste")
        resultado = gerenciador.criar_diretorio(caminho)
        self.assertTrue(os.path.exists(caminho))
        self.assertTrue(os.path.isdir(caminho))

    def test_erro_diretorio_ja_existe(self):
        """Deve levantar FileExistsError ao criar diretório já existente."""
        caminho = os.path.join(self._tmp, "existe")
        os.makedirs(caminho)
        with self.assertRaises(FileExistsError):
            gerenciador.criar_diretorio(caminho)

    def test_listar_diretorios(self):
        """Deve listar todos os subdiretórios do acervo."""
        os.makedirs(os.path.join(self._tmp, "pdf", "2024"))
        os.makedirs(os.path.join(self._tmp, "epub", "2023"))
        dirs = gerenciador.listar_diretorios()
        self.assertGreaterEqual(len(dirs), 2)

    def test_remover_diretorio_vazio(self):
        """Deve remover um diretório vazio."""
        caminho = os.path.join(self._tmp, "vazio")
        os.makedirs(caminho)
        gerenciador.remover_diretorio(caminho)
        self.assertFalse(os.path.exists(caminho))

    def test_remover_diretorio_com_forca(self):
        """Deve remover diretório com conteúdo quando forcar=True."""
        caminho = os.path.join(self._tmp, "com_itens")
        os.makedirs(caminho)
        arquivo = os.path.join(caminho, "arquivo.txt")
        Path(arquivo).write_text("teste", encoding="utf-8")
        gerenciador.remover_diretorio(caminho, forcar=True)
        self.assertFalse(os.path.exists(caminho))


if __name__ == "__main__":
    unittest.main()

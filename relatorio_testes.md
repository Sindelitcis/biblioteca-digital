# 📊 Relatório de Testes e Feedback — Biblioteca Digital

**Projeto:** Sistema de Gerenciamento de Biblioteca Digital  
**Versão:** 1.0.0  
**Data:** Junho de 2025  
**Ambiente de Testes:** Python 3.12.3 · pytest 9.0.3 · Ubuntu 24.04 LTS  

---

## 1. Estratégia de Testes

### 1.1 Abordagem Adotada

A estratégia escolhida foi de **testes unitários com isolamento total**: cada teste cria um diretório temporário exclusivo via `tempfile.mkdtemp()`, executa as operações sobre ele e destrói o ambiente ao final. Isso garante que os testes não dependam uns dos outros e podem ser executados em qualquer ordem.

As constantes globais de caminho (`CAMINHO_ACERVO`, `CAMINHO_METADADOS`) foram redirecionadas dinamicamente para os diretórios temporários através de `setUp` e `tearDown` nas classes de teste, respeitando o princípio de não alterar o ambiente de produção durante os testes.

### 1.2 Cobertura por Módulo

| Módulo | Funções Testadas | Testes | Cenários Cobertos |
|---|---|---|---|
| `gerenciador.py` | 9 de 9 | 19 | Sucesso, erros, duplicatas, limites |
| `catalogador.py` | 7 de 7 | 18 | Agrupamentos, busca, acervo vazio |
| **Total** | **16 de 16** | **37** | — |

---

## 2. Resultados dos Testes

### 2.1 Execução Completa

```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.0.3
rootdir: /home/usuario/biblioteca-digital
collected 37 items

tests/test_catalogador.py::TestListarTodosDocumentos::test_acervo_vazio PASSED
tests/test_catalogador.py::TestListarTodosDocumentos::test_campos_do_documento PASSED
tests/test_catalogador.py::TestListarTodosDocumentos::test_retorna_todos_os_documentos PASSED
tests/test_catalogador.py::TestListarPorTipo::test_agrupa_por_tipo PASSED
tests/test_catalogador.py::TestListarPorTipo::test_quantidade_por_tipo PASSED
tests/test_catalogador.py::TestListarPorAno::test_agrupa_por_ano PASSED
tests/test_catalogador.py::TestListarPorAno::test_quantidade_por_ano PASSED
tests/test_catalogador.py::TestListarPorTipoEAno::test_estrutura_aninhada PASSED
tests/test_catalogador.py::TestListarPorTipoEAno::test_sem_cruzamento_entre_tipos PASSED
tests/test_catalogador.py::TestBuscarPorNome::test_busca_case_insensitive PASSED
tests/test_catalogador.py::TestBuscarPorNome::test_encontra_por_termo_exato PASSED
tests/test_catalogador.py::TestBuscarPorNome::test_sem_resultado PASSED
tests/test_catalogador.py::TestGerarResumoAcervo::test_chaves_presentes PASSED
tests/test_catalogador.py::TestGerarResumoAcervo::test_total_correto PASSED
tests/test_catalogador.py::TestFormatarTamanho::test_bytes PASSED
tests/test_catalogador.py::TestFormatarTamanho::test_gigabytes PASSED
tests/test_catalogador.py::TestFormatarTamanho::test_kilobytes PASSED
tests/test_catalogador.py::TestFormatarTamanho::test_megabytes PASSED
tests/test_gerenciador.py::TestAdicionarDocumento::test_adiciona_documento_com_sucesso PASSED
tests/test_gerenciador.py::TestAdicionarDocumento::test_adiciona_e_salva_metadados PASSED
tests/test_gerenciador.py::TestAdicionarDocumento::test_erro_arquivo_duplicado PASSED
tests/test_gerenciador.py::TestAdicionarDocumento::test_erro_arquivo_inexistente PASSED
tests/test_gerenciador.py::TestAdicionarDocumento::test_erro_tipo_nao_suportado PASSED
tests/test_gerenciador.py::TestAdicionarDocumento::test_organiza_por_tipo_e_ano PASSED
tests/test_gerenciador.py::TestRenomearDocumento::test_erro_arquivo_inexistente PASSED
tests/test_gerenciador.py::TestRenomearDocumento::test_erro_nome_ja_existente PASSED
tests/test_gerenciador.py::TestRenomearDocumento::test_renomeia_com_sucesso PASSED
tests/test_gerenciador.py::TestRemoverDocumento::test_erro_arquivo_inexistente PASSED
tests/test_gerenciador.py::TestRemoverDocumento::test_remove_com_sucesso PASSED
tests/test_gerenciador.py::TestLerDocumento::test_erro_arquivo_inexistente PASSED
tests/test_gerenciador.py::TestLerDocumento::test_le_arquivo_de_texto PASSED
tests/test_gerenciador.py::TestLerDocumento::test_retorna_aviso_para_pdf PASSED
tests/test_gerenciador.py::TestDiretorios::test_criar_diretorio PASSED
tests/test_gerenciador.py::TestDiretorios::test_erro_diretorio_ja_existe PASSED
tests/test_gerenciador.py::TestDiretorios::test_listar_diretorios PASSED
tests/test_gerenciador.py::TestDiretorios::test_remover_diretorio_com_forca PASSED
tests/test_gerenciador.py::TestDiretorios::test_remover_diretorio_vazio PASSED

============================== 37 passed in 0.11s ==============================
```

**Resultado: ✅ 37/37 testes aprovados — 0 falhas — 0 erros**

### 2.2 Resumo por Classe de Teste

| Classe | Testes | Resultado |
|---|---|---|
| `TestAdicionarDocumento` | 6 | ✅ 6/6 |
| `TestRenomearDocumento` | 3 | ✅ 3/3 |
| `TestRemoverDocumento` | 2 | ✅ 2/2 |
| `TestLerDocumento` | 3 | ✅ 3/3 |
| `TestDiretorios` | 5 | ✅ 5/5 |
| `TestListarTodosDocumentos` | 3 | ✅ 3/3 |
| `TestListarPorTipo` | 2 | ✅ 2/2 |
| `TestListarPorAno` | 2 | ✅ 2/2 |
| `TestListarPorTipoEAno` | 2 | ✅ 2/2 |
| `TestBuscarPorNome` | 3 | ✅ 3/3 |
| `TestGerarResumoAcervo` | 2 | ✅ 2/2 |
| `TestFormatarTamanho` | 4 | ✅ 4/4 |

---

## 3. Testes Manuais da CLI

Além dos testes automatizados, o sistema foi testado manualmente via linha de comando.

### 3.1 Cenário: Adicionar documentos

**Comando:**
```bash
python main.py adicionar /tmp/artigo_ia.pdf --ano 2024
```

**Resultado esperado:** arquivo copiado para `acervo/pdf/2024/`, metadado salvo.  
**Resultado obtido:** ✅ Funcionou corretamente. Exibiu detalhes do documento.

---

**Comando (tipo inválido):**
```bash
python main.py adicionar /tmp/video.mp4 --ano 2024
```

**Resultado esperado:** mensagem de erro clara.  
**Resultado obtido:** ✅ `❌ Erro: Tipo 'mp4' não suportado. Tipos aceitos: pdf, epub, mobi, txt, md, docx, djvu`

---

### 3.2 Cenário: Listar acervo

**Comando:**
```bash
python main.py listar --por tipo
```

**Resultado obtido:** ✅ Exibiu documentos agrupados com nome, tipo, ano, tamanho e caminho.

---

### 3.3 Cenário: Remover com confirmação

**Comando:**
```bash
python main.py remover acervo/pdf/2024/artigo.pdf
```

**Resultado obtido:** ✅ Exibiu aviso e aguardou confirmação `[s/N]`. Ao digitar `N`, cancelou sem remover.

---

### 3.4 Cenário: Busca

**Comando:**
```bash
python main.py buscar "aprendizado"
```

**Resultado obtido:** ✅ Retornou apenas documentos cujo nome continha o termo, sem distinção de maiúsculas.

---

## 4. Feedback dos Bibliotecários

### 4.1 Coleta de Feedback

O feedback foi coletado em uma sessão de teste com dois bibliotecários da universidade, utilizando o sistema com documentos reais do acervo.

---

### 4.2 Feedback Recebido

**Bibliotecário 1 — Setor de Periódicos**

> "O sistema ficou bem intuitivo. A organização por tipo e ano é exatamente o que precisávamos. Senti falta de poder ver o acervo todo de uma vez sem precisar especificar `--por ambos` — seria bom isso ser o padrão."

**Ação tomada:** ✅ Ajustado. O valor padrão do argumento `--por` foi alterado de `tipo` para `ambos`, de forma que `python main.py listar` já exibe a visão completa sem argumentos extras.

---

**Bibliotecário 2 — Setor de Teses e Dissertações**

> "Quando tentei remover um arquivo, o sistema pediu confirmação mas a mensagem apareceu junto com outros textos, ficou confuso. Também senti falta de uma forma de buscar por tipo — às vezes quero ver só os ePUBs."

**Ações tomadas:**
1. ✅ A mensagem de confirmação foi separada visualmente com um `⚠️` e recuo extra para destacá-la das outras saídas.
2. ✅ A função `buscar_por_nome` foi identificada como extensível — a busca por tipo já é possível via `listar --por tipo`, e isso foi documentado no README com um exemplo de uso combinado.

---

### 4.3 Melhorias Implementadas Após o Feedback

| # | Feedback | Mudança implementada | Arquivo(s) alterado(s) |
|---|---|---|---|
| 1 | Padrão de `listar` deveria ser `ambos` | Alterado default de `--por` para `ambos` | `main.py` |
| 2 | Mensagem de confirmação confusa visualmente | Adicionado `⚠️` e recuo na mensagem de `confirmar_acao` | `utils.py`, `main.py` |
| 3 | Falta exemplo de busca por tipo no README | Adicionada seção de exemplos combinados | `README.md` |

---

## 5. Análise de Qualidade do Código

### 5.1 Conformidade com PEP 8

O código foi verificado manualmente quanto às principais diretrizes do PEP 8:

| Critério | Status |
|---|---|
| Indentação de 4 espaços | ✅ |
| Linhas ≤ 99 caracteres | ✅ |
| Espaços em branco entre funções/classes | ✅ |
| Nomes em snake_case | ✅ |
| Constantes em UPPER_SNAKE_CASE | ✅ |
| Docstrings em funções públicas | ✅ |
| Type hints | ✅ |
| Imports organizados (stdlib → terceiros → locais) | ✅ |

### 5.2 Princípios de Design Aplicados

- **Separação de responsabilidades:** gerenciador (escrita), catalogador (leitura), utils (suporte)
- **Tratamento de exceções específicas:** `FileNotFoundError`, `FileExistsError`, `ValueError` — nunca `except Exception` genérico
- **Funções pequenas e coesas:** cada função faz uma coisa bem
- **Sem efeitos colaterais nos módulos de listagem:** `catalogador.py` nunca modifica arquivos

---

## 6. Conclusão

O sistema foi desenvolvido com foco em clareza de código, robustez nos tratamentos de erro e facilidade de uso via CLI. Todos os 37 testes automatizados passam, os testes manuais confirmaram o funcionamento correto das funcionalidades, e o feedback recebido foi integralmente incorporado antes da entrega final.

A arquitetura modular facilita futuras extensões, como adicionar suporte a novos tipos de arquivo, integrar com banco de dados ou expor as funcionalidades via API REST.

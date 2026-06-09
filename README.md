# 📚 Biblioteca Digital — Sistema de Gerenciamento de Documentos

Sistema de linha de comando desenvolvido em Python para a gestão eficiente de documentos digitais de uma biblioteca universitária. Permite organizar, adicionar, renomear, remover e buscar arquivos como PDFs, ePUBs, TXTs e outros formatos, com persistência de metadados e log completo de operações.

---

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Funcionalidades](#funcionalidades)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Como Usar](#como-usar)
- [Referência de Comandos](#referência-de-comandos)
- [Tipos de Arquivo Suportados](#tipos-de-arquivo-suportados)
- [Arquitetura](#arquitetura)
- [Testes](#testes)
- [Contribuição](#contribuição)
- [Licença](#licença)

---

## Visão Geral

A biblioteca universitária possui uma vasta coleção de artigos, teses e livros digitais. Este sistema substitui a gestão manual de arquivos por uma interface de linha de comando (CLI) estruturada, reduzindo erros e aumentando a produtividade dos bibliotecários.

---

## Funcionalidades

### Gerenciamento de Documentos
| Operação | Descrição |
|---|---|
| **Adicionar** | Copia um arquivo para o acervo organizado por tipo e ano |
| **Renomear** | Renomeia um documento preservando sua localização |
| **Remover** | Remove permanentemente um documento do acervo |
| **Abrir** | Abre o documento no aplicativo padrão do sistema |
| **Ler** | Exibe o conteúdo textual de arquivos `.txt` e `.md` |
| **Buscar** | Pesquisa documentos por nome (case-insensitive) |

### Catalogação e Listagem
| Operação | Descrição |
|---|---|
| **Listar por tipo** | Exibe todos os documentos agrupados por extensão |
| **Listar por ano** | Exibe todos os documentos agrupados por ano de publicação |
| **Listar por tipo e ano** | Exibição completa com agrupamento duplo |
| **Resumo do acervo** | Estatísticas gerais: total, contagem por tipo/ano, tamanho |

### Gerenciamento de Diretórios
| Operação | Descrição |
|---|---|
| **Listar diretórios** | Lista todos os subdiretórios do acervo |
| **Criar diretório** | Cria uma nova pasta no acervo |
| **Remover diretório** | Remove uma pasta (vazia ou com conteúdo) |

### Recursos Transversais
- **Persistência de metadados** em `metadados.json`
- **Log de operações** em `biblioteca_digital.log`
- **Confirmação interativa** antes de ações destrutivas
- **Tratamento de erros** com mensagens claras

---

## Estrutura do Projeto

```
biblioteca-digital/
│
├── main.py                     # Ponto de entrada — interface CLI
│
├── biblioteca/                 # Pacote principal
│   ├── __init__.py
│   ├── gerenciador.py          # Operações de arquivos e diretórios
│   ├── catalogador.py          # Listagem e organização do acervo
│   └── utils.py                # Constantes, helpers e validações
│
├── tests/                      # Testes unitários
│   ├── __init__.py
│   ├── test_gerenciador.py     # 19 testes para o gerenciador
│   └── test_catalogador.py     # 18 testes para o catalogador
│
├── acervo/                     # Armazenamento organizado dos documentos
│   ├── pdf/
│   │   ├── 2023/
│   │   └── 2024/
│   ├── epub/
│   └── txt/
│
├── metadados.json              # Registro persistente dos documentos
├── biblioteca_digital.log      # Log de todas as operações
├── requirements.txt            # Dependências do projeto
├── CONTRIBUTING.md             # Guia de contribuição
└── README.md                   # Esta documentação
```

---

## Requisitos

- **Python 3.9+**
- **pytest** (apenas para rodar os testes)

```
pytest>=7.0
```

---

## Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/sindelitcis/biblioteca-digital.git
cd biblioteca-digital
```

### 2. (Opcional) Crie um ambiente virtual

```bash
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

---

## Como Usar

Todos os comandos são executados a partir da raiz do projeto com `python main.py`.

### Exemplos rápidos

```bash
# Ver todos os comandos disponíveis
python main.py --help

# Listar acervo completo (por tipo e ano)
python main.py listar

# Adicionar um artigo PDF publicado em 2024
python main.py adicionar /downloads/artigo_ia.pdf --ano 2024

# Buscar documentos sobre "redes neurais"
python main.py buscar "redes neurais"

# Renomear um documento
python main.py renomear acervo/pdf/2024/artigo_ia.pdf artigo_ia_2024.pdf

# Remover um documento (com confirmação)
python main.py remover acervo/pdf/2024/artigo_antigo.pdf

# Ver resumo do acervo
python main.py resumo
```

---

## Referência de Comandos

### `listar`

Lista os documentos do acervo com diferentes organizações.

```
python main.py listar [--por {tipo|ano|ambos|diretorios}]
```

| Flag | Descrição | Padrão |
|---|---|---|
| `--por tipo` | Agrupa por extensão (PDF, ePUB...) | — |
| `--por ano` | Agrupa por ano de publicação | — |
| `--por ambos` | Agrupamento duplo tipo → ano | ✓ |
| `--por diretorios` | Lista apenas diretórios do acervo | — |

---

### `adicionar`

Adiciona um documento ao acervo, organizando-o automaticamente.

```
python main.py adicionar <ARQUIVO> --ano <ANO> [--tipo {pdf|epub|...}]
```

| Argumento | Descrição |
|---|---|
| `ARQUIVO` | Caminho do arquivo a adicionar |
| `--ano` | Ano de publicação (obrigatório) |
| `--tipo` | Tipo do arquivo — inferido pela extensão se omitido |

---

### `renomear`

Renomeia um documento dentro do acervo.

```
python main.py renomear <CAMINHO_ATUAL> <NOVO_NOME>
```

---

### `remover`

Remove um documento do acervo.

```
python main.py remover <CAMINHO> [--sim]
```

| Flag | Descrição |
|---|---|
| `--sim` | Confirma a remoção sem perguntar |

---

### `buscar`

Busca documentos cujo nome contenha o termo informado.

```
python main.py buscar <TERMO>
```

---

### `abrir`

Abre o documento no aplicativo padrão do sistema operacional.

```
python main.py abrir <CAMINHO>
```

---

### `ler`

Exibe o conteúdo de arquivos de texto (`.txt`, `.md`) diretamente no terminal.

```
python main.py ler <CAMINHO> [--linhas N]
```

| Flag | Descrição | Padrão |
|---|---|---|
| `--linhas` | Número máximo de linhas a exibir | 50 |

---

### `resumo`

Exibe estatísticas do acervo: total de documentos, contagem por tipo, por ano e tamanho total.

```
python main.py resumo
```

---

### `dir`

Gerencia diretórios do acervo.

```
python main.py dir criar <CAMINHO>
python main.py dir remover <CAMINHO> [--forcar] [--sim]
```

| Flag | Descrição |
|---|---|
| `--forcar` | Remove mesmo que o diretório não esteja vazio |
| `--sim` | Confirma sem perguntar |

---

### Exemplos Combinados

Estas combinações de comandos permitem tarefas mais específicas do dia a dia:

```bash
# Listar apenas documentos PDF do acervo
python main.py listar --por tipo | grep -A 1000 "PDF"

# Buscar documentos de um ano específico e ordenar por tipo
python main.py listar --por ambos

# Adicionar explicitamente informando o tipo (útil quando a extensão é ambígua)
python main.py adicionar tese.pdf --ano 2024 --tipo pdf

# Ver resumo após adicionar/remover para conferir o estado do acervo
python main.py resumo

# Remover um diretório inteiro de uma só vez (com confirmação)
python main.py dir remover acervo/epub/2021 --forcar --sim

# Buscar termo e depois abrir o resultado diretamente
python main.py buscar "aprendizado de máquina"
python main.py abrir acervo/pdf/2024/artigo_ml.pdf
```

---

## Tipos de Arquivo Suportados

| Extensão | Formato |
|---|---|
| `.pdf` | Portable Document Format |
| `.epub` | Electronic Publication |
| `.mobi` | Mobipocket eBook |
| `.txt` | Texto puro |
| `.md` | Markdown |
| `.docx` | Microsoft Word |
| `.djvu` | DjVu (escaneados) |

---

## Arquitetura

O sistema é dividido em três módulos com responsabilidades bem definidas:

```
main.py  ──►  biblioteca/gerenciador.py   (escreve/modifica arquivos)
         ──►  biblioteca/catalogador.py   (lê e organiza o acervo)
         ──►  biblioteca/utils.py         (constantes e helpers)
```

**`gerenciador.py`** — toda operação de escrita (adicionar, renomear, remover, criar/remover diretórios) passa por aqui. Também mantém o `metadados.json` atualizado.

**`catalogador.py`** — apenas leitura. Varre o acervo e retorna documentos organizados por tipo, ano ou ambos. Também provê busca e estatísticas.

**`utils.py`** — constantes globais (caminhos, tipos suportados), funções de exibição e validação usadas pelos outros módulos.

---

## Testes

O projeto conta com **37 testes unitários** cobrindo todos os módulos.

### Executar todos os testes

```bash
python -m pytest tests/ -v
```

### Executar testes de um módulo específico

```bash
python -m pytest tests/test_gerenciador.py -v
python -m pytest tests/test_catalogador.py -v
```

### Relatório de testes

Consulte o arquivo [`relatorio_testes.md`](relatorio_testes.md) para o relatório completo com resultados, análise de cobertura e feedback incorporado.

---

## Contribuição

Leia o guia completo em [CONTRIBUTING.md](CONTRIBUTING.md) antes de abrir issues ou pull requests.

---

## Licença

Este projeto é desenvolvido para fins acadêmicos. Uso livre para estudos.

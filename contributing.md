# 🤝 Guia de Contribuição — Biblioteca Digital

Obrigado por se interessar em contribuir com o projeto! Este guia explica como configurar o ambiente, criar branches, realizar commits e abrir pull requests de forma padronizada.

---

## 📋 Índice

- [Pré-requisitos](#pré-requisitos)
- [Fork e Clone](#fork-e-clone)
- [Fluxo de Trabalho com Git](#fluxo-de-trabalho-com-git)
- [Convenção de Commits](#convenção-de-commits)
- [Padrões de Código](#padrões-de-código)
- [Como Abrir um Pull Request](#como-abrir-um-pull-request)
- [Reportar Bugs](#reportar-bugs)

---

## Pré-requisitos

- Git 2.30+
- Python 3.9+
- Conta no GitHub

---

## Fork e Clone

### 1. Fork do repositório

Clique em **Fork** no canto superior direito da página do repositório no GitHub. Isso cria uma cópia pessoal do projeto na sua conta.

### 2. Clone o seu fork

```bash
git clone https://github.com/SEU-USUARIO/biblioteca-digital.git
cd biblioteca-digital
```

### 3. Adicione o repositório original como upstream

```bash
git remote add upstream https://github.com/ORIGINAL/biblioteca-digital.git
```

### 4. Verifique os remotes configurados

```bash
git remote -v
# origin    https://github.com/SEU-USUARIO/biblioteca-digital.git (fetch)
# origin    https://github.com/SEU-USUARIO/biblioteca-digital.git (push)
# upstream  https://github.com/ORIGINAL/biblioteca-digital.git (fetch)
# upstream  https://github.com/ORIGINAL/biblioteca-digital.git (push)
```

---

## Fluxo de Trabalho com Git

### 1. Sincronize com o repositório original antes de começar

```bash
git fetch upstream
git checkout main
git merge upstream/main
```

### 2. Crie uma branch descritiva para sua mudança

Use o padrão `tipo/descricao-curta`:

```bash
git checkout -b feat/adicionar-suporte-odt
git checkout -b fix/corrigir-listagem-vazia
git checkout -b docs/melhorar-readme
git checkout -b test/cobertura-utils
```

Tipos de branch:
| Prefixo | Uso |
|---|---|
| `feat/` | Nova funcionalidade |
| `fix/` | Correção de bug |
| `docs/` | Apenas documentação |
| `test/` | Adição ou correção de testes |
| `refactor/` | Refatoração sem mudança funcional |
| `chore/` | Tarefas de manutenção (deps, CI) |

### 3. Faça suas alterações e commits

```bash
# Verifique o que mudou
git status
git diff

# Adicione apenas os arquivos relacionados à sua mudança
git add biblioteca/gerenciador.py

# Nunca use: git add .  (evita commitar arquivos desnecessários)

# Crie o commit
git commit -m "feat: adicionar suporte a arquivos .odt"
```

### 4. Mantenha sua branch atualizada durante o desenvolvimento

```bash
git fetch upstream
git rebase upstream/main
```

### 5. Envie sua branch para o seu fork

```bash
git push origin feat/adicionar-suporte-odt
```

---

## Convenção de Commits

Este projeto segue o padrão **Conventional Commits**. Cada mensagem deve seguir a estrutura:

```
tipo(escopo opcional): descrição curta no imperativo

[corpo opcional — explica o porquê, não o quê]

[rodapé opcional — referência a issue: Closes #42]
```

### Tipos permitidos

| Tipo | Quando usar |
|---|---|
| `feat` | Nova funcionalidade para o usuário |
| `fix` | Correção de bug |
| `docs` | Mudanças apenas na documentação |
| `test` | Adição ou correção de testes |
| `refactor` | Refatoração de código (sem feat e sem fix) |
| `style` | Formatação, espaços, ponto-e-vírgula (sem mudança de lógica) |
| `chore` | Atualização de dependências, configuração |

### Exemplos de boas mensagens

```bash
feat: adicionar busca por autor nos metadados
fix: corrigir erro ao renomear arquivo com espaço no nome
docs: atualizar exemplos de uso no README
test: adicionar testes para busca case-insensitive
refactor: extrair lógica de validação para utils.py
chore: adicionar pytest ao requirements.txt
```

### Exemplos de mensagens ruins (evitar)

```bash
git commit -m "fix"                    # ❌ Sem descrição
git commit -m "mudanças"               # ❌ Vago
git commit -m "WIP"                    # ❌ Não usar em commits públicos
git commit -m "atualizei vários arquivos"   # ❌ Fora do padrão
```

---

## Padrões de Código

### PEP 8

Todo código deve seguir o guia de estilo PEP 8. Pontos principais:

- Indentação com **4 espaços** (não tabs)
- Linhas com **no máximo 99 caracteres**
- Duas linhas em branco entre funções/classes de nível de módulo
- Uma linha em branco entre métodos dentro de uma classe
- Nomes de variáveis e funções em **snake_case**
- Nomes de classes em **PascalCase**
- Constantes em **UPPER_SNAKE_CASE**

### Docstrings

Todas as funções públicas devem ter docstring no formato Google Style:

```python
def adicionar_documento(origem: str, ano: int, tipo: str = None) -> dict:
    """
    Descrição curta em uma linha.

    Descrição longa opcional explicando comportamento,
    casos de borda, etc.

    Args:
        origem (str): Descrição do parâmetro.
        ano (int): Ano de publicação.
        tipo (str, opcional): Tipo do documento.

    Returns:
        dict: Descrição do retorno.

    Raises:
        FileNotFoundError: Quando o arquivo não existe.
        ValueError: Quando o tipo não é suportado.
    """
```

### Type hints

Use type hints em todas as funções:

```python
def buscar_por_nome(termo: str) -> list:
    ...
```

### Testes

- Todo novo código deve vir acompanhado de testes unitários
- Use `unittest.TestCase` como classe base
- Nomeie os testes com `test_<o_que_testa>`
- Isole os testes usando diretórios temporários (`tempfile.mkdtemp()`)

---

## Como Abrir um Pull Request

1. Certifique-se de que todos os testes passam:
   ```bash
   python -m pytest tests/ -v
   ```

2. Faça o push da sua branch para o seu fork:
   ```bash
   git push origin feat/sua-funcionalidade
   ```

3. Acesse o repositório original no GitHub e clique em **"Compare & pull request"**.

4. Preencha o template de PR:
   - **Título:** siga a convenção de commits (ex: `feat: adicionar suporte a .odt`)
   - **Descrição:** explique o que foi feito e por quê
   - **Issues relacionadas:** mencione com `Closes #<número>` se aplicável
   - **Testes:** confirme que todos os testes passam

5. Aguarde o review. Responda os comentários e faça ajustes se necessário.

### Checklist antes de abrir o PR

- [ ] Os testes passam (`pytest tests/ -v`)
- [ ] O código segue o PEP 8
- [ ] Funções novas têm docstrings
- [ ] O README foi atualizado se necessário
- [ ] O commit segue a convenção Conventional Commits

---

## Reportar Bugs

Ao abrir uma issue de bug, inclua:

1. **Descrição** do comportamento inesperado
2. **Passos para reproduzir** o erro
3. **Comportamento esperado**
4. **Comportamento obtido** (incluindo mensagem de erro completa)
5. **Ambiente:** sistema operacional e versão do Python

```
**Descrição:** O comando `renomear` falha silenciosamente quando...

**Reprodução:**
1. Execute `python main.py adicionar arquivo.pdf --ano 2024`
2. Execute `python main.py renomear acervo/pdf/2024/arquivo.pdf novo nome com espaço.pdf`

**Esperado:** Arquivo renomeado com sucesso.
**Obtido:** Erro: FileNotFoundError...

**Ambiente:** Ubuntu 22.04, Python 3.11.2
```

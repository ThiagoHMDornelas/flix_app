# Flix App

![Testes](https://github.com/ThiagoHMDornelas/flix_app/actions/workflows/tests.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![Streamlit](https://img.shields.io/badge/streamlit-1.52-FF4B4B)
![License](https://img.shields.io/badge/license-MIT-green)

Aplicação web para gerenciamento de filmes, desenvolvida com Streamlit. Serve como frontend do sistema, consumindo a [Flix API](https://github.com/ThiagoHMDornelas/flix_api) para autenticar, consultar e cadastrar dados.

## Sumário

- [Visão geral](#visão-geral)
- [Funcionalidades](#funcionalidades)
- [Tecnologias](#tecnologias)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Instalação e execução](#instalação-e-execução)
- [Variáveis de ambiente](#variáveis-de-ambiente)
- [Executar com Docker](#executar-com-docker)
- [Testes](#testes)
- [Fluxo da aplicação](#fluxo-da-aplicação)
- [Organização do código](#organização-do-código)
- [Relação com o Flix API](#relação-com-o-flix-api)
- [Licença](#licença)

## Visão geral

O **Flix App** é o frontend do sistema de catálogo de filmes. Ele consome os endpoints da Flix API, autentica o usuário via JWT e oferece uma interface web em Streamlit para consultar e cadastrar filmes, gêneros, atores/atrizes e avaliações.

## Funcionalidades

- Login de usuários com autenticação JWT
- Dashboard com estatísticas (filmes por gênero, totais e média de avaliações)
- Listagem de filmes, gêneros, atores/atrizes e avaliações em grid interativo
- Cadastro de filmes, gêneros, atores/atrizes e avaliações
- Grid com busca global, filtros, seleção de colunas e exportação para CSV
- Logout e tratamento automático de token expirado

## Tecnologias

- Python
- Streamlit
- Requests
- Plotly
- Streamlit AgGrid
- Streamlit Option Menu
- Pandas
- python-decouple
- Docker e Docker Compose
- GitHub Actions (CI)
- flake8 (desenvolvimento)

## Estrutura do projeto

```
flix_app/
├── api/              # cliente HTTP da Flix API (autenticação)
├── components/       # componentes reutilizáveis (grid de dados)
├── login/            # tela e lógica de login
├── home/             # dashboard com estatísticas
├── movies/           # gerenciamento de filmes
├── genres/           # gerenciamento de gêneros
├── actors/           # gerenciamento de atores/atrizes
├── reviews/          # gerenciamento de avaliações
├── tests/            # testes unitários
├── constants.py      # configurações e constantes
├── app.py            # ponto de entrada da aplicação
├── requirements.txt
└── requirements_dev.txt
```

Cada módulo segue a mesma divisão: `page.py` (interface), `service.py` (regras/cache) e `repository.py` (comunicação com a API).

## Instalação e execução

Pré-requisitos:

- Python 3.11 ou superior instalado
- [Flix API](https://github.com/ThiagoHMDornelas/flix_api) em execução

Acesse a pasta do projeto:

    cd flix_app

Crie um ambiente virtual:

    python -m venv .venv

No Windows, ative o ambiente virtual:

    .venv\Scripts\activate

No Linux ou macOS, ative o ambiente virtual:

    source .venv/bin/activate

Instale as dependências:

    pip install -r requirements.txt

Opcionalmente, para desenvolvimento (lint), instale também:

    pip install -r requirements_dev.txt

Inicie a aplicação:

    streamlit run app.py

A aplicação estará disponível em:

    http://localhost:8501

## Variáveis de ambiente

As configurações são lidas de variáveis de ambiente. O projeto usa o pacote `python-decouple` para carregar um arquivo `.env` na raiz.

1. Copie o arquivo de exemplo:

    No Windows:

        copy .env.example .env

    No Linux ou macOS:

        cp .env.example .env

2. Ajuste a URL da API, se necessário.

Variáveis disponíveis:

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `BASE_URL` | URL base da Flix API | `http://127.0.0.1:8000/api/v1/` |

O arquivo `.env` não é versionado (está no `.gitignore`).

## Executar com Docker

A forma recomendada de rodar o frontend. O Docker Compose sobe o serviço já configurado, sem precisar montar o ambiente Python manualmente.

**Pré-requisitos:**

- Docker Desktop instalado e em execução (engine)
- Docker Compose (já vem com o Docker Desktop)
- Git instalado (para clonar o repositório)
- A [Flix API](https://github.com/ThiagoHMDornelas/flix_api) em execução na máquina host, na porta `8000`
- A porta `8501` livre

> **Importante:** o Docker Desktop sozinho **não** faz o setup inicial — ele é o *engine* e o painel de gerenciamento. Clonar o repositório e rodar `docker compose up --build` são feitos pelo **terminal**; o Docker Desktop é ótimo para acompanhar logs, iniciar/parar e abrir um terminal dentro do container **depois** que a stack subiu.

> O Docker **não** precisa do arquivo `.env`: o `docker-compose.yml` já define `BASE_URL` apontando para a Flix API no host (`http://host.docker.internal:8000/api/v1/`). O `.env.example` é usado apenas na execução local (fora do Docker).

### Passo a passo (via shell / PowerShell)

**1. Clone o repositório**

```powershell
git clone https://github.com/ThiagoHMDornelas/flix_app.git
cd flix_app
```

> O `git clone` cria a pasta `flix_app` dentro da pasta atual, e o `cd` entra nela. Se você **já está dentro** da pasta do projeto, **pule o `cd`**.

**2. Suba a stack.** Na primeira execução o Docker compila a imagem do projeto — pode levar alguns minutos:

```powershell
docker compose up --build -d
```

**3. Confira os containers:**

```powershell
docker compose ps
```

Espere o serviço `web` como `Up`.

| Serviço | Porta | Acesso |
|---|---|---|
| `web` | 8501 | `http://localhost:8501` |

**4. Acesse a aplicação:**

- Aplicação: `http://localhost:8501`

**5. Comandos úteis:**

```powershell
docker compose logs -f web     # logs da aplicação
docker compose restart web     # reinicia a aplicação
docker compose down            # para e remove os containers
```

> O container acessa a Flix API pela URL definida em `BASE_URL`. Por padrão, o `docker-compose.yml` usa `http://host.docker.internal:8000/api/v1/`, que aponta para a API em execução na máquina host. Por isso a **Flix API precisa estar rodando** na porta `8000` antes de usar o frontend.

### Usando o Docker Desktop (interface gráfica)

Depois que a stack estiver no ar (passo 2), o Docker Desktop ajuda a operar. Na aba **Containers** você verá o serviço `web`:

- **Logs**: clique no container → aba *Logs* (equivale a `docker compose logs`).
- **Start / Stop / Restart**: botões no topo do container.
- **Terminal no container**: botão *Exec* (útil para depurar dentro do container).
- **Abrir no navegador**: clique na porta publicada (`8501:8501`).

O que **não** dá para fazer pela interface gráfica: clonar o repositório e rodar `docker compose up --build` em um clone novo (isso é feito pelo terminal).

### Problemas comuns

- **A aplicação abre, mas não carrega dados / login falha** → a **Flix API não está rodando** na máquina host. Suba a API (na porta `8000`) e recarregue a página.
- **A aplicação não abre**
  - Veja os logs: `docker compose logs -f web`
  - Confirme que o container está `Up`: `docker compose ps`
- **Erro de porta em uso** (`8501`) → pare o serviço que ocupa a porta ou ajuste o mapeamento no `docker-compose.yml` (ex.: `8502:8501`) e acesse em `http://localhost:8502`

## Testes

A suíte de testes cobre o cliente de autenticação (sucesso e erro) e o mapeamento de constantes. Execute:

    python -m unittest discover -v

A suíte também roda automaticamente a cada `push` e `pull request` via **GitHub Actions** (`.github/workflows/tests.yml`), e o resultado é exibido no badge no topo deste README.

## Fluxo da aplicação

O usuário acessa o Flix App e realiza o login. O aplicativo envia as credenciais ao endpoint de autenticação da Flix API e, em caso de sucesso, armazena o token JWT na sessão para as próximas requisições.

    Usuário
        |
        v
    Flix App
        |
        v
    Flix API
        |
        v
    Banco de dados

## Organização do código

A comunicação segue a camada:

    Página -> Service -> Repository -> API

- `page.py`: monta a interface (Streamlit) e trata o retorno ao usuário;
- `service.py`: concentra a lógica e o cache;
- `repository.py`: faz as requisições HTTP à Flix API.

## Relação com o Flix API

O **Flix App** funciona como frontend do sistema. Ele depende da **Flix API** para funcionar corretamente e não acessa diretamente o banco de dados — todas as operações são realizadas por meio dos endpoints da API.

> https://github.com/ThiagoHMDornelas/flix_api

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

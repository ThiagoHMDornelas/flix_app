# Flix App

![Testes](https://github.com/ThiagoHMDornelas/flix_app/actions/workflows/tests.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![Streamlit](https://img.shields.io/badge/streamlit-1.52-FF4B4B)

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

Com o Docker e o Docker Compose instalados, é possível subir a aplicação sem configurar o ambiente Python manualmente:

    docker compose up --build

A aplicação estará disponível em:

    http://localhost:8501

Para parar e remover os containers:

    docker compose down

O container acessa a Flix API pela URL definida em `BASE_URL`. Por padrão, o `docker-compose.yml` usa `http://host.docker.internal:8000/api/v1/`, que aponta para a API em execução na máquina host.

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

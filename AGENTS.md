# AGENTS.md — flix_app

Frontend Streamlit do catálogo de filmes: login JWT, grids interativos (`streamlit-aggrid`), dashboard com Plotly, consumindo a `flix-api`. Streamlit 1.52.2 · pandas 2.3.3 · Plotly 6.5.0 · streamlit-aggrid 1.2.1 · streamlit-option-menu · requests · python-decouple · Python 3.12 · Docker (porta 8501).

## Contexto em camadas
`SOUL.md` (regras globais do agente) → `AGENTS.md` da pasta da linguagem (regras comuns) → este arquivo (particularidades do projeto). Em conflito, vale o mais específico (este arquivo), exceto em regras de segurança/global.

## Arquitetura

Projeto **não-Django**: app Streamlit puro, organizado por entidade em pacotes (cada pacote tem `page.py`, `service.py` e `repository.py`).

### Estrutura

| Pasta | Finalidade | Particularidades |
|---|---|---|
| `app.py` | Entrada + navegação | `option_menu` no sidebar; token em `st.session_state['token']` decide login vs telas |
| `login/` | Autenticação JWT | `show_login()` com validação de campos vazios; guarda token na session |
| `home/` | Dashboard com estatísticas | Consumo `/movies/stats/` da API |
| `genres/`, `actors/`, `movies/`, `reviews/` | Telas por entidade | Mesma tríade; `movies/` tem grid com formulário e stats |
| `api/service.py` | Cliente `Auth` (único endpoint compartilhado) | `requests.post` em `${BASE_URL}authentication/token/`; reflete erro com status code |
| `components/grid.py` | Grid genérico `AgGrid` | Busca global, multiselect de colunas, botão limpar filtros, CSV export; aceita `key` único por tela |
| `constants.py` | `BASE_URL` + nacionalidades | `NATIONALITY_CHOICES` (Brasil→BRL, EUA→USA); `Base URL` default `http://127.0.0.1:8000/api/v1/` |
| `tests/` | Testes unittest | `test_api_service.py` (Auth) e `test_constants.py` |

## Camadas por tela (padrão obrigatório)

- **`page.py`** — interação pura com Streamlit (formulários, grids), chama o service.
- **`service.py`** — lógica de negócio, cache de dados de listagem com `@st.cache_data(ttl=...)`; após create, limpa o cache (`_get_genres_cached.clear()`).
- **`repository.py`** — chamadas `requests` com header `Authorization: Bearer <st.session_state.token>`. **Contrato de erro**: 200/201 → dados; 401 → `logout()` (token vencido) e `return None`; qualquer outro status → `raise Exception`.

Requer a `flix-api` no ar (rota default `http://127.0.0.1:8000/api/v1/`). Sem backend, login e telas falham.

## Testes e lint

- Suíte obrigatória antes de entregar: **`python -m unittest discover -v`** (runner nativo unittest, pasta `tests/`, com `__init__.py`).
- Lint com flake8 (`.flake8`: ignora E501, exclui `.venv`).
- CI (`.github/workflows/tests.yml`): roda `python -m unittest discover -v` em Python 3.12 (sem flake8). Testes usam `unittest.mock.patch` para mockar `requests` — sem backend no ar.

## Variáveis de ambiente

Uma única variável: `BASE_URL=http://127.0.0.1:8000/api/v1/` (lida com `python-decouple`).

## Contrato com a flix-api

- Único acoplamento: `BASE_URL`. Docker usa `http://host.docker.internal:8000/api/v1/` com `extra_hosts` (`host-gateway`) para atingir a API rodando no host.
- Endpoints consumidos: `authentication/token/`, `genres/`, `actors/`, `movies/`, `movies/stats/`, `reviews/`. Mudanças de rota/payload/autenticação na API quebram o app — atualizar os dois projetos em par.

## Padrões do Streamlit (pegadinhas)

- Streamlit **re-executa o script inteiro a cada interação**: serviços cacheados com `st.cache_data` e `st.session_state` para token e página anterior.
- Trocar página no menu limpa **todos** os caches (`st.cache_data.clear()`).
- Formulários usam `st.form`; webhooks de campo obrigatório usam `st.warning`.

## Docker

Serviço único na porta `8501` (Dockerfile já roda o Streamlit headless); usa `http://host.docker.internal:8000/api/v1/` com `extra_hosts` (`host-gateway`) para atingir a API no host.

## Convenções

- Secrets **sempre** em `.env` (nunca hardcode); mantenha o `.env.example` atualizado e o `.env` fora do versionamento.
- Migrações que apagam ou tornam campo obrigatório sem `default` precisam de aviso antes de rodar em produção.
- Mensagens de UI/validação em português do Brasil, revisadas (acentuação e concordância).
- Não commitar/pushar por conta própria: as alterações ficam prontas para o usuário revisar e commitar.
- Preservar encoding dos arquivos ao editar (não converter ANSI ↔ UTF-8 sem pedido explícito).

# AGENTS.md — flix_app

> Gerado automaticamente na clonagem para a VPS (21/10/2026). **Revisar**: ajuste o que não bater com a realidade do projeto.

## Visão geral
**Frontend Streamlit** do catálogo de filmes: login JWT, tabelas com `streamlit-aggrid` e gráficos com Plotly, consumindo a `flix_api`.

**Stack:** Streamlit 1.52 · pandas · Plotly · streamlit-aggrid · requests · python-decouple · Python 3.12 · Docker (porta 8501)

## Contexto em camadas
`~/.hermes/SOUL.md` (regras globais) → `~/projetos/python/AGENTS.md` (regras da linguagem) → este arquivo (particularidades do projeto).
Em conflito, vale o mais específico (este arquivo), exceto em regras de segurança/global.

## Estrutura
- `app.py` — entrada da aplicação Streamlit
- `components/` — componentes reutilizáveis
- `login/`, `home/` — telas
- `movies/`, `actors/`, `genres/`, `reviews/` — telas por entidade
- `api/` — clientes HTTP da Flix API
- `constants.py` — constantes/config compartilhadas

## Como rodar
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r requirements_dev.txt
cp .env.example .env    # BASE_URL apontando para a flix_api
streamlit run app.py
```
Requer a `flix_api` no ar.

## Testes e lint
```bash
python -m unittest discover -v
flake8
```

## Particularidades
- `BASE_URL` no `.env` é o único acoplamento com o backend.
- Streamlit reexecuta o script a cada interação: cachear chamadas de API (`st.cache_data`) e evitar estado global mutável.
- Docker expõe 8501 (não 8000).

## Convenções
- Secrets **sempre** em `.env` (nunca hardcode); mantenha o `.env.example` atualizado e o `.env` fora do versionamento.
- Migrações que apagam ou tornam campo obrigatório sem `default` precisam de aviso antes de rodar em produção.
- Mensagens de UI/validação em português do Brasil, revisadas (acentuação e concordância).
- Não commitar/pushar por conta própria: as alterações ficam prontas para o usuário revisar e commitar.
- Preservar encoding dos arquivos ao editar (não converter ANSI ↔ UTF-8 sem pedido explícito).

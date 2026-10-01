from decouple import config

# URL base da API (configurável via arquivo .env)
BASE_URL = config('BASE_URL', default='http://127.0.0.1:8000/api/v1/')

NATIONALITY_CHOICES = {
    'Brasil': 'BRL',
    'Estados Unidos': 'USA',
}

# Dicionário reverso para exibição
NATIONALITY_DISPLAY = {v: k for k, v in NATIONALITY_CHOICES.items()}

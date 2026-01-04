# url base
# BASE_URL = 'http://127.0.0.1:8000/api/v1/'
BASE_URL = 'https://thiagodornelas.pythonanywhere.com/api/v1/'

NATIONALITY_CHOICES = {
    'Brasil': 'BRL',
    'Estados Unidos': 'USA',
}

# Dicionário reverso para exibição
NATIONALITY_DISPLAY = {v: k for k, v in NATIONALITY_CHOICES.items()}

# NATIONALITY_DISPLAY = {}
# for k, v in NATIONALITY_CHOICES.items():
#     NATIONALITY_DISPLAY[v] = k

# # Resultado:
# # NATIONALITY_DISPLAY = {'BRL': 'Brasil', 'USA': 'Estados Unidos'}

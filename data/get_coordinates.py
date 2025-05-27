import googlemaps 
import pandas as pd
import time

# Inicializa o cliente da API
gKey = 'Insira sua chave'
gmaps = googlemaps.Client(key=gKey)

# Lê o CSV
df = pd.read_csv("20250401_atividade_economica.csv", sep=";", on_bad_lines='skip', engine='python')

# Função para montar o endereço corretamente
def montar_endereco(row):
    logradouro = f"{str(row.get('DESC_LOGRADOURO', '')).strip()} {str(row.get('NOME_LOGRADOURO', '')).strip()}".strip()
    numero = str(row.get('NUMERO_IMOVEL', '')).strip()
    bairro = str(row.get('NOME_BAIRRO', '')).strip()

    campos = [logradouro, numero, bairro, 'Belo Horizonte', 'MG', 'Brasil']
    campos = [c for c in campos if c]
    return ', '.join(campos)

# Listas pra armazenar resultados
latitudes = []
longitudes = []
status_api = []

# Loop pelas linhas
for i, row in df.iterrows():
    endereco = montar_endereco(row)
    try:
        geocode_result = gmaps.geocode(endereco)
        if geocode_result:
            location = geocode_result[0]['geometry']['location']
            latitudes.append(location['lat'])
            longitudes.append(location['lng'])
            status_api.append('OK')
        else:
            latitudes.append(None)
            longitudes.append(None)
            status_api.append('ZERO_RESULTS')
    except Exception as e:
        latitudes.append(None)
        longitudes.append(None)
        status_api.append(str(e))

    time.sleep(0.1)  # evita estourar limite de requisições por segundo

# Adiciona colunas no DataFrame original
df['LATITUDE'] = latitudes
df['LONGITUDE'] = longitudes
df['STATUS_GEOCODIFICACAO'] = status_api

# Salva em CSV
df.to_csv("atividade_economica_com_coords.csv", sep=';', index=False)
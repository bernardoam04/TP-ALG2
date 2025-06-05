import csv
import requests
import os

os.makedirs("imagens", exist_ok=True)

# Caminho para o CSV
caminho_csv = "comida_di_buteco.csv"

with open(caminho_csv, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        id_estabelecimento = row["ID_ATIV_ECON_ESTABELECIMENTO"]
        imagem_url = row["Link Imagem"]

        if not imagem_url:
            continue

        try:
            response = requests.get(imagem_url, timeout=10)
            if response.status_code == 200:
                caminho_arquivo = f"imagens/{id_estabelecimento}.jpg"
                with open(caminho_arquivo, "wb") as f:
                    f.write(response.content)
                print(f"Salvou imagem: {caminho_arquivo}")
            else:
                print(f"Erro {response.status_code} ao baixar {imagem_url}")
        except Exception as e:
            print(f"Erro ao baixar {imagem_url}: {e}")

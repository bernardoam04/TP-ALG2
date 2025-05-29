import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0'}

dados = []

for page in range(1, 12):  # páginas de 1 a 11
    url = f"https://comidadibuteco.com.br/butecos/belo-horizonte/page/{page}/"
    print(f"🔎 Página {page}: {url}")
    
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        print(f"❌ Falha na página {page}")
        continue

    soup = BeautifulSoup(resp.text, 'html.parser')

    itens = soup.find_all("div", class_="item")

    for item in itens:
        nome_tag = item.find("h2")
        nome = nome_tag.get_text(strip=True) if nome_tag else "Sem nome"

        link_tag = item.find("a", string="Detalhes")
        link = link_tag['href'] if link_tag else "Sem link"

        dados.append({'Nome': nome, 'Link Detalhes': link})

# Criar DataFrame
df = pd.DataFrame(dados)
print(df)

# (Opcional) salvar como CSV
df.to_csv("butecos_bh.csv", index=False)

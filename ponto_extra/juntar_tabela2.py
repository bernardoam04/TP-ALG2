import pandas as pd

df_cdb = pd.read_csv("bares_completos_com_petisco.csv", on_bad_lines='skip', engine='python')
df_cdb_foto = pd.read_csv("butecos_bh.csv", on_bad_lines='skip', engine='python')

df_cdb['Link Imagem'] = ""

lookup_foto = dict(zip(df_cdb_foto['Nome'], df_cdb_foto['Link Imagem']))

for i, row in df_cdb.iterrows():
    nome_bar = row['Nome']
    if nome_bar in lookup_foto:
        df_cdb.at[i, 'Link Imagem'] = lookup_foto[nome_bar]
    else:
        df_cdb.at[i, 'Link Imagem'] = "Sem foto"

df_cdb.to_csv("bares_completos_com_petisco_e_foto.csv", index=False)

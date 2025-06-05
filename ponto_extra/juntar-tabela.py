import pandas as pd
df_cdb = pd.read_csv("comida_di_buteco.csv", on_bad_lines='skip', engine='python')
df_bares = pd.read_csv("../docs/bares_com_cdb.csv", sep=";", on_bad_lines='skip', engine='python')

df_cdb['ID_ATIV_ECON_ESTABELECIMENTO'] = df_cdb['ID_ATIV_ECON_ESTABELECIMENTO'].astype(int)
df_bares['ID_ATIV_ECON_ESTABELECIMENTO'] = df_bares['ID_ATIV_ECON_ESTABELECIMENTO'].astype(int)

ids_cdb = set(df_cdb['ID_ATIV_ECON_ESTABELECIMENTO'])

df_bares['cdb'] = df_bares['ID_ATIV_ECON_ESTABELECIMENTO'].apply(lambda x: 1 if x in ids_cdb else 0)

print(len(df_bares[df_bares['cdb'] == 1]))
import pandas as pd

# Lê o CSV original
df = pd.read_csv("20250401_atividade_economica.csv", sep=";", on_bad_lines='skip', engine='python')

# Lista de descrições permitidas
valores_permitidos = [
    "RESTAURANTES E SIMILARES",
    "BARES E OUTROS ESTABELECIMENTOS ESPECIALIZADOS EM SERVIR BEBIDAS, COM ENTRETENIMENTO",
    "BARES E OUTROS ESTABELECIMENTOS ESPECIALIZADOS EM SERVIR BEBIDAS, SEM ENTRETENIMENTO"
]

# Filtra mantendo apenas os valores desejados
df_filtrado = df[df["DESCRICAO_CNAE_PRINCIPAL"].isin(valores_permitidos)]

# Sobrescreve o CSV original com os dados filtrados
df_filtrado.to_csv("20250401_atividade_economica.csv", index=False, sep=";")

import pandas as pd

# Lê o CSV original
df = pd.read_csv("20250401_atividade_economica.csv", sep=";", on_bad_lines='skip', engine='python')

df_filtrado = df[df['DESCRICAO_CNAE_PRINCIPAL'].str.contains(
    r'\b(?:bar|bares|restaurante|restaurantes)\b',
    case=False,
    na=False
)]


# Sobrescreve o CSV original com os dados filtrados
df_filtrado.to_csv("20250401_atividade_economica.csv", index=False, sep=";")
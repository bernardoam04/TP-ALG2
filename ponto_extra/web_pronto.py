import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import traceback 

df = pd.read_csv('../data/bares_cdb.csv')
print("[INFO] DataFrame original 'df' após leitura do CSV (primeiras linhas):")
print(df.head())
print("[INFO] dtypes do DataFrame original 'df':")
print(df.dtypes)


limite = None  


def extrair_dados_completos_buteco(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        nome_petisco_final = None 
        descricao_final = None
        endereco_final = None

        section_text_div = soup.find('div', class_='section-text')

        if section_text_div:
            direct_p_tags = section_text_div.find_all('p', recursive=False)
            paragraphs_with_b = [p for p in direct_p_tags if p.find('b')]

            if not paragraphs_with_b and section_text_div.find_all('p'): 
                all_p_tags_in_div = section_text_div.find_all('p')
                paragraphs_with_b = [p for p in all_p_tags_in_div if p.find('b')]

            if len(paragraphs_with_b) > 0:
                p_descricao_tag = paragraphs_with_b[0]
                b_tag_descricao = p_descricao_tag.find('b')
                if b_tag_descricao:
                    nome_petisco_capturado = b_tag_descricao.get_text(strip=True)
                    nome_petisco_final = nome_petisco_capturado
                    
                    texto_completo_p_descricao = p_descricao_tag.get_text(strip=True)
                    if texto_completo_p_descricao.startswith(nome_petisco_capturado):
                        descricao_final = texto_completo_p_descricao[len(nome_petisco_capturado):].strip()
                    else:
                        descricao_final = texto_completo_p_descricao.replace(nome_petisco_capturado, '', 1).strip()
                else:
                    descricao_final = p_descricao_tag.get_text(strip=True)
        
            if len(paragraphs_with_b) > 1:
                p_endereco_tag = paragraphs_with_b[1]
                b_tag_endereco = p_endereco_tag.find('b')
                if b_tag_endereco and "Endereço:" in b_tag_endereco.get_text():
                    texto_completo_p_endereco = p_endereco_tag.get_text(strip=True)
                    label_endereco = b_tag_endereco.get_text(strip=True)
                    if texto_completo_p_endereco.startswith(label_endereco):
                        endereco_final = texto_completo_p_endereco[len(label_endereco):].strip()
                    else:
                        endereco_final = texto_completo_p_endereco.replace(label_endereco, '', 1).strip()
                elif "Endereço:" in p_endereco_tag.get_text(strip=True):
                    texto_completo_p_endereco = p_endereco_tag.get_text(strip=True)
                    partes_endereco = texto_completo_p_endereco.split("Endereço:", 1)
                    if len(partes_endereco) > 1:
                        endereco_final = partes_endereco[1].strip()
                    else:
                        endereco_final = texto_completo_p_endereco
                else:
                    endereco_final = p_endereco_tag.get_text(strip=True)
            
        return {'Nome Petisco': nome_petisco_final, 'Descricao': descricao_final, 'Endereco': endereco_final}

    except requests.exceptions.HTTPError as e:
        print(f"[ERRO HTTP] {url}: {e.response.status_code} {e.response.reason}")
        return {'Nome Petisco': None, 'Descricao': None, 'Endereco': None}
    except requests.exceptions.RequestException as e:
        print(f"[ERRO DE REQUISIÇÃO] {url}: {e}")
        return {'Nome Petisco': None, 'Descricao': None, 'Endereco': None}
    except Exception as e:
        print(f"[ERRO INESPERADO DURANTE PARSING] {url}: {e.__class__.__name__} {e}")
        traceback.print_exc()
        return {'Nome Petisco': None, 'Descricao': None, 'Endereco': None}

total_linhas_csv = len(df)
linhas_a_processar = total_linhas_csv if limite is None else min(limite, total_linhas_csv)

df_processado_slice = df.iloc[:linhas_a_processar]

dados_extraidos = []
for i, row in df_processado_slice.iterrows():
    indice_atual_df = row.name
    print(f"Processando linha {indice_atual_df + 1}/{total_linhas_csv}: {row['Nome']} - {row['Link Detalhes']}")
    info = extrair_dados_completos_buteco(row['Link Detalhes'])
    dados_extraidos.append(info)

if not dados_extraidos:
    print("Nenhum dado foi extraído. Verifique os logs de erro e a lógica de extração.")
else:
    df_temp_extraido = pd.DataFrame(dados_extraidos, index=df_processado_slice.index)
    
    print("\n[INFO] DataFrame temporário com dados extraídos (primeiras linhas):")
    print(df_temp_extraido.head())
    print("[INFO] dtypes de 'df_temp_extraido':")
    print(df_temp_extraido.dtypes)

    colunas_para_atualizar = ['Nome Petisco', 'Descricao', 'Endereco']

    for coluna in colunas_para_atualizar:
        if coluna in df_temp_extraido:
            df.loc[df_temp_extraido.index, coluna] = df_temp_extraido[coluna]
    


df.to_csv('bares_completos_com_petisco.csv', index=False) 
try:
    df_final_lido = pd.read_csv('bares_completos_com_petisco.csv')
    print(df_final_lido.head())
except FileNotFoundError:
    print("Arquivo 'bares_completos_com_petisco.csv' não encontrado para verificação.")
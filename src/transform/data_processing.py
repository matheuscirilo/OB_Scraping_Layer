import pandas as pd
import json
from sqlalchemy import create_engine

class ImoveisDataProcessor:
    def __init__(self):
        pass
   
    def process_data(self, df):
        df['codigo'] = df['codigo'].str.replace(r'^Cód: ', '', regex=True)
        df['titulo'] = df['titulo'].str.split().str[0].str.lower()
        df['status'] = df['status'].str.replace(r'^- ', '', regex=True)

        df[['bairro', 'cidade', 'estado']] = df['localidade'].str.split(r'[-/]', expand=True)
        df.drop(columns= ['localidade'], inplace=True)

        df['area_total_m2'] = df['area_total'].str.split().str[0].str.replace('.', '').str.replace(',', '.').astype(float)
        df['preco'] = df['preco'].str.replace(r'^R\$ ', '', regex=True).str.replace('.', '').str.replace(',', '.').astype(float)
        return df
    
    def load_data_from_jsonl(self)-> None:
        try:
            data = []
            file_path = '../extract/data/imoveis_casa_feliz.jsonl'
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    json_obj = json.loads(line)
                    data.append(json_obj)
            df = pd.DataFrame(data)
            self.process_data(df)
            print(f"Arquivo '{file_path}' carregado com sucesso.")
        except FileNotFoundError:
            print(f"O arquivo '{file_path}' não foi encontrado.")
        except Exception as e:
            print(f"Ocorreu um erro ao carregar o arquivo '{file_path}': {e}")
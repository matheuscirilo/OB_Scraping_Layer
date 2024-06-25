import os
import pandas as pd
import json

class ImoveisDataProcessor:
    def __init__(self):
        pass
   
    def process_data(self, df) -> pd.DataFrame:
        df.fillna({
            'codigo': '',
            'titulo': '',
            'status': '',
            'localidade': '',
            'area_total': '0',
            'area_privativa': '0',
            'preco': '0',
            'bairro': '',
            'cidade': '',
            'estado': '',
        }, inplace=True)

        df['codigo'] = df['codigo'].str.replace(r'^Cód: ', '', regex=True)

        df['titulo'] = df['titulo'].str.split().str[0].str.lower()

        df['status'] = df['status'].str.replace(r'^- ', '', regex=True)

        df[['bairro', 'cidade', 'estado']] = df['localidade'].str.split(r'[-/]', expand=True)
        df.drop(columns= ['localidade'], inplace=True)

        df['area_total_m2'] = df['area_total'].str.split().str[0].str.replace('.', '').str.replace(',', '.').astype(float)
        df['area_privativa'] = df['area_privativa'].str.split().str[0].str.replace('.', '').str.replace(',', '.').astype(float)
        df['preco'] = df['preco'].str.replace(r'^R\$ ', '', regex=True).str.replace('.', '').str.replace(',', '.').astype(float)
        return df
    
    def load_data_from_jsonl(self)-> pd.DataFrame:
        try:
            data = []
            base_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(base_dir)
            file_path = os.path.join(parent_dir, 'data', 'imoveis_casa_feliz.jsonl')

            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    json_obj = json.loads(line)
                    data.append(json_obj)
            df = pd.DataFrame(data)
            return df
        except FileNotFoundError:
            print(f"O arquivo não foi encontrado.")
            return None
        except Exception as e:
            print(f"Ocorreu um erro ao carregar o arquivo: {e}")
            return None
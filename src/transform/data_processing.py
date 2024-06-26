import os
import googlemaps
import pandas as pd
import json
from dotenv import dotenv_values

# Para depuração, carregar e imprimir as variáveis do .env
env_vars = dotenv_values(".env")

class ImoveisDataProcessor:
    def __init__(self):
        self._key = env_vars.get("KEY")
        self._df = self.load_data_from_jsonl()

    def geocodingbairro(self, localidade):
        # Inicializa o cliente Google Maps com a chave de API fornecida
        gmaps = googlemaps.Client(key=self._key)

        try:
            # Geocodifica o endereço
            geocode_result = gmaps.geocode(localidade)
        
            # Verifica se a geocodificação retornou algum resultado
            if geocode_result:
                location = geocode_result[0]['geometry']['location']
                lat = location['lat']
                lng = location['lng']
                return lat, lng
            else:
                print(f"Endereço: {localidade} -> Não encontrado")
                return "", ""
        except Exception as e:
            print(f"Erro ao geocodificar {localidade}: {e}")
            return "", ""
        

    def process_data(self) -> pd.DataFrame:
        df = self._df
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

        # Adicionar colunas de latitude e longitude
        df['lat'] = None
        df['lng'] = None

        # Chame a função geocodingbairro para cada localidade
        for index, row in df.iterrows():
            lat, lng = self.geocodingbairro(row['localidade'])
            df.at[index, 'lat'] = lat
            df.at[index, 'lng'] = lng

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

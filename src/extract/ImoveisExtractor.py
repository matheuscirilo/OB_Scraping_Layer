import requests
from bs4 import BeautifulSoup
import json
import datetime
import os

class ImoveisExtractor:
    def __init__(self, url, headers=None):
        self.url = url
        self.headers = headers or {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"}
        self.data = []

    def proxima_pagina(self, soup):
        paginas = soup.find('ul', class_='pagination')
        if paginas:
            botoes = soup.find_all('a', class_='btn secondary-color-bt')
            for botao in botoes:
                if "PRÓXIMO" in botao.get_text(strip=True):
                    return botao['href']
        else:
            return None

    def encontra_elementos(self, elementos):
        dados_imoveis_pag = []
        if elementos:
            for elemento in elementos:
                cod = elemento.find('div', class_="destaque-imovel-imovel cod-imovel").get_text(strip=True) if elemento.find('div', class_="destaque-imovel-imovel cod-imovel") else None
                tipo = elemento.find('h3').get_text(strip=True) if elemento.find('h3') else None
                preco = elemento.find('span', class_='preco').get_text(strip=True) if elemento.find('span', class_='preco') else None    
                localidade = elemento.find('span', class_='bairro').get_text(strip=True) if elemento.find('span', class_='bairro') else None        
                qtde_quartos = elemento.find('li', {'title': 'Dormitório'}).get_text(strip=True) if elemento.find('li', {'title': 'Dormitório'}) else None
                qtde_banheiros = elemento.find('li', {'title': 'Banheiro'}).get_text(strip=True) if elemento.find('li', {'title': 'Banheiro'}) else None
                qtde_vagas = elemento.find('li', {'title': 'Vaga'}).get_text(strip=True) if elemento.find('li', {'title': 'Vaga'}) else None
                qtde_suite = elemento.find('li', {'title': 'Suíte'}).get_text(strip=True) if elemento.find('li', {'title': 'Suíte'}) else None
                area_total = elemento.find('li', {'title': 'Área total'}).get_text(strip=True) if elemento.find('li', {'title': 'Área total'}) else None
                area_privativa = elemento.find('li', {'title': 'Área Privativa'}).get_text(strip=True) if elemento.find('li', {'title': 'Área Privativa'}) else None
                data_extracao = datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S.%f")
                status = elemento.find('span', class_='status').get_text(strip=True) if elemento.find('span', class_='status') else None

                # Adicionando os dados extraídos à lista
                dados_imoveis_pag.append({
                    'codigo': cod,
                    'titulo': tipo,
                    'status': status,
                    'preco': preco,
                    'localidade': localidade,
                    'qtde_quartos': qtde_quartos,
                    'qtde_banheiros': qtde_banheiros,
                    'qtde_vagas': qtde_vagas,
                    'qtde_suite': qtde_suite,
                    'area_total': area_total,
                    'area_privativa': area_privativa,
                    'data_extracao': data_extracao
                })
            return dados_imoveis_pag
        else:
            print("Nenhum elemento encontrado com a classe 'pgl-property'.")
            return []

    def extract_data(self):
        dados_imoveis = []

        try:
            while True:
                # Fazendo a requisição para a página de produtos
                response = requests.get(self.url, headers=self.headers)                
                # Extraindo o conteúdo HTML da resposta
                html = response.text
                # Criando o objeto BeautifulSoup para análise do HTML
                soup = BeautifulSoup(html, 'html.parser')
                # Encontrando todos os elementos div com a classe especificada
                elementos = soup.find_all('div', class_="pgl-property")
                
                dados_pagina = self.encontra_elementos(elementos)
                
                dados_imoveis.extend(dados_pagina)

                self.url = self.proxima_pagina(soup)
                if self.url is None:
                    break 

            return dados_imoveis

        except requests.RequestException as e:
            print(f"Erro ao fazer a requisição para '{self.url}': {e}")
            return []

    def save_to_jsonl(self, data):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, '..', 'data', 'imoveis_casa_feliz.jsonl')
        diretorio = os.path.dirname(file_path)
        if not os.path.exists(diretorio):
            os.makedirs(diretorio)

        with open(file_path, 'w', encoding='utf-8') as jsonfile:
            for imovel in data:
                jsonfile.write(json.dumps(imovel, ensure_ascii=False) + '\n')
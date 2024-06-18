import requests
from bs4 import BeautifulSoup
import json
import datetime
import os

def proxima_pagina(soup) -> str:
    paginas = soup.find('ul', class_='pagination')
    if paginas:
        botoes = soup.find_all('a', class_='btn secondary-color-bt')
        for botao in botoes:
            if "PRÓXIMO" in botao.get_text(strip=True):
                return botao['href']
    else:
        return None
        
def encontra_elementos(elementos) -> list:
    dados_imoveis_pag = []

    # Verificando se encontramos elementos
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
                'suite': qtde_suite,
                'area_total': area_total,
                'area_privativa': area_privativa,
                'data_extracao': data_extracao
            })
        return dados_imoveis_pag
    else:
        print("Nenhum elemento encontrado com a classe 'pgl-property'.")
        return []

# URL da página de busca de imóveis
url = 'https://casafelizimoveis.com.br/busca/?pagina=1'

# Cabeçalhos para simular um navegador real
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"}

dados_imoveis = []

while True:

    # Fazendo a requisição para a página de produtos
    response = requests.get(url, headers=headers)

    # Verificando se a requisição foi bem-sucedida
    print(f'Status: {response.status_code} {url} - Extraindo HTML...')
    
    # Extraindo o conteúdo HTML da resposta
    html = response.text
    # Criando o objeto BeautifulSoup para análise do HTML
    soup = BeautifulSoup(html, 'html.parser')
    # Encontrando todos os elementos div com a classe especificada
    elementos = soup.find_all('div', class_="pgl-property")
    
    dados_pagina = encontra_elementos(elementos)
    dados_imoveis.extend(dados_pagina)

    url = proxima_pagina(soup)
    if url is None:
        print("Final do Scraping")
        break 

print(f'Total de imóveis extraídos: {len(dados_imoveis)}')

# Diretório para salvar o arquivo JSON
diretorio = os.path.join(os.getcwd(), "data")
if not os.path.exists(diretorio):
    os.makedirs(diretorio)

# Salvando os dados em um arquivo JSON
caminho_arquivo = os.path.join(diretorio, "imoveis_casa_feliz.json")
with open(caminho_arquivo, 'w', encoding='utf-8') as jsonfile:
    json.dump(dados_imoveis, jsonfile, ensure_ascii=False, indent=4)

print(f'Dados salvos em {caminho_arquivo}')







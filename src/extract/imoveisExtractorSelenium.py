from selenium import webdriver

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.options import Options

chrome_driver_path = 'C:\\chromedriver-win64\\chromedriver.exe'

# Configuração do Chrome
chrome_options = Options()
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
chrome_options.add_argument("--headless")  # Executar o Chrome em modo headless (opcional)
chrome_options.add_argument("--disable-gpu")  # Necessário para o modo headless no Windows
chrome_options.add_argument("--ignore-certificate-errors")  # Ignorar erros de certificado SSL
chrome_options.add_argument("--ignore-ssl-errors")  # Ignorar erros SSL
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

service = Service(chrome_driver_path)

options = webdriver.ChromeOptions()

driver = webdriver.Chrome(service=service, options=options)

url = 'https://www.mansurimobiliaria.com/venda/imoveis/todas-as-cidades/todos-os-bairros/0-quartos/0-suite-ou-mais/0-vaga/0-banheiro-ou-mais/todos-os-condominios?valorminimo=0&valormaximo=0&pagina=1'

url_teste = 'https://www.google.com'
driver.get(url_teste)
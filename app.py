from src.load.database_handler import DatabaseHandler
from src.transform.data_processing import ImoveisDataProcessor
from src.extract.ImoveisExtractor import ImoveisExtractor

if __name__ == "__main__":
    
    #EXTRACT

    # URL da página de busca de imóveis
    url = 'https://casafelizimoveis.com.br/busca/?pagina=1'

    # Instanciando o extrator de imóveis
    extractor = ImoveisExtractor(url)

    # Extraindo os dados
    dados_imoveis = extractor.extract_data()

    # Salvando os dados em um arquivo JSONL
    extractor.save_to_jsonl(dados_imoveis)

    print('EXTRACT TERMINADO')
    
    #TRANSFORM

    # Instanciar ImoveisDataProcessor
    processor = ImoveisDataProcessor()
    df = processor.load_data_from_jsonl()

    print('TRANSFORM TERMINADO')

    # LOAD


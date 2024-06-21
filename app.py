from src.load.database_connection import MySQLDatabase
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
    
    #TRANSFORM

    # Instanciar ImoveisDataProcessor
    processor = ImoveisDataProcessor()
    df = processor.load_data_from_jsonl()
    df_processado = processor.process_data(df)

    # LOAD
    
    db = MySQLDatabase()
    db.insert_data(df_processado)
    db.close_connection()
    




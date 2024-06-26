from src.load.database_connection import MySQLDatabase
from src.transform.data_processing import ImoveisDataProcessor
from src.extract.ImoveisExtractorbs4 import ImoveisExtractor

if __name__ == "__main__":
    
    #EXTRACT
    # Instanciando o extrator de imóveis
    extractor = ImoveisExtractor()
    extractor.extract_data()
    
    #TRANSFORM
    # Instanciar ImoveisDataProcessor
    processor = ImoveisDataProcessor()
    df_processado = processor.process_data()

    # LOAD
    db = MySQLDatabase()
    db.insert_data(df_processado)

    
    




import mysql.connector as mysql_connector
from dotenv import dotenv_values
import pandas as pd

# Para depuração, carregar e imprimir as variáveis do .env
env_vars = dotenv_values(".env")

class MySQLDatabase:

    def __init__(self) -> None:
        self._host = env_vars.get("HOST")
        self._username = env_vars.get("USERNAME")
        self._passwd = env_vars.get("PASSWD")
        self._database = env_vars.get("DATABASE")
        self.conn = self._connecting()

    def _connecting(self):
        try:
            connection = mysql_connector.connect(
                host=self._host,
                password=self._passwd,
                user=self._username,
                database=self._database
            )
            print("Connection successful")
            return connection
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def close_connection(self):
        """Fecha a conexão com o banco de dados."""
        if self.conn is not None and self.conn.is_connected():
            self.conn.close()

    def insert_data(self, data: pd.DataFrame):
        if data is None or data.empty:
            print("DataFrame is empty or None")
            return
        
        required_columns = [
            "codigo", "titulo", "status", "preco", "bairro",
            "cidade", "estado", "qtde_quartos", "qtde_banheiros",
            "qtde_vagas", "qtde_suite", "area_total_m2", "area_privativa", "data_extracao"
        ]

        if not all(col in data.columns for col in required_columns):
            print(data.columns)
            print("DataFrame is missing some required columns")
            return
        
        # Tratar valores NaN antes de inserir no banco de dados
        data = data.where(pd.notnull(data), None)
        
        """Insere dados na tabela casa_feliz_imobiliaria."""
        
        query = """
        INSERT INTO casa_feliz_imobiliaria (
            codigo, titulo, status, preco, bairro, cidade, estado,
            qtde_quartos, qtde_banheiros, qtde_vagas, qtde_suite,
            area_total_m2, area_privativa, data_extracao
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
            cursor = self.conn.cursor()
            for _, row in data.iterrows():
                values = [None if pd.isna(value) else value for value in row[required_columns]]
                cursor.execute(query, tuple(values))
            self.conn.commit()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
    
    def fetch_data(self, query):
        if self.conn is not None and self.conn.is_connected():
            try:
                return pd.read_sql(query, self.conn)
            except mysql_connector.Error as e:
                print(f"Error: {e}")
                return None
        else:
            print("No active connection")
            return None
    

        
    

    

    
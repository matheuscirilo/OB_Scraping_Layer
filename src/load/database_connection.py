from dotenv import dotenv_values
import pandas as pd
from sqlalchemy import create_engine, Table, MetaData

# Para depuração, carregar e imprimir as variáveis do .env
env_vars = dotenv_values(".env")

class MySQLDatabase:

    def __init__(self) -> None:
        self._host = env_vars.get("HOST")
        self._username = env_vars.get("USERNAME")
        self._passwd = env_vars.get("PASSWD")
        self._database = env_vars.get("DATABASE")
        self._engine = self._open_connection()
        self.metadata = MetaData()

    def _open_connection(self):
        try:          
            db_url = f'mysql+pymysql://{self._username}:{self._passwd}@{self._host}/{self._database}' 
            engine = create_engine(db_url)
            return engine
        except Exception as e:
            print(f"Error: {e}")
            return None

    def insert_data(self, df: pd.DataFrame) -> None:
        if df is None or df.empty:
            print("DataFrame is empty or None")
        
        required_columns = [
            "codigo", "titulo", "status", "preco", "bairro",
            "cidade", "estado", "qtde_quartos", "qtde_banheiros",
            "qtde_vagas", "qtde_suite", "area_total_m2", "area_privativa", "data_extracao", "lat", "lng"
        ]

        if not all(col in df.columns for col in required_columns):
            print(df.columns)
            print("DataFrame is missing some required columns")

        table = Table('casa_feliz_imobiliaria', self.metadata, autoload_with=self._engine)

        try:
            with self._engine.connect() as connection:
                trans = connection.begin()
                connection.execute(table.insert(), df.to_dict(orient='records'))
                trans.commit()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self._engine.dispose()
        
    def fetch_data(self, query: str) -> pd.DataFrame:
        try:
            with self._engine.connect() as connection:
                return pd.read_sql(query, connection)
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            self._engine.dispose()

    

        
    

    

    
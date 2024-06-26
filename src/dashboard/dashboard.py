import sys
import os

# Adicione o diretório pai do diretório 'src' ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
from load.database_connection import MySQLDatabase

def calcular_preco_medio_por_bairro(df):
    # Filtrar dados onde o preço é maior que zero
    df_non_zero_prices = df[df['preco'] > 0]

    # Transformar todos os nomes de bairro para minúsculas
    df_non_zero_prices['bairro'] = df_non_zero_prices['bairro'].str.lower()

    # Calcular preço médio por bairro e ordenar de forma descendente
    average_price_by_bairro = df_non_zero_prices.groupby('bairro')['preco'].mean().sort_values(ascending=False)

    return average_price_by_bairro

def ajustaZoon(df: pd.DataFrame):

    if len(df) <=1:
        return 15   
    else:
        return 13

# Função principal do Streamlit
def main():
    st.title("Dashboard de Imóveis")

    # Instanciar a classe de banco de dados e conectar
    db = MySQLDatabase()

    # Buscar dados do banco de dados
    query = "SELECT * FROM casa_feliz_imobiliaria"
    df = db.fetch_data(query)

    if df is not None:
        
        df['data_extracao'] = pd.to_datetime(df['data_extracao'], format='%Y%m%d')
 
        # ordenar pela coluna Data em ordem crescente
        df.sort_values('data_extracao', ascending=True, inplace=True)
        
        col1, col2 = st.columns(2)
        col1.metric(label="Número Total de casas", value=len(df['codigo'].unique()))
        col2.metric(label="última atualização", value=str(df['data_extracao'][0]))

     
        # Qual o preço médio por marca
        st.subheader('Preço médio por bairro')
        col1, col2 = st.columns(2) # Primeira linha com duas colunas      
        status_filtro = col1.radio("Filtrar por status:", df['status'].unique())
        titulo_filtro = col2.radio("filtrar por tipo:", df['titulo'].unique(), horizontal=True)
        df_filtrado = df[(df['status'] == status_filtro) & (df['titulo'] == titulo_filtro)]
        average_price_by_bairro = calcular_preco_medio_por_bairro(df_filtrado)
        st.line_chart(average_price_by_bairro)

        st.map(df_filtrado, latitude='lat', longitude='lng', zoom=ajustaZoon(df_filtrado))         

    else:
        st.error("Falha ao buscar os dados do banco de dados")

if __name__ == "__main__":
    main()
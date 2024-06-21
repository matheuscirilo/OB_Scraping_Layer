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

# Função principal do Streamlit
def main():
    st.title("Dashboard de Imóveis")

    # Instanciar a classe de banco de dados e conectar
    db = MySQLDatabase()

    # Buscar dados do banco de dados
    if db.conn:
        query = "SELECT * FROM casa_feliz_imobiliaria"
        df = db.fetch_data(query)
        db.close_connection()

        if df is not None:
            # Qual o preço médio por marca
            st.subheader('Preço médio por bairro')
            status_filtro = st.radio("Filtrar por status:", df['status'].unique())
            titulo_filtro = st.radio("filtrar por tipo:", df['titulo'].unique(), horizontal=True)
            df_filtrado = df[(df['status'] == status_filtro) & (df['titulo'] == titulo_filtro)]
            average_price_by_bairro = calcular_preco_medio_por_bairro(df_filtrado)
            col1, col2 = st.columns([4, 2])
            col1.bar_chart(average_price_by_bairro)
            col2.write(average_price_by_bairro)
            
            
            st.map()



        else:
            st.error("Falha ao buscar os dados do banco de dados")
    else:
        st.error(f"Falha ao conectar ao banco de dados")

if __name__ == "__main__":
    main()
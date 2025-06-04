#-------------------------------------------------------------------------------
# Name:        módulo1
# Purpose:
#
# Author:      srsouza
#
# Created:     03/06/2025
# Copyright:   (c) srsouza 2025
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import streamlit as st
import pandas as pd
import numpy as np

st.title("Exemplo de App com Streamlit")

# Carregar dados
df = pd.DataFrame({
    'Coluna 1': [1, 2, 3, 4],
    'Coluna 2': [10, 20, 30, 40]
})

# Exibir tabela
st.write("Tabela de dados:")
st.write(df)

# Adicionar slider
valor = st.slider("Selecione um valor", 0, 100, 50)
st.write("O valor selecionado é:", valor)

# Adicionar checkbox
if st.checkbox("Mostrar tabela"):
    st.write(df)

# Adicionar gráfico interativo
data = pd.DataFrame(
    np.random.randn(50, 3),
    columns=['a', 'b', 'c']
)
st.line_chart(data)
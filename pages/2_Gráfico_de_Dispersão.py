
import pandas as pd
import streamlit as st
import numpy as np

st.write("# Proficiência em Língua Portuguesa vs Matemática")
st.markdown(
    """
    A figura apresenta um gráfico de dispersão com as proficiências de Língua Portuguesa e Matemática para os valores de INSE.
    
    Selecione um valor para o INSE:
    """
)

# Importar os dados
df_es_filtrado = pd.read_csv('data/raw_data/df_es_filtrado.csv', sep=",")

data = {
    'PROFICIENCIA_LP': df_es_filtrado['PROFICIENCIA_LP_SAEB'],
    'PROFICIENCIA_MT': df_es_filtrado['PROFICIENCIA_MT_SAEB'],
    'INSE': df_es_filtrado['NU_TIPO_NIVEL_INSE']
}
df = pd.DataFrame(data)

df = df.sort_values('INSE')
nivel = st.radio(
    label="INSE",
    options=np.arange(1,9),
    horizontal=True
)
st.scatter_chart(
    data=df[df['INSE']==nivel],
    x='PROFICIENCIA_LP',
    y='PROFICIENCIA_MT',
    x_label='Proficiência em Língua Portuguesa',
    y_label='Proficiência em Matemática',
    #size='INSE',
    width=500,
    height=500,
    use_container_width=False,
    color='INSE'
)
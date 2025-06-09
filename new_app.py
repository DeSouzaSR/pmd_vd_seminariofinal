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

st.title("Desempenho SAEB 2023: Uma Análise Visual por Nível Socioeconômico no Ensino Médio Capixaba")
st.subheader("Trabalho para a disciplina de Visualização de Dados da Pós-graduação em Mineração de Dados do IFES - Serra - ES")
st.write("Professor Dr. Richard Junior Manuel Godinez Tello")
st.write("Autores: Cristiani Oliveira, Katia Franco, Sandro De Souza, Ueliton Oliveira")
st.write("Fonte dos dados: https://www.gov.br/inep/pt-br/areas-de-atuacao/avaliacao-e-exames-educacionais/saeb/resultados")

st.divider()

################################################################
#### Estatísticas Gerais #######################################
################################################################

st.header("Estatísticas gerais para Língua Portuguesa e Matemática", divider=True)

st.write("Máximos e mínimos para Língua Portuguesa e Matemática por tipo de nível socioeconômico")

# Importar os dados
df_es_filtrado = pd.read_csv('data/raw_data/df_es_filtrado.csv', sep=",")



# Group data by socioeconomic level and get the min and max proficiency scores
socioeconomic_stats = df_es_filtrado.groupby('NU_TIPO_NIVEL_INSE').agg(
    min_lp=('PROFICIENCIA_LP_SAEB', 'min'),
    max_lp=('PROFICIENCIA_LP_SAEB', 'max'),
    min_mt=('PROFICIENCIA_MT_SAEB', 'min'),
    max_mt=('PROFICIENCIA_MT_SAEB', 'max')
)

socioeconomic_stats = socioeconomic_stats.sort_index()
st.write(socioeconomic_stats)

st.write("Média, mediana e moda de todos os valores que estão dentro dos atributos PROFICIENCIA_LP_SAEB e PROFICIENCIA_MT_SAEB separados por nível sócioeconômico do atributo NU_TIPO_NIVEL_INSE do dataframedf_es. Quero só 2 dígitos depois do ponto para todos os valores.")

socioeconomic_stats = df_es_filtrado.groupby('NU_TIPO_NIVEL_INSE').agg(
    mean_lp=('PROFICIENCIA_LP_SAEB', 'mean'),
    median_lp=('PROFICIENCIA_LP_SAEB', 'median'),
    mode_lp=('PROFICIENCIA_LP_SAEB', lambda x: x.mode()[0] if not x.mode().empty else None),
    mean_mt=('PROFICIENCIA_MT_SAEB', 'mean'),
    median_mt=('PROFICIENCIA_MT_SAEB', 'median'),
    mode_mt=('PROFICIENCIA_MT_SAEB', lambda x: x.mode()[0] if not x.mode().empty else None)
)

socioeconomic_stats = socioeconomic_stats.round(2)
st.write(socioeconomic_stats)

################################################################
#### Gráfico de dispersão  ################################################
################################################################

# Criando um DataFrame de exemplo
data = {
    'PROFICIENCIA_LP': df_es_filtrado['PROFICIENCIA_LP_SAEB'],
    'PROFICIENCIA_MT': df_es_filtrado['PROFICIENCIA_MT_SAEB'],
    'INSE': df_es_filtrado['NU_TIPO_NIVEL_INSE']
}
df = pd.DataFrame(data)

# Mapeando os níveis do INSE para uma ordem numérica para plotagem
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


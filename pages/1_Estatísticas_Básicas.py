import streamlit as st
import pandas as pd

st.set_page_config(page_title="Estatísticas básicas", page_icon="📈")

st.markdown("# Estatísticas básicas")
st.sidebar.header("Estatísticas básicas")

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
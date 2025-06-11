import pandas as pd
import streamlit as st
import seaborn as sns

st.write("# Proficiência em Língua Portuguesa vs Matemática")
st.markdown(
    """
    A figura apresenta um gráfico BoxPlot com as notas somadas de proficiências de Língua Portuguesa e Matemática
    para os valores de INSE. Observa-se aumento da mediana para índices INSE maiores. 
    """
)

# Leitura dos dados
df_es = pd.read_csv('data/raw_data/df_es_filtrado.csv', sep=",")

# Cálculo da proficiência total
df_es['PROFICIENCIA_TOTAL'] = df_es['PROFICIENCIA_LP_SAEB'] + df_es['PROFICIENCIA_MT_SAEB']

# Box plots de proficiência por nível sócieconômico
fig = sns.boxplot(data=df_es, x='NU_TIPO_NIVEL_INSE', y='PROFICIENCIA_TOTAL').get_figure()
st.pyplot(fig)


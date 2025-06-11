import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt # Importa a biblioteca matplotlib

st.write("# Proficiência em Língua Portuguesa vs Matemática")
st.markdown(
    """
    A figura apresenta um gráfico BoxPlot com as notas somadas de proficiências de Língua Portuguesa e Matemática
    para os valores de INSE. Observa-se aumento da mediana para índices INSE maiores.
    """
)

# Leitura dos dados
# Certifique-se de que o caminho 'data/raw_data/df_es_filtrado.csv' está correto
# no ambiente onde o Streamlit está sendo executado (e.g., GitHub repo).
try:
    df_es = pd.read_csv('data/raw_data/df_es_filtrado.csv', sep=",")
except FileNotFoundError:
    st.error("Erro: O arquivo 'df_es_filtrado.csv' não foi encontrado. Verifique o caminho.")
    st.stop() # Para a execução do aplicativo Streamlit

# Cálculo da proficiência total
df_es['PROFICIENCIA_TOTAL'] = df_es['PROFICIENCIA_LP_SAEB'] + df_es['PROFICIENCIA_MT_SAEB']

# Garantindo a ordem correta dos níveis do INSE
# Se 'NU_TIPO_NIVEL_INSE' for categórico como 'Nível I', 'Nível II', etc.
# Ordene-o para que o box plot seja exibido na sequência correta.
# Supondo que 'NU_TIPO_NIVEL_INSE' seja uma coluna de texto como 'Nível I', 'Nível II', etc.
# Mapeie para uma ordem numérica para garantir o sort correto, ou use pd.Categorical.
inse_order = {
    'Nível I': 1, 'Nível II': 2, 'Nível III': 3, 'Nível IV': 4,
    'Nível V': 5, 'Nível VI': 6, 'Nível VII': 7, 'Nível VIII': 8
}
# Criar uma coluna numérica para ordenar ou garantir que a coluna seja do tipo Category
df_es['NU_TIPO_NIVEL_INSE_ORDEM'] = df_es['NU_TIPO_NIVEL_INSE'].map(inse_order)
# Remover linhas com valores de INSE que não estejam no mapeamento, se existirem
df_es.dropna(subset=['NU_TIPO_NIVEL_INSE_ORDEM'], inplace=True)

# Obter a ordem única dos níveis INSE para os rótulos do eixo x
sorted_inse_levels = sorted(df_es['NU_TIPO_NIVEL_INSE'].unique(), key=lambda x: inse_order.get(x, 99))

# Preparar os dados para o box plot do matplotlib
# Criar uma lista de arrays, onde cada array contém os dados para um box plot
data_for_boxplot = [df_es[df_es['NU_TIPO_NIVEL_INSE'] == level]['PROFICIENCIA_TOTAL'] for level in sorted_inse_levels]

# Criar a figura e o eixo para o plot
fig, ax = plt.subplots(figsize=(10, 6))

# Gerar o box plot
ax.boxplot(data_for_boxplot, labels=sorted_inse_levels, patch_artist=True, medianprops={'color': 'red'})

# Adicionar títulos e rótulos
ax.set_title('Distribuição da Proficiência Total por Nível Socioeconômico (INSE)')
ax.set_xlabel('Nível Socioeconômico (INSE)')
ax.set_ylabel('Proficiência Total (Língua Portuguesa + Matemática)')
ax.grid(axis='y', linestyle='--', alpha=0.7)

# Exibir o plot no Streamlit
st.pyplot(fig)

st.write("---")
st.write("Este gráfico mostra a distribuição das notas de proficiência total (LP + Matemática) para cada nível do Indicador de Nível Socioeconômico (INSE).")
st.write("A linha vermelha dentro de cada caixa representa a mediana, a caixa delimita o primeiro e o terceiro quartil (25% e 75% dos dados), e as 'barras' ou 'bigodes' estendem-se aos valores mínimo e máximo dentro de 1.5 vezes o intervalo interquartil.")
st.write("Pontos fora dos bigodes são considerados outliers.")


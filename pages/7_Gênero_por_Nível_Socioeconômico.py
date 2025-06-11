import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# --- Títulos e descrições para o Streamlit ---
st.write("# Distribuição de Gênero por Nível Socioeconômico")
st.markdown(
    """
    A figura apresenta um gráfico de barras agrupadas mostrando a contagem de estudantes
    masculinos e femininos em cada Nível Socioeconômico (INSE).
    """
)

# --- Leitura e Pré-processamento dos Dados ---
file_path = 'data/raw_data/df_es_filtrado.csv'
try:
    df_es = pd.read_csv(file_path, sep=",")
except FileNotFoundError:
    st.error(f"Erro: O arquivo '{file_path}' não foi encontrado. Verifique o caminho.")
    st.stop()
except Exception as e:
    st.error(f"Ocorreu um erro ao carregar o arquivo CSV: {e}")
    st.stop()

# Verificar se as colunas essenciais existem
required_cols = ['NU_TIPO_NIVEL_INSE', 'TX_RESP_Q01']
missing_columns = [col for col in required_cols if col not in df_es.columns]

if missing_columns:
    st.error(f"Erro: As seguintes colunas necessárias não foram encontradas no arquivo CSV: {', '.join(missing_columns)}. Verifique o dicionário de dados e o arquivo.")
    st.stop()

# Forçar a coluna INSE a ser numérica e remover NaNs
df_es['NU_TIPO_NIVEL_INSE'] = pd.to_numeric(df_es['NU_TIPO_NIVEL_INSE'], errors='coerce')
df_es.dropna(subset=['NU_TIPO_NIVEL_INSE', 'TX_RESP_Q01'], inplace=True)

if df_es.empty:
    st.warning("Após o pré-processamento, não há dados válidos para plotar a distribuição de gênero.")
    st.stop()

# Mapeamento para exibir os níveis do INSE como strings
inse_display_labels = {
    1: 'Nível I', 2: 'Nível II', 3: 'Nível III', 4: 'Nível IV',
    5: 'Nível V', 6: 'Nível VI', 7: 'Nível VII', 8: 'Nível VIII'
}

# Mapear os valores de gênero diretamente (se já estiverem como 'Masculino'/'Feminino')
# Se houver outros valores como '.', 'C', '*', eles se tornarão NaN e serão removidos.
gender_mapping = {
    'Masculino': 'Masculino',
    'Feminino': 'Feminino'
}
df_es['TX_RESP_Q01_LABEL'] = df_es['TX_RESP_Q01'].map(gender_mapping)

# Remover NaNs que podem surgir do mapeamento de gênero, se houver outros valores
df_es.dropna(subset=['TX_RESP_Q01_LABEL'], inplace=True)


# Contar a distribuição de gênero por nível socioeconômico
gender_socioeconomic_counts = df_es.groupby(['NU_TIPO_NIVEL_INSE', 'TX_RESP_Q01_LABEL']).size().unstack(fill_value=0)

# Reindexar para garantir que todos os níveis INSE (1 a 8) estejam presentes e ordenados
all_inse_levels = sorted(df_es['NU_TIPO_NIVEL_INSE'].unique())
gender_socioeconomic_counts = gender_socioeconomic_counts.reindex(all_inse_levels, fill_value=0)

# Garantir a ordem das colunas de gênero, caso existam no DataFrame
gender_cols = ['Masculino', 'Feminino']
present_gender_cols = [col for col in gender_cols if col in gender_socioeconomic_counts.columns]

if not present_gender_cols:
    st.warning("Não há dados de gênero válidos ('Masculino' ou 'Feminino') para plotar. Verifique a coluna 'TX_RESP_Q01'.")
    st.stop()

gender_socioeconomic_counts = gender_socioeconomic_counts[present_gender_cols]

# Converter as colunas para tipo numérico (int) para plotagem
for col in present_gender_cols:
    gender_socioeconomic_counts[col] = gender_socioeconomic_counts[col].astype(int)


# --- Criação do Gráfico de Barras Agrupadas com Matplotlib ---
fig, ax = plt.subplots(figsize=(12, 7)) # Cria a figura e os eixos

# Plota o gráfico de barras agrupadas diretamente do DataFrame processado
gender_socioeconomic_counts.plot(
    kind='bar',
    ax=ax,
    width=0.8, # Largura das barras
    edgecolor='black'
)

# Definir os rótulos do eixo X usando o mapeamento INSE
tick_positions = np.arange(len(gender_socioeconomic_counts.index))
tick_labels = [inse_display_labels.get(level, str(level)) for level in gender_socioeconomic_counts.index]
ax.set_xticks(tick_positions)
ax.set_xticklabels(tick_labels, rotation=45, ha='right') # Rotação para melhor leitura

# Adicionar títulos e rótulos
ax.set_title('Distribuição de Gênero por Nível Socioeconômico')
ax.set_xlabel('Nível Socioeconômico (INSE)')
ax.set_ylabel('Número de Alunos')
ax.legend(title='Gênero')
ax.grid(axis='y', linestyle='--', alpha=0.7) # Adiciona grade no eixo Y

plt.tight_layout() # Ajusta o layout para evitar sobreposição

# --- Exibir o gráfico no Streamlit ---
st.pyplot(fig)

# --- Informações Adicionais para o Streamlit ---
st.write("---")
st.write("Este gráfico de barras agrupadas ilustra a quantidade de estudantes por gênero (Masculino e Feminino) dentro de cada Nível Socioeconômico (INSE).")
st.write("As barras agrupadas permitem comparar diretamente o número de meninos e meninas em cada nível de INSE, revelando possíveis disparidades na composição de gênero entre os diferentes estratos socioeconômicos.")

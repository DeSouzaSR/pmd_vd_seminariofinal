import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt  # Importa a biblioteca matplotlib

# --- Títulos e descrições para o Streamlit ---
st.write("# Proficiência em Língua Portuguesa vs Matemática")
st.markdown(
    """
    A figura apresenta um gráfico de dispersão com as proficiências de Língua Portuguesa e Matemática para os valores de INSE.

    Por favor, selecione um valor para o Nível Socioeconômico (INSE) no menu lateral à esquerda.
    """
)

# --- Leitura e Pré-processamento dos Dados ---
# Importar os dados
file_path = 'data/raw_data/df_es_filtrado.csv'
try:
    df_es_filtrado = pd.read_csv(file_path, sep=",")
except FileNotFoundError:
    st.error(f"Erro: O arquivo '{file_path}' não foi encontrado. Verifique o caminho.")
    st.stop()
except Exception as e:
    st.error(f"Ocorreu um erro ao carregar o arquivo CSV: {e}")
    st.stop()

# Verificar se as colunas essenciais existem
required_cols = ['PROFICIENCIA_LP_SAEB', 'PROFICIENCIA_MT_SAEB', 'NU_TIPO_NIVEL_INSE']
missing_columns = [col for col in required_cols if col not in df_es_filtrado.columns]

if missing_columns:
    st.error(
        f"Erro: As seguintes colunas necessárias não foram encontradas no arquivo CSV: {', '.join(missing_columns)}. Verifique o dicionário de dados e o arquivo.")
    st.stop()

# Garantir que as colunas de proficiência são numéricas e remover NaNs
df_es_filtrado['PROFICIENCIA_LP_SAEB'] = pd.to_numeric(df_es_filtrado['PROFICIENCIA_LP_SAEB'], errors='coerce')
df_es_filtrado['PROFICIENCIA_MT_SAEB'] = pd.to_numeric(df_es_filtrado['PROFICIENCIA_MT_SAEB'], errors='coerce')
df_es_filtrado['NU_TIPO_NIVEL_INSE'] = pd.to_numeric(df_es_filtrado['NU_TIPO_NIVEL_INSE'],
                                                     errors='coerce')  # Garantir que INSE também é numérico

df_es_filtrado.dropna(subset=['PROFICIENCIA_LP_SAEB', 'PROFICIENCIA_MT_SAEB', 'NU_TIPO_NIVEL_INSE'], inplace=True)

# Mapear os níveis INSE numéricos para rótulos de exibição
inse_display_labels = {
    1: 'Nível I', 2: 'Nível II', 3: 'Nível III', 4: 'Nível IV',
    5: 'Nível V', 6: 'Nível VI', 7: 'Nível VII', 8: 'Nível VIII'
}

# Filtrar para incluir apenas os INSEs que estão no nosso dicionário de labels
df_es_filtrado = df_es_filtrado[df_es_filtrado['NU_TIPO_NIVEL_INSE'].isin(inse_display_labels.keys())]

if df_es_filtrado.empty:
    st.warning("Após o pré-processamento, não há dados válidos para plotar. Verifique os dados de INSE e proficiência.")
    st.stop()

# --- Seleção do Nível INSE na barra lateral ---
st.sidebar.header("Opções de Visualização")
selected_inse_level = st.sidebar.radio(
    label="Selecione o Nível Socioeconômico (INSE):",
    options=sorted(df_es_filtrado['NU_TIPO_NIVEL_INSE'].unique()),  # Usa os níveis INSE presentes nos dados
    format_func=lambda x: inse_display_labels.get(x, f'INSE {x}'),  # Formata os rótulos
    horizontal=False  # Pode ser True se preferir na horizontal
)

# Preparar o DataFrame para o gráfico de dispersão com base na seleção
df_filtered_by_inse = df_es_filtrado[df_es_filtrado['NU_TIPO_NIVEL_INSE'] == selected_inse_level]

if df_filtered_by_inse.empty:
    st.warning(
        f"Não há dados disponíveis para o Nível Socioeconômico {inse_display_labels.get(selected_inse_level, str(selected_inse_level))}. Por favor, selecione outro nível.")
    st.stop()

# --- Criação do Gráfico de Dispersão com Matplotlib ---
fig, ax = plt.subplots(figsize=(10, 8))  # Cria a figura e os eixos

# Plota os pontos de dispersão
ax.scatter(x=df_filtered_by_inse['PROFICIENCIA_LP_SAEB'],
           y=df_filtered_by_inse['PROFICIENCIA_MT_SAEB'],
           alpha=0.6,
           s=50,  # Tamanho dos pontos
           c='skyblue')  # Cor dos pontos

# --- Ajustar os limites dos eixos dinamicamente ---
# Encontrar o mínimo e máximo geral das proficiências no DataFrame filtrado
min_prof = min(df_filtered_by_inse['PROFICIENCIA_LP_SAEB'].min(), df_filtered_by_inse['PROFICIENCIA_MT_SAEB'].min())
max_prof = max(df_filtered_by_inse['PROFICIENCIA_LP_SAEB'].max(), df_filtered_by_inse['PROFICIENCIA_MT_SAEB'].max())

# Definir os limites dos eixos com uma margem
# Ajuste 'padding' conforme a necessidade de visualização
padding = 20
ax.set_xlim(min_prof - padding, max_prof + padding)
ax.set_ylim(min_prof - padding, max_prof + padding)

# Adicionar títulos e rótulos
ax.set_title(
    f"Proficiência em LP vs. Matemática para {inse_display_labels.get(selected_inse_level, f'INSE {selected_inse_level}')}")
ax.set_xlabel('Proficiência em Língua Portuguesa')
ax.set_ylabel('Proficiência em Matemática')
ax.grid(True, linestyle='--', alpha=0.7)  # Adiciona grade

# Manter proporção de aspecto igual para eixos de proficiência
ax.set_aspect('equal', adjustable='box')

# --- Exibir o gráfico no Streamlit ---
st.pyplot(fig)

st.write("---")
st.write(
    f"Este gráfico de dispersão mostra a relação entre a proficiência em Língua Portuguesa e Matemática para os estudantes do **{inse_display_labels.get(selected_inse_level, f'INSE {selected_inse_level}')}**.")
st.write(
    "Cada ponto representa um estudante, e sua posição nos eixos indica suas respectivas proficiências nas duas áreas. Os eixos foram ajustados para focar na área de dados relevante, melhorando a visualização das tendências.")

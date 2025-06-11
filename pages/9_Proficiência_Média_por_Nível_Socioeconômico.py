import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# --- Títulos e descrições para o Streamlit ---
st.write("# Proficiência Média por Gênero e Nível Socioeconômico")
st.markdown(
    """
    A figura apresenta um gráfico de barras agrupadas que compara a proficiência média
    em Língua Portuguesa ou Matemática entre estudantes masculinos e femininos, para cada Nível Socioeconômico (INSE).
    Use o menu lateral à esquerda para selecionar a proficiência desejada.
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
required_cols = ['NU_TIPO_NIVEL_INSE', 'TX_RESP_Q01', 'PROFICIENCIA_LP_SAEB', 'PROFICIENCIA_MT_SAEB']
missing_columns = [col for col in required_cols if col not in df_es.columns]

if missing_columns:
    st.error(f"Erro: As seguintes colunas necessárias não foram encontradas no arquivo CSV: {', '.join(missing_columns)}. Verifique o dicionário de dados e o arquivo.")
    st.stop()

# Forçar colunas a serem numéricas e remover NaNs
df_es['NU_TIPO_NIVEL_INSE'] = pd.to_numeric(df_es['NU_TIPO_NIVEL_INSE'], errors='coerce')
df_es['PROFICIENCIA_LP_SAEB'] = pd.to_numeric(df_es['PROFICIENCIA_LP_SAEB'], errors='coerce')
df_es['PROFICIENCIA_MT_SAEB'] = pd.to_numeric(df_es['PROFICIENCIA_MT_SAEB'], errors='coerce')

# Mapear os valores de gênero (A e B) para 'Masculino' e 'Feminino'
gender_mapping = {
    'Masculino': 'Masculino', # Assumindo que já vêm como strings
    'Feminino': 'Feminino'
}
df_es['TX_RESP_Q01_LABEL'] = df_es['TX_RESP_Q01'].map(gender_mapping)

# Remover linhas com valores nulos nas colunas essenciais para o plot
df_es.dropna(subset=['NU_TIPO_NIVEL_INSE', 'TX_RESP_Q01_LABEL', 'PROFICIENCIA_LP_SAEB', 'PROFICIENCIA_MT_SAEB'], inplace=True)

if df_es.empty:
    st.warning("Após o pré-processamento, não há dados válidos para plotar a proficiência média por gênero. Verifique as colunas de INSE, Gênero e Proficiências.")
    st.stop()

# Mapeamento para exibir os níveis do INSE como strings (para rótulos)
inse_display_labels = {
    1: 'Nível I', 2: 'Nível II', 3: 'Nível III', 4: 'Nível IV',
    5: 'Nível V', 6: 'Nível VI', 7: 'Nível VII', 8: 'Nível VIII'
}

# --- Seleção de Proficiência na barra lateral ---
st.sidebar.header("Opções de Proficiência")
selected_proficiency = st.sidebar.radio(
    label="Selecione a Proficiência:",
    options=['Língua Portuguesa', 'Matemática'],
    index=0 # Padrão para Língua Portuguesa
)

# Definir a coluna de proficiência e o rótulo do eixo Y com base na seleção
if selected_proficiency == 'Língua Portuguesa':
    proficiency_col = 'PROFICIENCIA_LP_SAEB'
    y_axis_label = 'Média de Proficiência em Língua Portuguesa'
else:
    proficiency_col = 'PROFICIENCIA_MT_SAEB'
    y_axis_label = 'Média de Proficiência em Matemática'

# --- Cálculo da Proficiência Média por Nível Socioeconômico e Gênero ---
# Agrupar por nível socioeconômico e gênero e calcular a média da proficiência selecionada
mean_proficiency_by_socioeconomic_gender = df_es.groupby(['NU_TIPO_NIVEL_INSE', 'TX_RESP_Q01_LABEL']).agg(
    mean_proficiency=(proficiency_col, 'mean')
).unstack(fill_value=0) # Transforma os gêneros em colunas, preenchendo NaNs com 0

# A coluna 'mean_proficiency' é um MultiIndex, então acessamos o nível 0
mean_proficiency_by_socioeconomic_gender.columns = mean_proficiency_by_socioeconomic_gender.columns.get_level_values(1)

# Reindexar para garantir que todos os níveis INSE e gêneros (Masculino/Feminino)
# estejam presentes e na ordem correta, mesmo que não haja dados para algum.
all_inse_levels = sorted(df_es['NU_TIPO_NIVEL_INSE'].unique())
mean_proficiency_by_socioeconomic_gender = mean_proficiency_by_socioeconomic_gender.reindex(all_inse_levels, fill_value=0)

# Garantir a ordem das colunas de gênero
gender_cols_ordered = ['Masculino', 'Feminino']
# Filtrar apenas as colunas de gênero que existem no DataFrame resultante
present_gender_cols = [col for col in gender_cols_ordered if col in mean_proficiency_by_socioeconomic_gender.columns]
mean_proficiency_by_socioeconomic_gender = mean_proficiency_by_socioeconomic_gender[present_gender_cols]

# Verificar se há dados para plotar após o processamento
if mean_proficiency_by_socioeconomic_gender.empty or mean_proficiency_by_socioeconomic_gender.sum().sum() == 0:
    st.warning(f"Não há dados de proficiência média para {selected_proficiency.lower()} após o processamento. Por favor, verifique seus dados ou seleções.")
    st.stop()

# --- Criação do Gráfico de Barras Agrupadas com Matplotlib ---
fig, ax = plt.subplots(figsize=(12, 7)) # Cria a figura e os eixos

# Plota o gráfico de barras agrupadas diretamente do DataFrame processado
mean_proficiency_by_socioeconomic_gender.plot(
    kind='bar',
    ax=ax,
    width=0.8, # Largura total do grupo de barras
    edgecolor='black',
    color=['#1f77b4', '#ff7f0e'] # Azul para Masculino, Laranja para Feminino
)

# Definir os rótulos do eixo X usando o mapeamento INSE
tick_positions = np.arange(len(mean_proficiency_by_socioeconomic_gender.index))
tick_labels = [inse_display_labels.get(level, str(level)) for level in mean_proficiency_by_socioeconomic_gender.index]
ax.set_xticks(tick_positions)
ax.set_xticklabels(tick_labels, rotation=45, ha='right') # Rotação para melhor leitura

# --- Ajuste do limite inferior do eixo Y ---
ax.set_ylim(bottom=250) # Define o limite inferior do eixo Y em 200

# Adicionar títulos e rótulos
ax.set_title(f'Proficiência Média em {selected_proficiency} por Nível Socioeconômico e Gênero')
ax.set_xlabel('Nível Socioeconômico (INSE)')
ax.set_ylabel(y_axis_label)
ax.legend(title='Gênero')
ax.grid(axis='y', linestyle='--', alpha=0.7) # Adiciona grade no eixo Y

plt.tight_layout() # Ajusta o layout para evitar sobreposição

# --- Exibir o gráfico no Streamlit ---
st.pyplot(fig)

# --- Informações Adicionais para o Streamlit ---
st.write("---")
st.write(f"Este gráfico de barras agrupadas exibe a proficiência média em **{selected_proficiency.lower()}** para estudantes masculinos e femininos em cada nível do Indicador de Nível Socioeconômico (INSE).")
st.write("Cada par de barras representa um nível INSE, com a barra azul para o sexo masculino e a barra laranja para o sexo feminino.")
st.write("A altura de cada barra indica a proficiência média para aquele grupo, permitindo a comparação direta de desempenho entre os gêneros e entre os diferentes estratos socioeconômicos.")

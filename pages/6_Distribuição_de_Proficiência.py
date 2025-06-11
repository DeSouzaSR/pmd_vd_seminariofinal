import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np # Necessário para np.arange
# Removido: from scipy.stats import gaussian_kde # Importa para cálculo do KDE

# --- Títulos e descrições para o Streamlit ---
st.write("# Distribuição de Proficiência por Nível Socioeconômico")
st.markdown(
    """
    As figuras apresentam histogramas da distribuição de proficiência em Língua Portuguesa e Matemática.
    Use o menu lateral à esquerda para selecionar um ou mais Níveis Socioeconômicos (INSE) para visualização.
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
required_cols = ['PROFICIENCIA_LP_SAEB', 'PROFICIENCIA_MT_SAEB', 'NU_TIPO_NIVEL_INSE']
missing_columns = [col for col in required_cols if col not in df_es.columns]

if missing_columns:
    st.error(f"Erro: As seguintes colunas necessárias não foram encontradas no arquivo CSV: {', '.join(missing_columns)}. Verifique o dicionário de dados e o arquivo.")
    st.stop()

# Forçar as colunas de proficiência e INSE a serem numéricas, tratando erros para NaN
df_es['PROFICIENCIA_LP_SAEB'] = pd.to_numeric(df_es['PROFICIENCIA_LP_SAEB'], errors='coerce')
df_es['PROFICIENCIA_MT_SAEB'] = pd.to_numeric(df_es['PROFICIENCIA_MT_SAEB'], errors='coerce')
df_es['NU_TIPO_NIVEL_INSE'] = pd.to_numeric(df_es['NU_TIPO_NIVEL_INSE'], errors='coerce')

# Remover linhas com valores nulos nas colunas essenciais
df_es.dropna(subset=['PROFICIENCIA_LP_SAEB', 'PROFICIENCIA_MT_SAEB', 'NU_TIPO_NIVEL_INSE'], inplace=True)

if df_es.empty:
    st.warning("Após o pré-processamento, não há dados válidos para plotar os histogramas.")
    st.stop()

# Mapeamento para exibir os níveis do INSE como strings
inse_display_labels = {
    1: 'Nível I', 2: 'Nível II', 3: 'Nível III', 4: 'Nível IV',
    5: 'Nível V', 6: 'Nível VI', 7: 'Nível VII', 8: 'Nível VIII'
}

# --- Seleção de Nível INSE na barra lateral ---
st.sidebar.header("Filtro por Nível Socioeconômico (INSE)")
# Obter os níveis INSE únicos e ordenados presentes nos dados
available_inse_levels = sorted(df_es['NU_TIPO_NIVEL_INSE'].unique())

selected_inse_levels_nums = st.sidebar.multiselect(
    label="Selecione um ou mais Níveis Socioeconômicos (INSE):",
    options=available_inse_levels,
    default=available_inse_levels, # Seleciona todos por padrão
    format_func=lambda x: inse_display_labels.get(x, f'INSE {x}')
)

# Se nada for selecionado, usar todos os níveis disponíveis
if not selected_inse_levels_nums:
    st.warning("Nenhum Nível Socioeconômico selecionado. Exibindo dados para todos os níveis disponíveis.")
    selected_inse_levels_nums = available_inse_levels

# Filtrar o DataFrame com base nos níveis INSE selecionados
df_filtered = df_es[df_es['NU_TIPO_NIVEL_INSE'].isin(selected_inse_levels_nums)].copy()

if df_filtered.empty:
    st.warning("Não há dados para os Níveis Socioeconômicos selecionados. Por favor, ajuste sua seleção.")
    st.stop()

# --- Criação dos Histogramas com Matplotlib ---
# Configura o layout para dois subplots na vertical, compartilhando o eixo X
fig, axes = plt.subplots(2, 1, figsize=(12, 14), sharex=True) # 2 linhas, 1 coluna

# --- Plot para Língua Portuguesa ---
ax_lp = axes[0]
data_lp_hist = [] # Dados para o histograma empilhado
labels_lp = []    # Rótulos para a legenda

# Coleta os dados e rótulos para o histograma empilhado
for level_num in sorted(selected_inse_levels_nums):
    subset_data = df_filtered[df_filtered['NU_TIPO_NIVEL_INSE'] == level_num]['PROFICIENCIA_LP_SAEB']
    if not subset_data.empty:
        data_lp_hist.append(subset_data)
        labels_lp.append(inse_display_labels.get(level_num, f'INSE {level_num}'))

if data_lp_hist:
    # Plota o histograma empilhado
    ax_lp.hist(data_lp_hist, bins=20, stacked=True, label=labels_lp, edgecolor='black', alpha=0.7)
    ax_lp.legend(title='Nível INSE') # Coloca a legenda após adicionar a KDE

ax_lp.set_title('Distribuição de Proficiência em Língua Portuguesa')
ax_lp.set_xlabel('Proficiência em LP')
ax_lp.set_ylabel('Frequência')
ax_lp.grid(axis='y', linestyle='--', alpha=0.7)


# --- Plot para Matemática ---
ax_mt = axes[1]
data_mt_hist = [] # Dados para o histograma empilhado
labels_mt = []    # Rótulos para a legenda

# Coleta os dados e rótulos para o histograma empilhado
for level_num in sorted(selected_inse_levels_nums):
    subset_data = df_filtered[df_filtered['NU_TIPO_NIVEL_INSE'] == level_num]['PROFICIENCIA_MT_SAEB']
    if not subset_data.empty:
        data_mt_hist.append(subset_data)
        labels_mt.append(inse_display_labels.get(level_num, f'INSE {level_num}'))

if data_mt_hist:
    # Plota o histograma empilhado
    ax_mt.hist(data_mt_hist, bins=20, stacked=True, label=labels_mt, edgecolor='black', alpha=0.7)
    ax_mt.legend(title='Nível INSE') # Coloca a legenda após adicionar a KDE

ax_mt.set_title('Distribuição de Proficiência em Matemática')
ax_mt.set_xlabel('Proficiência em MT')
ax_mt.set_ylabel('Frequência')
ax_mt.grid(axis='y', linestyle='--', alpha=0.7)

# Ajustar layout para evitar sobreposição
plt.tight_layout()

# --- Exibir os gráficos no Streamlit ---
st.pyplot(fig)

# --- Informações Adicionais para o Streamlit ---
st.write("---")
st.write("Estes histogramas mostram a distribuição da proficiência em Língua Portuguesa e Matemática para os Níveis Socioeconômicos (INSE) selecionados.")
st.write("As barras empilhadas indicam a frequência de estudantes em diferentes faixas de proficiência para cada nível de INSE. A legenda no canto superior direito indica a cor correspondente a cada nível INSE selecionado.")

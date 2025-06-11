import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# --- Títulos e descrições para o Streamlit ---
st.write("# Proficiência por Nível Socioeconômico e Gênero")
st.markdown(
    """
    A figura apresenta um gráfico BoxPlot agrupado que compara a distribuição da proficiência
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

# Mapear os valores de gênero diretamente (se já estiverem como 'Masculino'/'Feminino')
gender_mapping = {
    'Masculino': 'Masculino',
    'Feminino': 'Feminino'
}
df_es['TX_RESP_Q01_LABEL'] = df_es['TX_RESP_Q01'].map(gender_mapping)

# Remover linhas com valores nulos nas colunas essenciais para o plot
df_es.dropna(subset=['NU_TIPO_NIVEL_INSE', 'TX_RESP_Q01_LABEL', 'PROFICIENCIA_LP_SAEB', 'PROFICIENCIA_MT_SAEB'], inplace=True)

if df_es.empty:
    st.warning("Após o pré-processamento, não há dados válidos para plotar a distribuição de gênero e proficiência. Verifique as colunas de INSE, Gênero e Proficiências.")
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
    y_axis_label = 'Proficiência em Língua Portuguesa'
else:
    proficiency_col = 'PROFICIENCIA_MT_SAEB'
    y_axis_label = 'Proficiência em Matemática'


# --- Preparação dos Dados para o Box Plot Agrupado ---
sorted_inse_levels = sorted(df_es['NU_TIPO_NIVEL_INSE'].unique())
data_for_boxplot = []
xtick_labels = []
xtick_positions = []
box_positions = [] # Posições para cada box (Masculino e Feminino)

group_width = 0.75 # Largura total para o par de boxes
gap_between_groups = 0.5 # Espaço entre os grupos de INSE
box_spacing = 0.1 # Espaço entre Masculino e Feminino dentro de um grupo

current_position = 0 # Posição inicial para o primeiro grupo de boxes

for i, level_num in enumerate(sorted_inse_levels):
    # Dados para Masculino e Feminino no nível atual
    male_data = df_es[(df_es['NU_TIPO_NIVEL_INSE'] == level_num) & (df_es['TX_RESP_Q01_LABEL'] == 'Masculino')][proficiency_col]
    female_data = df_es[(df_es['NU_TIPO_NIVEL_INSE'] == level_num) & (df_es['TX_RESP_Q01_LABEL'] == 'Feminino')][proficiency_col]

    # Adicionar os dados, garantindo que não estejam vazios (para evitar erros no boxplot)
    # Se um gênero não tiver dados, o array ficará vazio, e o matplotlib lidará com isso.
    data_for_boxplot.append(male_data.tolist())
    data_for_boxplot.append(female_data.tolist())

    # Calcular as posições para os boxes Masculino e Feminino
    pos_male = current_position + (group_width / 2) - (box_spacing / 2)
    pos_female = current_position + (group_width / 2) + (box_spacing / 2)

    box_positions.append(pos_male)
    box_positions.append(pos_female)

    # Rótulo central para o grupo INSE
    xtick_labels.append(inse_display_labels.get(level_num, f'INSE {level_num}'))
    xtick_positions.append(current_position + group_width / 2)

    current_position += group_width + gap_between_groups # Avança para o próximo grupo


# --- Criação do Gráfico de Box Plot Agrupado com Matplotlib ---
fig, ax = plt.subplots(figsize=(14, 8)) # Cria a figura e os eixos

# Cores para Masculino e Feminino
colors = ['#1f77b4', '#ff7f0e'] # Azul para Masculino, Laranja para Feminino
box_colors = []
for _ in sorted_inse_levels:
    box_colors.extend(colors) # Alterna as cores para cada par (Masculino, Feminino)

# Crie os boxplots
bp = ax.boxplot(data_for_boxplot, positions=box_positions, widths=0.4, patch_artist=True,
                medianprops={'color': 'red'},
                boxprops=dict(edgecolor='black'))

# Atribuir cores aos boxes
for patch, color in zip(bp['boxes'], box_colors):
    patch.set_facecolor(color)

# Definir os rótulos do eixo X e suas posições
ax.set_xticks(xtick_positions)
ax.set_xticklabels(xtick_labels, rotation=45, ha='right') # Rotação para melhor leitura


# Criar legendas customizadas para Masculino e Feminino
handles = [plt.Rectangle((0,0),1,1, fc=colors[0], edgecolor='black'),
           plt.Rectangle((0,0),1,1, fc=colors[1], edgecolor='black')]
labels = ['Masculino', 'Feminino']
ax.legend(handles, labels, title='Gênero')


# Adicionar títulos e rótulos
ax.set_title(f'Distribuição de {selected_proficiency} por Nível Socioeconômico e Gênero')
ax.set_xlabel('Nível Socioeconômico (INSE)')
ax.set_ylabel(y_axis_label)
ax.grid(axis='y', linestyle='--', alpha=0.7) # Adiciona grade no eixo Y

plt.tight_layout() # Ajusta o layout para evitar sobreposição

# --- Exibir o gráfico no Streamlit ---
st.pyplot(fig)

# --- Informações Adicionais para o Streamlit ---
st.write("---")
st.write(f"Este gráfico de box plot compara a distribuição de **{selected_proficiency.lower()}** entre estudantes masculinos e femininos em cada nível do Indicador de Nível Socioeconômico (INSE).")
st.write("Para cada nível de INSE, as caixas azuis representam os estudantes masculinos e as caixas laranjas representam os estudantes femininos.")
st.write("A linha vermelha dentro de cada caixa indica a mediana, a caixa delimita o intervalo interquartil (25º a 75º percentil), e os 'bigodes' se estendem aos valores mínimo e máximo (excluindo *outliers*).")
st.write("Compare as posições e tamanhos das caixas e bigodes para identificar diferenças e tendências entre gêneros e níveis socioeconômicos.")

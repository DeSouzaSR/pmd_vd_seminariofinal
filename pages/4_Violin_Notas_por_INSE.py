import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt # Importa a biblioteca matplotlib
import numpy as np

# --- Títulos e descrições para o Streamlit ---
st.write("# Distribuição de Proficiência por Nível Socioeconômico (Gráfico de Violino)")
st.markdown(
    """
    A figura apresenta um gráfico de violino que ilustra a distribuição da proficiência selecionada
    (Proficiência Total, Língua Portuguesa ou Matemática) para cada nível do Indicador de Nível Socioeconômico (INSE).
    Observe as formas dos "violinos" para entender a densidade dos dados em diferentes pontos.
    """
)

# --- Leitura e Pré-processamento dos Dados ---
# Certifique-se de que o arquivo 'data/raw_data/df_es_filtrado.csv' está acessível.
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

# Cálculo da proficiência total
# Forçar as colunas de proficiência a serem numéricas, tratando erros para NaN
df_es['PROFICIENCIA_LP_SAEB'] = pd.to_numeric(df_es['PROFICIENCIA_LP_SAEB'], errors='coerce')
df_es['PROFICIENCIA_MT_SAEB'] = pd.to_numeric(df_es['PROFICIENCIA_MT_SAEB'], errors='coerce')
df_es['PROFICIENCIA_TOTAL'] = df_es['PROFICIENCIA_LP_SAEB'] + df_es['PROFICIENCIA_MT_SAEB']


# --- Preparação dos Dados para o Gráfico de Violino do Matplotlib ---
# Mapeamento para garantir a ordem correta dos níveis do INSE (I, II, ..., VIII)
# As chaves são os NÚMEROS que aparecem na coluna 'NU_TIPO_NIVEL_INSE'
inse_display_labels = {
    1: 'Nível I', 2: 'Nível II', 3: 'Nível III', 4: 'Nível IV',
    5: 'Nível V', 6: 'Nível VI', 7: 'Nível VII', 8: 'Nível VIII'
}

# Remover linhas onde a proficiência total é NaN OU onde o NU_TIPO_NIVEL_INSE é NaN
df_es.dropna(subset=['PROFICIENCIA_TOTAL', 'PROFICIENCIA_LP_SAEB', 'PROFICIENCIA_MT_SAEB', 'NU_TIPO_NIVEL_INSE'], inplace=True)

# Filtrar para incluir apenas os INSEs que estão no nosso dicionário de labels
df_es = df_es[df_es['NU_TIPO_NIVEL_INSE'].isin(inse_display_labels.keys())]

# Se após a remoção de NaNs e filtragem o DataFrame ficar vazio, avisar o usuário
if df_es.empty:
    st.warning("Após o pré-processamento, não há dados válidos para plotar. Verifique se os dados de INSE estão nos níveis esperados (1-8) e se há proficiência.")
    st.stop()

# --- Opção de seleção de proficiência no Streamlit (Sidebar) ---
st.sidebar.header("Opções de Visualização")
proficiency_option = st.sidebar.radio(
    "Selecione o tipo de proficiência:",
    ('Proficiência Total', 'Proficiência em Língua Portuguesa', 'Proficiência em Matemática')
)

# Mapear a opção selecionada para o nome da coluna no DataFrame
if proficiency_option == 'Proficiência Total':
    y_column_name = 'PROFICIENCIA_TOTAL'
    y_axis_label = 'Proficiência Total (LP + MT)'
elif proficiency_option == 'Proficiência em Língua Portuguesa':
    y_column_name = 'PROFICIENCIA_LP_SAEB'
    y_axis_label = 'Proficiência em Língua Portuguesa'
else: # Proficiência em Matemática
    y_column_name = 'PROFICIENCIA_MT_SAEB'
    y_axis_label = 'Proficiência em Matemática'


# Obter a lista de níveis de INSE numéricos únicos presentes no DataFrame após o tratamento, e ordená-los
present_and_sorted_inse_values = sorted(df_es['NU_TIPO_NIVEL_INSE'].unique())

# Criar uma lista de séries de dados e uma lista de rótulos para o gráfico de violino,
# garantindo que apenas os níveis com dados válidos sejam incluídos.
data_for_violinplot = []
labels_for_violinplot = []

for level_num in present_and_sorted_inse_values:
    # Usar a coluna selecionada dinamicamente
    subset_data = df_es[df_es['NU_TIPO_NIVEL_INSE'] == level_num][y_column_name]
    if not subset_data.empty: # Garante que só adiciona se houver dados para o nível
        data_for_violinplot.append(subset_data)
        # Usa o dicionário 'inse_display_labels' para obter o rótulo de string correto
        labels_for_violinplot.append(inse_display_labels.get(level_num, f'INSE {level_num}')) # Fallback se o número não estiver no dicionário

# --- Criação do Gráfico de Violino com Matplotlib ---
fig, ax = plt.subplots(figsize=(12, 6)) # Cria a figura e os eixos

# Passar os dados e os rótulos filtrados para o violinplot
# 'showmeans=True' adiciona uma marca para a média
# 'showmedians=True' adiciona uma marca para a mediana
# 'showextrema=False' remove as linhas que mostram os valores mínimo e máximo
ax.violinplot(data_for_violinplot, showmeans=True, showmedians=True)

# Define os rótulos do eixo X manualmente, pois violinplot não tem um parâmetro 'labels' direto como boxplot
ax.set_xticks(np.arange(1, len(labels_for_violinplot) + 1))
ax.set_xticklabels(labels_for_violinplot)


# Adicionar títulos e rótulos
ax.set_title(f'Distribuição de {proficiency_option} por Nível Socioeconômico')
ax.set_xlabel('Nível Socioeconômico (INSE)') # Rótulo mais claro
ax.set_ylabel(y_axis_label) # Rótulo do eixo Y dinâmico
ax.grid(True, axis='y', linestyle='--', alpha=0.7) # Adiciona grade no eixo Y

# --- Exibir o gráfico no Streamlit ---
st.pyplot(fig)

# --- Informações Adicionais para o Streamlit ---
st.write("---")
st.write(f"Este gráfico de violino exibe a distribuição das notas de **{proficiency_option.lower()}** para cada um dos níveis do Indicador de Nível Socioeconômico (INSE).")
st.write("A forma do violino mostra a densidade da distribuição dos dados. Linhas horizontais dentro de cada violino representam a média (linha contínua) e a mediana (linha tracejada).")
st.write("As áreas mais largas do violino indicam onde há uma maior concentração de estudantes.")

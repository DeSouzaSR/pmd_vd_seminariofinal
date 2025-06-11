import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt # Importa a biblioteca matplotlib

# --- Títulos e descrições para o Streamlit ---
st.write("# Proficiência em Língua Portuguesa vs Matemática")
st.markdown(
    """
    A figura apresenta um gráfico BoxPlot com as notas somadas de proficiências de Língua Portuguesa e Matemática
    para os valores de INSE. Observa-se aumento da mediana para índices INSE maiores.
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


# --- Preparação dos Dados para o Box Plot do Matplotlib ---
# Mapeamento para garantir a ordem correta dos níveis do INSE (I, II, ..., VIII)
# AGORA, as chaves são os NÚMEROS que aparecem na coluna 'NU_TIPO_NIVEL_INSE'
inse_display_labels = {
    1: 'Nível I', 2: 'Nível II', 3: 'Nível III', 4: 'Nível IV',
    5: 'Nível V', 6: 'Nível VI', 7: 'Nível VII', 8: 'Nível VIII'
}

# Remover linhas onde a proficiência total é NaN OU onde o NU_TIPO_NIVEL_INSE é NaN
df_es.dropna(subset=['PROFICIENCIA_TOTAL', 'NU_TIPO_NIVEL_INSE'], inplace=True)

# Filtrar para incluir apenas os INSEs que estão no nosso dicionário de labels
df_es = df_es[df_es['NU_TIPO_NIVEL_INSE'].isin(inse_display_labels.keys())]

# Se após a remoção de NaNs e filtragem o DataFrame ficar vazio, avisar o usuário
if df_es.empty:
    st.warning("Após o pré-processamento, não há dados válidos para plotar. Verifique se os dados de INSE estão nos níveis esperados (1-8) e se há proficiência.")
    st.stop()

# Obter a lista de níveis de INSE numéricos únicos presentes no DataFrame após o tratamento, e ordená-los
# Eles já são numéricos, então a ordenação natural funciona
present_and_sorted_inse_values = sorted(df_es['NU_TIPO_NIVEL_INSE'].unique())

# Criar uma lista de séries de dados e uma lista de rótulos para o box plot,
# garantindo que apenas os níveis com dados válidos sejam incluídos.
data_for_boxplot = []
labels_for_boxplot = []

for level_num in present_and_sorted_inse_values:
    subset_data = df_es[df_es['NU_TIPO_NIVEL_INSE'] == level_num]['PROFICIENCIA_TOTAL']
    if not subset_data.empty: # Garante que só adiciona se houver dados para o nível
        data_for_boxplot.append(subset_data)
        # Usa o dicionário 'inse_display_labels' para obter o rótulo de string correto
        labels_for_boxplot.append(inse_display_labels.get(level_num, f'INSE {level_num}')) # Fallback se o número não estiver no dicionário

# --- Criação do Box Plot com Matplotlib ---
fig, ax = plt.subplots(figsize=(12, 6)) # Cria a figura e os eixos

# Passar os dados e os rótulos filtrados para o boxplot
ax.boxplot(data_for_boxplot, labels=labels_for_boxplot, patch_artist=True, medianprops={'color': 'red'})

# Adicionar títulos e rótulos
ax.set_title('Distribuição de Proficiência Total por Nível Socioeconômico')
ax.set_xlabel('Nível Socioeconômico (INSE)') # Rótulo mais claro
ax.set_ylabel('Proficiência Total (LP + MT)')
ax.grid(True) # Adiciona a grade

# --- Exibir o gráfico no Streamlit ---
st.pyplot(fig)

# --- Informações Adicionais para o Streamlit ---
st.write("---")
st.write("Este gráfico exibe a distribuição das notas de proficiência total (soma de Língua Portuguesa e Matemática) para cada um dos níveis do Indicador de Nível Socioeconômico (INSE).")
st.write("A linha vermelha em cada caixa representa a mediana, e a caixa em si abrange o intervalo interquartil (do 25º ao 75º percentil). As 'hastes' ou 'bigodes' estendem-se aos valores máximo e mínimo dentro de um limite de 1.5 vezes o intervalo interquartil, e os pontos fora dessas hastes são considerados *outliers*.")

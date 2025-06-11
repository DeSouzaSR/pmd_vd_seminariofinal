import streamlit as st
import pandas as pd
import numpy as np # Importar numpy para a função .mode() e outras operações

st.set_page_config(page_title="Estatísticas Básicas", page_icon="📈")

st.markdown("# Estatísticas Básicas de Proficiência")
st.sidebar.header("Opções de Estatística")

# --- Leitura e Pré-processamento dos Dados ---
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
required_cols = ['NU_TIPO_NIVEL_INSE', 'PROFICIENCIA_LP_SAEB', 'PROFICIENCIA_MT_SAEB']
missing_columns = [col for col in required_cols if col not in df_es_filtrado.columns]

if missing_columns:
    st.error(f"Erro: As seguintes colunas necessárias não foram encontradas no arquivo CSV: {', '.join(missing_columns)}. Verifique o dicionário de dados e o arquivo.")
    st.stop()

# Forçar colunas de proficiência e INSE a serem numéricas, tratando erros para NaN
df_es_filtrado['PROFICIENCIA_LP_SAEB'] = pd.to_numeric(df_es_filtrado['PROFICIENCIA_LP_SAEB'], errors='coerce')
df_es_filtrado['PROFICIENCIA_MT_SAEB'] = pd.to_numeric(df_es_filtrado['PROFICIENCIA_MT_SAEB'], errors='coerce')
df_es_filtrado['NU_TIPO_NIVEL_INSE'] = pd.to_numeric(df_es_filtrado['NU_TIPO_NIVEL_INSE'], errors='coerce')

# Remover linhas com valores nulos nas colunas essenciais para as estatísticas
df_es_filtrado.dropna(subset=['NU_TIPO_NIVEL_INSE', 'PROFICIENCIA_LP_SAEB', 'PROFICIENCIA_MT_SAEB'], inplace=True)

if df_es_filtrado.empty:
    st.warning("Após o pré-processamento, não há dados válidos para calcular as estatísticas. Verifique as colunas de INSE e proficiências.")
    st.stop()

# Mapeamento para exibir os níveis do INSE como strings (para rótulos da tabela)
inse_display_labels = {
    1: 'Nível I', 2: 'Nível II', 3: 'Nível III', 4: 'Nível IV',
    5: 'Nível V', 6: 'Nível VI', 7: 'Nível VII', 8: 'Nível VIII'
}

# --- Cálculo da Tabela de Mínimos e Máximos ---
socioeconomic_min_max_stats = df_es_filtrado.groupby('NU_TIPO_NIVEL_INSE').agg(
    min_lp=('PROFICIENCIA_LP_SAEB', 'min'),
    max_lp=('PROFICIENCIA_LP_SAEB', 'max'),
    min_mt=('PROFICIENCIA_MT_SAEB', 'min'),
    max_mt=('PROFICIENCIA_MT_SAEB', 'max')
)
socioeconomic_min_max_stats = socioeconomic_min_max_stats.sort_index()
# Mapear o índice numérico do INSE para rótulos de string para exibição
socioeconomic_min_max_stats.index = socioeconomic_min_max_stats.index.map(lambda x: inse_display_labels.get(x, str(x)))

# Renomear colunas para a tabela de Mínimos e Máximos
socioeconomic_min_max_stats = socioeconomic_min_max_stats.rename(columns={
    'min_lp': 'Mínimo LP',
    'max_lp': 'Máximo LP',
    'min_mt': 'Mínimo MT',
    'max_mt': 'Máximo MT'
})

# --- Definir o nome do índice para exibição na tabela ---
socioeconomic_min_max_stats.index.name = "Nível Socioeconômico"


# --- Cálculo da Tabela de Média, Mediana e Moda ---
socioeconomic_mean_median_mode_stats = df_es_filtrado.groupby('NU_TIPO_NIVEL_INSE').agg(
    mean_lp=('PROFICIENCIA_LP_SAEB', 'mean'),
    median_lp=('PROFICIENCIA_LP_SAEB', 'median'),
    # A moda pode retornar múltiplos valores, pegamos o primeiro se existir
    mode_lp=('PROFICIENCIA_LP_SAEB', lambda x: x.mode()[0] if not x.mode().empty else np.nan),
    mean_mt=('PROFICIENCIA_MT_SAEB', 'mean'),
    median_mt=('PROFICIENCIA_MT_SAEB', 'median'),
    mode_mt=('PROFICIENCIA_MT_SAEB', lambda x: x.mode()[0] if not x.mode().empty else np.nan)
)
socioeconomic_mean_median_mode_stats = socioeconomic_mean_median_mode_stats.sort_index()
socioeconomic_mean_median_mode_stats = socioeconomic_mean_median_mode_stats.round(2)
# Mapear o índice numérico do INSE para rótulos de string para exibição
socioeconomic_mean_median_mode_stats.index = socioeconomic_mean_median_mode_stats.index.map(lambda x: inse_display_labels.get(x, str(x)))

# Renomear colunas para a tabela de Média, Mediana e Moda
socioeconomic_mean_median_mode_stats = socioeconomic_mean_median_mode_stats.rename(columns={
    'mean_lp': 'Média LP',
    'median_lp': 'Mediana LP',
    'mode_lp': 'Moda LP',
    'mean_mt': 'Média MT',
    'median_mt': 'Mediana MT',
    'mode_mt': 'Moda MT'
})

# --- Definir o nome do índice para exibição na tabela ---
socioeconomic_mean_median_mode_stats.index.name = "Nível Socioeconômico"


# --- Seleção do Tipo de Estatística na Barra Lateral ---
selected_stat_type = st.sidebar.radio(
    "Selecione o tipo de estatística a exibir:",
    ("Mínimo e Máximo", "Média, Mediana e Moda")
)

# --- Exibição Condicional da Tabela ---
if selected_stat_type == "Mínimo e Máximo":
    st.write("### Proficiência: Mínimos e Máximos por Nível Socioeconômico")
    st.markdown(
        """
        Esta tabela apresenta os valores mínimos e máximos de proficiência em Língua Portuguesa e Matemática
        para cada nível socioeconômico (INSE) dos estudantes.
        """
    )
    st.dataframe(socioeconomic_min_max_stats)
else: # selected_stat_type == "Média, Mediana e Moda"
    st.write("### Proficiência: Média, Mediana e Moda por Nível Socioeconômico")
    st.markdown(
        """
        Esta tabela exibe a média, mediana e moda da proficiência em Língua Portuguesa e Matemática,
        separadas por nível socioeconômico (INSE) dos estudantes. Todos os valores são arredondados para duas casas decimais.
        """
    )
    st.dataframe(socioeconomic_mean_median_mode_stats)

# --- Informações Adicionais para o Streamlit ---
st.write("---")
st.markdown(
    """
    As tabelas fornecem uma visão sumarizada do desempenho dos estudantes nas avaliações do SAEB, permitindo
    a comparação das estatísticas de proficiência entre os diferentes estratos socioeconômicos.
    """
)

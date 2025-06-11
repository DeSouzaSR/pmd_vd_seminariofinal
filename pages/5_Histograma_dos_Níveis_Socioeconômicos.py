import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np # Necessário para np.arange

# --- Títulos e descrições para o Streamlit ---
st.write("# Distribuição dos Níveis Socioeconômicos")
st.markdown(
    """
    A figura apresenta um histograma que mostra a distribuição de frequência
    dos estudantes por Nível Socioeconômico (INSE) na rede estadual do Espírito Santo.
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

# Verificar se a coluna essencial existe
required_col = 'NU_TIPO_NIVEL_INSE'
if required_col not in df_es.columns:
    st.error(f"Erro: A coluna '{required_col}' não foi encontrada no arquivo CSV. Verifique o dicionário de dados e o arquivo.")
    st.stop()

# Remover valores nulos da coluna INSE para a contagem de frequência
df_es.dropna(subset=[required_col], inplace=True)

# Garantir que a coluna INSE é numérica, se não for, tentar converter e remover NaNs
df_es[required_col] = pd.to_numeric(df_es[required_col], errors='coerce')
df_es.dropna(subset=[required_col], inplace=True)

if df_es.empty:
    st.warning("Após o pré-processamento, não há dados válidos para plotar o histograma de INSE.")
    st.stop()

# --- Criação do Histograma com Matplotlib ---
fig, ax = plt.subplots(figsize=(10, 6))

# Definir os bins para os níveis de INSE (1 a 8)
# Criamos bins para que cada nível seja o centro de um bin
# Por exemplo, para INSE 1, o bin seria de 0.5 a 1.5
bins = np.arange(0.5, 9.5, 1) # Bins de 0.5 a 8.5 com passo de 1

ax.hist(df_es[required_col], bins=bins, edgecolor='black', alpha=0.7)

# Definir os rótulos do eixo X para os níveis de INSE
# Centrar os ticks nos valores inteiros dos níveis
ax.set_xticks(np.arange(1, 9))

# Mapeamento para garantir a ordem correta dos níveis do INSE (I, II, ..., VIII)
inse_display_labels = {
    1: 'Nível I', 2: 'Nível II', 3: 'Nível III', 4: 'Nível IV',
    5: 'Nível V', 6: 'Nível VI', 7: 'Nível VII', 8: 'Nível VIII'
}
# Cria os rótulos para os ticks, usando o mapeamento
tick_labels = [inse_display_labels.get(i, str(i)) for i in np.arange(1, 9)]
ax.set_xticklabels(tick_labels, rotation=45, ha='right')


# Adicionar títulos e rótulos
ax.set_title('Distribuição dos Níveis Socioeconômicos (INSE)')
ax.set_xlabel('Nível Socioeconômico')
ax.set_ylabel('Frequência')
ax.grid(axis='y', linestyle='--', alpha=0.7) # Adiciona grade no eixo Y

# --- Exibir o gráfico no Streamlit ---
st.pyplot(fig)

# --- Informações Adicionais para o Streamlit ---
st.write("---")
st.write("Este gráfico mostra a contagem de estudantes em cada um dos oito níveis do Indicador de Nível Socioeconômico (INSE).")
st.write("Observar a forma desta distribuição pode indicar a predominância de estudantes em determinados estratos socioeconômicos na base de dados analisada.")

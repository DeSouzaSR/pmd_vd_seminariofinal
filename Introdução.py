import streamlit as st

st.set_page_config(
    page_title = "Início"
)

st.write("# Desempenho SAEB 2023: Uma Análise Visual por Nível Socioeconômico no Ensino Médio Capixaba")
st.sidebar.success("Selecione uma exibição de dados acima")

st.markdown(
    """
    ## Trabalho para a disciplina de Visualização de Dados da Pós-graduação em Mineração de Dados do IFES - Serra - ES"
    
    * **Professor**: Dr. Richard Junior Manuel Godinez Tello
    * **Autores**:
        - Cristiani Oliveira
        - Katia Franco
        - Sandro De Souza
        - Ueliton Oliveira
        
    * **Fonte dos dados**: [INEP](https://www.gov.br/inep/pt-br/areas-de-atuacao/avaliacao-e-exames-educacionais/saeb/resultados)
    
    """
)

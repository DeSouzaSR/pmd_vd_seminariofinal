import streamlit as st

st.set_page_config(
    page_title="Início",
    layout="centered", # Define o layout da página como centralizado
    initial_sidebar_state="expanded" # Expande a barra lateral por padrão
)

# Título principal do aplicativo, conforme definido anteriormente
st.write("# Desempenho SAEB 2023: Uma Análise Visual por Nível Socioeconômico no Ensino Médio Capixaba")

# Mensagem na barra lateral para guiar o usuário
#st.sidebar.success("Selecione uma exibição de dados acima para iniciar a análise.")

# Separador visual para organização do conteúdo
st.markdown("---")

# Contexto Acadêmico e Detalhes da Autoria
st.subheader("Contexto Acadêmico e Autoria")
st.markdown(
    """
    Este aplicativo interativo foi desenvolvido como parte dos requisitos para a disciplina de **Visualização de Dados**,
    integrante do curso de Pós-graduação em Mineração de Dados do **Instituto Federal do Espírito Santo (IFES) - Campus Serra**.
    """
)

# Detalhes do Professor
st.markdown("##### Orientação")
st.markdown("Professor: Dr. Richard Junior Manuel Godinez Tello")

# Detalhes dos Autores
st.markdown("##### Desenvolvimento")
st.markdown(
    """
    Autores: Cristiani Oliveira, Katia Franco, Sandro De Souza, Ueliton Oliveira
    """
)

# Separador visual
st.markdown("---")

# Propósito do Aplicativo e Escopo do Estudo
st.subheader("Propósito do Aplicativo")
st.markdown(
    """
    O presente trabalho tem como objetivo explorar e visualizar os microdados do Sistema de Avaliação da Educação Básica (SAEB)
    referentes ao ano de 2023. Por meio de gráficos e análises visuais, investiga-se a relação entre o nível socioeconômico
    dos estudantes do Ensino Médio da rede estadual do Espírito Santo e seu desempenho nas avaliações. Esta análise inclui
    recortes específicos de proficiência em Língua Portuguesa e Matemática, bem como uma exploração da distribuição por gênero.
    Este aplicativo serve como a fase inicial de um projeto de análise de dados mais abrangente,
    focando primariamente na exploração descritiva dos dados.
    """
)

# Separador visual
st.markdown("---")

# Seção de Fonte dos Dados
st.subheader("Fonte dos Dados")
st.markdown(
    """
    Os dados utilizados nesta análise são provenientes do Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira (INEP),
    disponíveis publicamente e acessíveis através do seguinte link: [Microdados SAEB - INEP](https://www.gov.br/inep/pt-br/areas-de-atuacao/avaliacao-e-exames-educacionais/saeb/resultados).
    """
)

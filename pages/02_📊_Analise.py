import streamlit as st
import plotly.express as px



st.set_page_config(page_title="Visualização dos dados", layout="wide", page_icon=":bar_chart:")
st.header("Análise Exploratória de Dados", divider="blue")


# Verifica se os dados estão carregados
if "dados" not in st.session_state:
    st.error("Os dados não foram carregados corretamente")
else: #Colunas para caixas de seleção
    dados = st.session_state["dados"]
    categoricas = [col for col in dados.columns if dados[col].dtype == "object"]
    numericas = [col for col in dados.columns if dados[col].dtype in ["int64", "float64"]]
    
    #Barra Lateral    
    with st.sidebar:        
        coluna1 = st.selectbox("Selecione o atributo categórico para exibir", categoricas, key="selectbox1")
        coluna2 = st.selectbox("Selecione o atributo numérico para exibir", numericas, key="selectbox2")        
        analisar = st.button("Gerar Gráficos")
    #Configuração da visualização dos dados categóricos
    if analisar:
        if coluna1 in categoricas:
            agrupado = dados[coluna1].value_counts().reset_index()
            agrupado.columns = [coluna1, "Quantidade"]
            fig = px.bar(agrupado, x=coluna1, y="Quantidade", title=f"Gráfico de barras de {coluna1}", color="Quantidade")
            fig.update_layout(yaxis_title="Contagem de Clientes", xaxis_title=f"Distribuição de {coluna1}")
            st.plotly_chart(fig, use_container_width=True)
        #Configuração da visualização dos dados numéricos
        if coluna2 in numericas:
            fig = px.histogram(dados, x=coluna2, title=f"Histograma de {coluna2}")
            fig.update_layout(yaxis_title="Contagem de clientes", xaxis_title=f"Distribuição de {coluna2}" )
            fig.update_traces(text=f"Distribuição de {coluna2}", textposition="none", hovertemplate="Quantidade: %{y}<br>Intervalo: %{x} ")
            st.plotly_chart(fig, use_container_width=True)










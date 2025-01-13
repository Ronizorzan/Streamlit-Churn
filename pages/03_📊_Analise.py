import streamlit as st
import pandas as pd
import plotly.express as px



st.set_page_config(page_title="Visualização dos dados", layout="wide", page_icon=":bar_chart:")


# Verifica se os dados estão carregados
if "dados" not in st.session_state:
    st.error("Os dados não foram carregados corretamente")
else: #Colunas para caixas de seleção
    dados = st.session_state["dados"]
    categoricas = [col for col in dados.columns if dados[col].dtype == "object"]
    numericas = [col for col in dados.columns if dados[col].dtype in ["int64", "float64"]]
    
    #Barra Lateral    
    with st.sidebar:
        st.header("Análise Exploratória de Dados")
        coluna1 = st.selectbox("Selecione o atributo categórico para exibir", categoricas, key="selectbox1")
        coluna2 = st.selectbox("Selecione o atributo numérico para exibir", numericas, key="selectbox2")
        escala_cores = ["blues", "balance", "Viridis", "Plasma", "Magma", "Cividis", "Blues", "Greens", "Turbo", "IceFire", "Electric"]
        escala_cores2 = [ "lightblue", "lightcoral", "lightcyan", "lightgoldenrodyellow", "lightgray", "lightgrey", "lightgreen",
                          "lightpink", "lightsalmon", "lightseagreen", "lightskyblue", "lightslategray", "lightslategrey", "lightsteelblue", "lightyellow"]
        cores = st.selectbox("Selecione a escala de cores para o gráfico de barras", escala_cores, index=0)
        cores2 = st.selectbox("Selecione a cor do Histograma", escala_cores2, index=0)
        analisar = st.button("Gerar Gráficos")
    #Configuração da visualização dos dados categóricos
    if analisar:
        if coluna1 in categoricas:
            agrupado = dados[coluna1].value_counts().reset_index()
            agrupado.columns = [coluna1, "contagem"]
            fig = px.bar(agrupado, x=coluna1, y="contagem", title=f"Gráfico de barras de {coluna1}", color="contagem", color_continuous_scale=str(cores))
            fig.update_layout(yaxis_title="Contagem de Clientes", xaxis_title=f"Distribuição de {coluna1}")
            st.plotly_chart(fig, use_container_width=True)
        #Configuração da visualização dos dados numéricos
        if coluna2 in numericas:
            fig = px.histogram(dados, x=coluna2, title=f"Histograma de {coluna2}", color_discrete_sequence=[cores2])
            fig.update_layout(yaxis_title="contagem de clientes", xaxis_title=f"Distribuição de {coluna2}" )
            st.plotly_chart(fig, use_container_width=True)










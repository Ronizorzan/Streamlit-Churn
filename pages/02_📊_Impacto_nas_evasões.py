import streamlit as st
from functions import *



st.set_page_config(page_title="Visualização de Impacto do Modelo", layout="wide", page_icon=":bar_chart:")
st.header("Impacto na Taxa de Evasão", divider="green")

# Verifica se os dados estão carregados
if "confusao" not in st.session_state:
    st.error("A matriz não foi carregada corretamente")
else:
    matriz_confusao = st.session_state["confusao"]
    markdown = st.session_state["markdown"]
        
    with st.sidebar:        
        # Permitir que o usuário insira a taxa de retenção estimada para os clientes de risco
        taxa_retencao_estimada = st.slider("Taxa de Retenção para Clientes de Alto Risco corretamente identificados pelo modelo:",
                                        0, 100, 75, help="Essa é a porcentagem de clientes retidos com \
                                        \ncampanhas de marketing bem-sucedidas\
                                        \n(100 indica que 100% dos clientes em risco\
                                        \ncorretamente identificados pelo modelo foram retidos)") / 100 
        
        calcular = st.button("Calcular Métricas")
        st.markdown(markdown, unsafe_allow_html=True)


    if calcular:
        resultado = calcular_metricas(matriz_confusao, taxa_retencao_estimada)
        grafico1 = plot_barras_empilhadas(resultado)
        col1, col2 = st.columns([0.65,0.35], gap="medium")
        with col1:
            st.pyplot(grafico1, use_container_width=True)
        
        with col2:
            st.markdown("<div style='font-size:28px; font-weight:bold'>Estimativa de  Impacto com a Intervenção", unsafe_allow_html=True)
                                                
            #Taxa de Evasão atual
            st.markdown("<hr style='border: 1px solid green'>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:19px; font-weight:bold'>🚨Taxa de Evasão Atual:\
                       <span style='color: red'>{resultado['Taxa_Evasão_atual']}%</span> do total de clientes.", unsafe_allow_html=True)
            
            st.text("")  # Taxa de Evasão estimada com o uso do Modelo
            st.markdown(f"<div style='font-size:19px; font-weight:bold'>⬇️Nova Taxa de Evasão Estimada:\
                        <span style='color:green'>{round(resultado['Nova_taxa_evasão'], 2)}%</span> do total de Clientes", unsafe_allow_html=True)
            
            st.text("") # Retenção de Clientes
            st.write(f"""<div style='font-size:19px; font-weight:bold'>⬆️De um total de <span style="color:red">{resultado['Total_Evasões_atuais']}</span>
                     clientes com risco de evasão <span style="color:green">{resultado['Estimativa_clientes_retidos']}</span> foram<br>
                     retidos com campanhas direcionadas pelo modelo.</div>""", unsafe_allow_html=True )
            st.markdown("<hr style='border: 1px solid green'>", unsafe_allow_html=True)

            #Redução percentual nas evasões
            st.markdown(f"<div style='font-size:35px; font-weight:bold'>-----------Resultado Final-----------", unsafe_allow_html=True)
            st.markdown("<hr style='border: 1px solid green'>", unsafe_allow_html=True)
            reducao_percentual = (resultado['Estimativa_clientes_retidos'] / resultado['Total_Evasões_atuais']) * 100
            st.write(f"<div style='font-size:25px; font-weight:bold'>Uma redução de\
                     <span style='color:green; font-size: 28px'>{round(reducao_percentual, 2)}%</span> no total de Evasões,\
                        considerando que <span style='color: #305099'>{taxa_retencao_estimada*100}0%</span> dos clientes identificados pelo modelo\
                             foram retidos com campanhas de marketing direcionadas.", unsafe_allow_html=True)
            
    
#Página de cálculos financeiros
import streamlit as st
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix
from yellowbrick.classifier import ConfusionMatrix
from matplotlib.pyplot import gca, Circle, legend


st.set_page_config(page_title="Cálculos Financeiros e Métricas", layout="wide",page_icon=":moneybag:")

if "modelo" not in st.session_state:
    st.error("O modelo não foi carregado corretamente")

else:
    modelo = st.session_state["modelo"]
    X_treinamento = st.session_state["X_treinamento"]
    y_treinamento = st.session_state["y_treinamento"]
    X_teste = st.session_state["X_teste"]
    y_teste = st.session_state["y_teste"]
    confusao = st.session_state["confusao"]
    markdown = st.session_state["markdown"]

    #Configuração da barra lateral
    with st.sidebar.expander("Configurações Financeiras", expanded=True):
        cobranca_media = st.number_input("Insira a média de Cobranças Mensais por Cliente", min_value=0.0, value=100.0, step=1.0, 
                                         help="Insira o valor médio gasto por cada cliente")
        gasto_campanhas = st.number_input("Insira o Gasto Médio por Cliente com Campanhas ", min_value=0.0, value=5.0, step=1.0, 
                                          help="Insira o gasto médio com campanhas")
        retencao = st.slider("Porcentagem de Clientes retidos com campanhas", min_value=0, max_value=100, value=90, 
                             help="Selecione a porcentagem de clientes retidos \
                                \n com campanhas bem sucedidas") / 100
        previsoes = modelo.predict(X_teste)
        
        #Cálculos das Métricas                 
        verd_neg = confusao[0][0]
        verd_posit = confusao[1][1]
        falso_posit = confusao[0][1]
        falso_neg = confusao[1][0]   
        clientes_nao_evasivos = verd_neg + falso_posit
        clientes_evasivos = verd_posit + falso_neg
        precision = precision_score(y_teste, previsoes, average="macro")
        recall = recall_score(y_teste, previsoes, average="macro")
        f1 = f1_score(y_teste, previsoes, average="macro")
        acuracia = st.session_state["acuracia"]
        calcular = st.button("Calcular")        
        st.sidebar.markdown(markdown, unsafe_allow_html=True)
    if calcular:
        col1, col2 = st.columns([0.45,0.55], gap="large")
        with col1: # Matriz de Confusão Gráfica            
            cm = ConfusionMatrix(modelo, classes=["Não", "Sim"], cmap="Blues", percent=False)            
            cm.fit(X_teste, y_teste)
            cm.score(X_teste, y_teste)
            
            #Adição de círculo e legenda para destacar erros e acertos do modelo
            for i in range(confusao.shape[0]):
                for j in range(confusao.shape[1]):
                    if i != j:
                        gca().add_patch(Circle((j + 0.5, i + 0.5), 0.2, fill=False, color="green", linewidth=1.0))  
                    else:
                        gca().add_patch(Circle((j + 0.5, i + 0.5), 0.2, fill=False, color="red", linewidth=1.0))
                        legend(["Erros do Modelo", "Acertos do Modelo"], bbox_to_anchor=(0.15, -0.05))
            st.subheader(":blue[**A Matriz abaixo exibe os erros e acertos do modelo**]", divider="blue", help="Confira abaixo o desempenho do modelo\
                                \n do ponto de vista técnico")
            st.pyplot(cm.fig, use_container_width=True)
            st.write("""<div style="font-size:24px; font-weight:bold"> 
                     A matriz de confusão acima traz uma visão clara\
                     e abrangente do desempenho geral do modelo.</div>""", unsafe_allow_html=True)
            
            
            
        with col2: #Cálculos do Retorno Financeiro            
            calculo_retencao = verd_posit * (retencao) * cobranca_media #Cálculo do retorno com clientes que não "evadiram"
            calculo_campanha = falso_posit * gasto_campanhas  #Cálculo de Gastos com clientes que não iam "evadir"
            calculo_perdas = falso_neg * cobranca_media #Perdas com clientes que "churnaram"
            retorno_liquido = calculo_retencao - (calculo_campanha + calculo_perdas) #Retorno líquido após dedução dos valores perdidos
                                                                                            #   com campanhas desnecessárias e perda de clientes que "churnaram"


            st.subheader(":blue[Métricas Adicionais (Detalhes técnicos)]", divider="blue", help="Confira abaixo algumas métricas\
                         detalhadas do desempenho do modelo")
            st.write(f"<div style='color:#1968D4; font-size:20px; font-weight:bold'> Acurácia do Modelo:  {acuracia*100:.2f}%", unsafe_allow_html=True)
            st.write("<div style='font-size:18px; font-weight:bold'> --> O modelo acertou aproximadamente 8 de 10 previsões nos dados de teste </div>", unsafe_allow_html=True)
            st.write(f"<div style='color:#1968D4; font-size:20px; font-weight:bold'>Precisão(Precision): {precision*100:.2f}%</div>", unsafe_allow_html=True)
            st.write("<div style='font-size:18px; font-weight:bold'> --> De todos os previstos como \'evasivos\' quantos realmente evadiram</div>", unsafe_allow_html=True)
            st.write(f"<div style='color:#1968D4; font-size:20px; font-weight:bold'>Sensibilidade(Recall):  {recall*100:.2f}%</div>", unsafe_allow_html=True)
            st.write("<div style='font-size:18px; font-weight:bold'> --> De todos os \'evasivos\', quantos foram corretamente identificados pelo Modelo </div>", unsafe_allow_html=True)
            st.write(f"<div style='color:#1968D4; font-size:20px; font-weight:bold'>F1-Score: {f1*100:.2f}%</div>", unsafe_allow_html=True)
            st.write("<div style='font-size:18px; font-weight:bold'> --> Média poderada: Calculada através da média harmônica de Precisão e Sensibilidade</div>", unsafe_allow_html=True )
            

            #Visualização dos Cálculos            
            st.write(" ")   
            st.subheader(":blue[**Retorno Financeiro calculado através da Matriz ao lado**]", divider="blue", help="Abaixo você confere o impacto do modelo\
                         do ponto de vista de negócio")
            st.write("<div style='font-size:20px; font-weight:bold'> Valor Mensal Obtido com Retenção de Clientes:</div>", unsafe_allow_html=True)
            st.write(f"<div style='color:green; font-size:22px; font-weight:bold'>Clientes com risco de evasão corretamente \
                     identificados --- > R$ {calculo_retencao:,.2f}</div><br>", unsafe_allow_html=True)
            st.write("<div style='font-size:20px; font-weight:bold'> Valor Mensal gasto com Clientes fora de Risco:</div>", unsafe_allow_html=True)
            st.write(f"<div style='color:red; font-size:22px; font-weight:bold'> Clientes sem risco de evasão classificados \
                     como em risco --- > R$ {calculo_campanha:,.2f}</div><br>", unsafe_allow_html=True)
            st.write("<div style='font-size:20px; font-weight:bold'> Valor Mensal Perdido com Evasões:</div>", unsafe_allow_html=True)
            st.write(f"<div style='color:red; font-size:22px; font-weight:bold'>Clientes com risco de evasão não identificados\
                     --- > R$ {calculo_perdas:,.2f}</div><br>", unsafe_allow_html=True)
                                    
            st.write("<div style='font-size:30px; font-weight:bold'>Impacto Financeiro Final</div>", unsafe_allow_html=True)

            if retorno_liquido >0:                
                st.write(f"<div style='color:green; font-size:26px; font-weight:bold'>Valor Líquido Mensal Retornado com o Uso do Modelo: \
                                        {retorno_liquido:,.2f}</div>", unsafe_allow_html=True)

            else:                
                st.write(f"<div style='color:red; font-size:26px; font-weight:bold'> Valor Líquido Mensal Retornado com o Uso do Modelo: \
                            {retorno_liquido:,.2f}</div>", unsafe_allow_html=True)
            



    









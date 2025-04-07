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

    #Configuração da barra lateral
    with st.sidebar.expander("Configurações Financeiras"):
        cobranca_media = st.number_input("Insira a média de Cobranças Mensais por Cliente", min_value=0.0, value=100.0, step=1.0)
        gasto_campanhas = st.number_input("Insira o Gasto Médio por Cliente com Campanhas ", min_value=0.0, value=5.0, step=1.0)
        retencao = st.slider("Porcentagem de Clientes retidos com campanhas", min_value=0.0, max_value=100.0, value=90.0)
        previsoes = modelo.predict(X_teste)
        confusao = confusion_matrix(y_teste, previsoes)
        precision = precision_score(y_teste, previsoes, average="weighted")
        recall = recall_score(y_teste, previsoes, average="weighted")
        f1 = f1_score(y_teste, previsoes, average="macro")
        acuracia = st.session_state["acuracia"]
        calcular = st.button("Calcular")
    if calcular:
        col1, col2 = st.columns(2, gap="large")
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
            st.subheader(":blue[**A Matriz abaixo exibe os erros e acertos do modelo**]", divider="blue")
            st.pyplot(cm.fig, use_container_width=True)
            st.write("""<div style="font-size:20px; font-weight:bold; color:darkblue"> 
                     A matriz de confusão acima mostra uma visão abrangente do desempenho do modelo destacando não só os acertos 
                     mas também os erros do modelo. Isso possibilita uma visão informativa e realista 
                     do desempenho do modelo</div>""", unsafe_allow_html=True)
            
            
        with col2: #Cálculos do Retorno Financeiro
            verd_neg = confusao[0][0]
            verd_posit = confusao[1][1]
            falso_posit = confusao[0][1]
            falso_neg = confusao[1][0]
            retencao = retencao / 100
            calculo_retencao = verd_posit * (retencao) * cobranca_media #Cálculo do retorno com clientes que não "churnaram"
            calculo_campanha = falso_posit * gasto_campanhas  #Cálculo de Gastos com clientes que não iam "churnar"
            calculo_perdas = falso_neg * cobranca_media #Perdas com clientes que "churnaram"
            retorno_liquido = calculo_retencao - (calculo_campanha + calculo_perdas) #Retorno líquido após dedução dos valores perdidos
                                                                                            #   com campanhas desnecessárias e perda de clientes que "churnaram"


            st.subheader(":blue[**Métricas Adicionais**]", divider="blue")
            st.write(f"**Acurácia:**    :green[**{acuracia*100:.2f}%**]  -  ***Desempenho Geral do Modelo - Acerta aproximadamente 8 de 10 previsões*** ")
            st.write(f"**Precisão:**    :green[**{precision*100:.2f}%**] - ***Mede a porcentagem de clientes previstos como \'churn\' que realmente evadiram***")
            st.write(f"**Recall:**      :green[**{recall*100:.2f}%**]    - ***Mede a capacidade do Modelo de identificar clientes com risco de evasão***")
            st.write(f"**F1-Score:**    :green[**{f1*100:.2f}%**]        - ***Média Harmônica de Precisão e Recall, ajustada para a importância de cada classe***" )
            

            #Visualização dos Cálculos            
            st.markdown(" ")            
            st.subheader(":blue[**Retorno Financeiro calculado de acordo com a Matriz ao lado**]", divider="blue")
            st.write(f"**Valor Mensal Obtido com Retenção de Clientes:** :green[***R$ {calculo_retencao:,.2f}***]")
            st.write(f"**Valor Mensal gasto com Clientes fora de Risco:** :red[***R$ {calculo_campanha:,.2f}***]")            
            st.write(f"**Valor Mensal Perdido com Evasões:** :red[***R$ {calculo_perdas:,.2f}***]")
            if retorno_liquido >0:
                st.success(f"**Valor Líquido Mensal Retornado com o Uso do Modelo: {retorno_liquido:,.2f}**")
                #st.markdown(f"<div style='color:green; font-size:22px; font-weight:bold'>Valor Líquido Mensal Retornado com o Uso do Modelo: \
                 #            {retorno_liquido:,.2f}</div>", unsafe_allow_html=True)

            else:
                st.error(f"**Valor Líquido Mensal Retornado com o Uso do Modelo: {retorno_liquido:,.2f}**")
                #st.markdown(f"<div style='color:red; font-size:22px; font-weight:bold'> Valor Líquido Mensal Retornado com o Uso do Modelo: \
                 #           {retorno_liquido:,.2f}</div>", unsafe_allow_html=True)
            



    








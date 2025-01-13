#Página de cálculos financeiros
import streamlit as st
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix, accuracy_score
from yellowbrick.classifier import ConfusionMatrix


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
        acuracia = accuracy_score(y_teste, previsoes)
        calcular = st.button("Calcular")
    if calcular:
        col1, col2 = st.columns(2, gap="medium", vertical_alignment="center")
        with col1: # Matriz de Confusão Gráfica
            st.markdown("**Descrição:** A Matriz abaixo mostra na diagonal principal os acertos do modelo")
            cm = ConfusionMatrix(modelo, classes=["Não", "Sim"], cmap="Purples", percent=False)
            cm.fit(X_teste, y_teste)
            cm.score(X_teste, y_teste)
            cm.show()
            st.pyplot(cm.fig)
            
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


            st.markdown("**Métricas Adicionais**")
            st.write(f"Acurácia:    {acuracia*100:.2f}%  -  Desempenho Geral do Modelo ")
            st.write(f"Precisão:    {precision*100:.2f}% - Mede a porcentagem de clientes previstos como \'churn\' que realmente evadiram")
            st.write(f"Recall:      {recall*100:.2f}%    - Mede a capacidade do Modelo de identificar clientes clientes com risco de evasão")
            st.write(f"F1-Score:    {f1*100:.2f}%        - Média Harmônica de Precisão e Recall, ajustada para a importância de cada classe")

            #Visualização dos Cálculos
            st.markdown("**Retorno Financeiro Mensal calculado de acordo com a Matriz ao lado**")
            st.write(f"Valor Mensal Obtido com Retenção de Clientes: R$ {calculo_retencao:.2f}")
            st.write(f"Valor Mensal gasto com Clientes fora de Risco: R$ {calculo_campanha:.2f}")
            st.write(f"Valor Mensal Perdido com Evasões: R$ {calculo_perdas:.2f}")
            st.write(f"Valor Líquido Mensal Retornado com o Uso do Modelo: R$ {retorno_liquido:.2f}")






    








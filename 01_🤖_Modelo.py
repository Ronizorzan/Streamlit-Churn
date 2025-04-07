#Página Principal
import pandas as pd
import streamlit as st
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import RFE




#Configuração do Layout da página
st.set_page_config("Classificação de Churn", layout="centered", page_icon=":robot_face:")
st.title("Previsões do Modelo")


#Função principal para criação do modelo e tratamento dos dados
@st.cache_resource
def load_data():
    churn = pd.read_csv("dados_tratados.csv")
    X = churn.drop("Churn", axis=1)
    y = churn["Churn"]
    X_treinamento, X_teste, y_treinamento, y_teste = train_test_split(X,y, test_size=0.3, random_state=1238)

    #Criação de objetos label-encoder para decodificação dos dados
    encoders = dict()
    for colunas in X_treinamento.columns:
        encoder = LabelEncoder()
        if X_treinamento[colunas].dtype=="object":
            X_treinamento[colunas] = encoder.fit_transform(X_treinamento[colunas])
            X_teste[colunas] = encoder.transform(X_teste[colunas])
            encoders[colunas] = encoder
        
    
                  
    encoder_y = LabelEncoder()
    y_treinamento = encoder_y.fit_transform(y_treinamento)
    y_teste = encoder_y.transform(y_teste)

    seletor = RFE(RandomForestClassifier(class_weight="balanced"), n_features_to_select=10, step=1 )
    seletor.fit(X_treinamento, y_treinamento)
    X_treinamento = seletor.transform(X_treinamento)
    X_teste = seletor.transform(X_teste)                                        # "Hiper-parâmetros anteriores"
    #floresta = RandomForestClassifier(bootstrap = True, max_depth = 10, max_leaf_nodes = 50, n_estimators = 500, warm_start = False, class_weight={0:1,1:2.5}) 
    floresta = RandomForestClassifier(bootstrap=True, criterion="gini", max_features=0.1, min_samples_leaf=3,
                                       min_samples_split=2, n_estimators=100, class_weight={0:1, 1:1.85}, random_state=3231)
    modelo = floresta.fit(X_treinamento, y_treinamento)
    previsoes = cross_val_score(modelo, X_teste, y_teste, cv=5)
    acuracia = previsoes.mean()


    return churn, X_treinamento, X_teste, y_treinamento, y_teste, modelo, acuracia, encoders, encoder_y, seletor



dados, X_treinamento, X_teste, y_treinamento, y_teste, modelo, acuracia, encoders, encoder_y, seletor = load_data()


#Compartilhamento de objetos entre as diferentes páginas
st.session_state["dados"] = dados
st.session_state["X_treinamento"] = X_treinamento
st.session_state["X_teste"] = X_teste
st.session_state["y_treinamento"] = y_treinamento
st.session_state["y_teste"] = y_teste
st.session_state["modelo"] = modelo
st.session_state["acuracia"] = acuracia
st.session_state["encoders"] = encoders
st.session_state["seletor"] = seletor
        



#Configuração das caixas de seleção
st.write(f"**Acurácia Aproximada do Modelo:**  :green[**{acuracia*100:.2f}%**]")
with st.expander("Selecione os atributos para prever"):    
    novos_dados =   [st.selectbox("Gênero", dados["gender"].unique()),
    st.selectbox("Idoso", dados["SeniorCitizen"].unique()),                         
    st.selectbox("Parceiro", dados["Partner"].unique(), index=0),
    st.selectbox("Dependentes", dados["Dependents"].unique(), index=0),
    st.number_input("Tempo de Serviço", min_value=1, value=1),
    st.selectbox("Serviço de Telefone", dados["PhoneService"].unique()),
    st.selectbox("Linhas Múltiplas", dados["MultipleLines"].unique()),
    st.selectbox("Serviço de Internet", dados["InternetService"].unique(), index=1),
    st.selectbox("Segurança Online", dados["OnlineSecurity"].unique(), index=1),
    st.selectbox("Back-up Online", dados["OnlineBackup"].unique()),
    st.selectbox("Proteção de Dispositivo", dados["DeviceProtection"].unique()),
    st.selectbox("Suporte Técnico", dados["TechSupport"].unique()),
    st.selectbox("TV Por Streaming", dados["StreamingTV"].unique()),
    st.selectbox("Contrato", dados["Contract"].unique()),
    st.selectbox("Faturamento Sem Papel", dados["PaperlessBilling"].unique(), index=1),
    st.selectbox("Método de Pagamento", dados["PaymentMethod"].unique(), index=1),
    st.number_input("Cobranças Mensais", min_value=0.0, step=10.0, value= 65.0),
    st.number_input("Cobranças Totais", min_value=0.0, step=100.0, value=500.0)]
    processar = st.button("Processar os Dados")
    
    #Transformação dos novos dados para previsão
    if processar and novos_dados: 
        with st.spinner("Aguarde... Carregando os Modelos"):        
            novos_dados = pd.DataFrame([novos_dados], columns=dados.columns.drop( "Churn"))
            for colunas in novos_dados.columns:
                if colunas in encoders:
                    novos_dados[colunas] = encoders[colunas].transform(novos_dados[colunas])
            novos_dados = seletor.transform(novos_dados) #Seleção de Atributos
            previsao = modelo.predict(novos_dados) # Previsão dos novos dados
            mapeamento_previsao = {"No": "Não", "Yes": "Sim"} #Tradução da Previsão
            previsao_dec = encoder_y.inverse_transform(previsao) # reversão da transformação para melhor entendimento das previsões
            previsao_prob = modelo.predict_proba(novos_dados) #Previsão em probabilidade        
            st.write(f"<div style='font-size:20px; font-weight:bold'>Previsão do Modelo: {mapeamento_previsao[previsao_dec[0]]}</div>",
                        unsafe_allow_html=True) #Visualização traduzida através do dicionário        
            
            #Visualização da previsão final
            if previsao_prob[0][0] >0.5:
                st.success(f"**A previsão de evasão para esse cliente é NÃO - Probabilidade: {previsao_prob[0][0]* 100:.2f}%**", icon="✅")
            else:
                st.error(f"**A previsão de evasão para esse cliente é SIM - Probabilidade: {previsao_prob[0][1]* 100:.2f}%**", icon="🚨")
        
        


                

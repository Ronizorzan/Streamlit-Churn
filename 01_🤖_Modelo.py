#Página Principal
import pandas as pd
import streamlit as st
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import confusion_matrix
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
    previsoes = floresta.predict(X_teste)
    confusao = confusion_matrix(y_teste, previsoes)
    cross_val = cross_val_score(modelo, X_teste, y_teste, cv=5)
    acuracia = cross_val.mean()
    


    return churn, X_treinamento, X_teste, y_treinamento, y_teste, modelo, acuracia, encoders, encoder_y, seletor, confusao



dados, X_treinamento, X_teste, y_treinamento, y_teste, modelo, acuracia, encoders, encoder_y, seletor, confusao  = load_data()

markdown = """
        <style>
        .footer {
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            padding: 20px 25px;
            border-radius: 12px;
            text-align: center;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin-top: 40px;
            color: #343a40;
            box-shadow: 0 4px 6px rgba(10,10,10,1.0);
        }
        .footer p {
            margin: 5px 0;
        }
        .footer a {
            margin: 0 10px;
            display: inline-block;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            text-decoration: none;
        }
        .footer a:hover {
            transform: translateY(-5px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        .footer img {
            height: 42px;
            width: auto;
            vertical-align: middle;
        }
        </style>
        <div class="footer">
            <p><strong>Desenvolvido por: Ronivan</strong></p>
            <a href="https://github.com/Ronizorzan" target="_blank" title="GitHub">
                <img src="https://img.icons8.com/ios-filled/50/000000/github.png" alt="GitHub">
            </a>
            <a href="https://www.linkedin.com/in/ronivan-zorzan-barbosa" target="_blank" title="LinkedIn">
                <img src="https://img.icons8.com/color/48/000000/linkedin.png" alt="LinkedIn">
            </a>
            <a href="https://share.streamlit.io/user/ronizorzan" target="_blank" title="Streamlit">
                <img src="https://images.seeklogo.com/logo-png/44/1/streamlit-logo-png_seeklogo-441815.png" alt="Streamlit Community">
            </a>
        </div>
        """


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
st.session_state["confusao"] = confusao
st.session_state["markdown"] = markdown
# Rodapé na barra lateral com as informações do desenvolvedor
with st.sidebar:
    st.markdown(markdown,
        unsafe_allow_html=True
    )
      
       


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
        
        


                

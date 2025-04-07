#Página da Explicabilidade
from interpret import set_visualize_provider, show
from interpret.provider import InlineProvider      
from interpret.glassbox import ExplainableBoostingClassifier
from lime.lime_tabular import LimeTabularExplainer
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd



st.set_page_config(page_title="Explicabilidade do Modelo", layout="wide", page_icon=":memo:")

if "modelo" not in st.session_state: #Verificação de carregamento do modelo
    st.error("O modelo não foi carregado corretamente")
else:
    with st.sidebar: #Configuração da barra lateral
        st.header("Configurações da Explicabilidade local")
        instancia = st.number_input("Selecione uma Linha para explicar:", min_value=1, max_value=len(st.session_state["X_teste"])) #Número de Instâncias
        features = st.number_input("Insira o número de Características para exibir:", min_value=1, max_value=10, value=5) #Número de características
        processar = st.button("Mostrar Explicações")
    if processar and instancia:
        X_treinamento = st.session_state["X_treinamento"]
        y_treinamento = st.session_state["y_treinamento"]
        X_teste = st.session_state["X_teste"]
        dados = st.session_state["dados"]
        modelo = st.session_state["modelo"]
        acuracia = st.session_state["acuracia"]
        encoders = st.session_state["encoders"]
        seletor = st.session_state["seletor"]
        colunas= [col for col, support in zip(dados.columns, seletor.support_) if support] #Filtragem das colunas selecionadas por "RFE" para utilização nos gráficos de explicabilidade
        col1, col2 = st.columns([3,2])

        #Explicabilidade Global
        with st.spinner("Aguarde... Carregando os Modelos"):
            with col1:
                set_visualize_provider(InlineProvider())
                ebm = ExplainableBoostingClassifier(feature_names=list(colunas), max_bins=features)
                ebm.fit(X_treinamento, y_treinamento)
                set_visualize_provider(InlineProvider())
                explanation = ebm.explain_global("Explicação Global do Modelo")
                show(explanation)
                st.write("Explicabilidade Global")
                st.markdown("**Descrição:** O gráfico abaixo mostra a importância dos atributos de forma generalizada")
                st.plotly_chart(explanation.visualize(), use_container_width=True)

            #Explicabilidade Local
            with col2:    
                st.write(f"Acurácia Aproximada do Modelo: {acuracia*100:.2f}%")
                st.write("Explicabilidade Local")
                st.markdown("**Descrição:** O gráfico abaixo mostra a contribuição dos atributos para a classificação do cliente escolhido")
                previsor = lambda x: modelo.predict_proba(x).astype(float)
                expl = LimeTabularExplainer(X_teste, class_names=["Não", "Sim"], feature_names=list(colunas))
                instancia_selecionada = X_teste[instancia,:]
                explainer = expl.explain_instance(instancia_selecionada, previsor, num_features=features)
                components.html(explainer.as_html(), height=500,width=500, scrolling=True)
                instancia_selecionada = pd.DataFrame(instancia_selecionada)
                              
        


    
       
    
    
 
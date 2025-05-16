#Página da Explicabilidade
import shap
import streamlit as st
import plotly.express as px
import pandas as pd
from numpy import reshape


#Configuração do Layout da página
st.set_page_config(page_title="Explicabilidade do Modelo", layout="wide", page_icon=":memo:")

st.title("Previsão de Churn de Clientes")

                           
#Função para criação da Explicabilidade Global
def explicabilidade_global(modelo, colunas, features):
    """Esta função cria um gráfico de explicabilidade global através
    de um modelo de RandomForest.Ela foi desenvolvida com espaço para
    futura melhorias. O gráfico é customizado de forma á torná-lo altamente
    agradável e informativo, bem como tornar possível sua exibição lado a lado
    com outros gráficos mantendo a consistência de suas cores e informações. """
    importancias = modelo.feature_importances_  
    importancias_df = pd.DataFrame({
        "Atributo": colunas,
        "Importância": importancias.round(2)
    })

    # Ordenar os atributos por importância
    importancias_df = importancias_df.sort_values(by="Importância", ascending=False).head(features)   
    importancias_df.sort_values("Importância", ascending=True, inplace=True) 

    # Criar o gráfico de barras com Plotly Express
    fig = px.bar(
        data_frame=importancias_df,
        x="Importância",
        y="Atributo",
        color="Importância",
        color_continuous_scale="Greens",
        orientation="h",  # Gráfico horizontal
        labels={"Importância": "Importância", "Atributo": "Atributo"},
        title="Importância Global dos Atributos"
    )

    # Ajustar o layout para alinhamento elegante
    fig.update_layout(
        title=dict(
            font=dict(size=20),
            x=0.25  # Centralizar título
        ),
        xaxis=dict(title="Contribuição", title_font=dict(size=18), tickfont=dict(size=14)),
        yaxis=dict(title="Atributos", title_font=dict(size=18), tickfont=dict(size=14), automargin=True),
        template="plotly_white",  # Layout clean e elegante
        coloraxis_colorbar=dict(
            title="Importância",
            thickness=10,
            lenmode="fraction",
            len=0.5,
            yanchor="middle"))

    # Refinar as barras para visualização nítida
    fig.update_traces(
        texttemplate="%{x:.2f}",  # Exibir valores bem-formatados nas barras
        textposition="inside",   # Posicionar os textos dentro das barras
        marker=dict(line=dict(color="black", width=1.5))  # Adicionar bordas às barras
    )
    fig.add_vline(x=0, line=dict(color="black", width=2.0, dash="solid"))

    return fig


if "modelo" not in st.session_state: #Verificação de carregamento do modelo
    st.error("O modelo não foi carregado corretamente")
else:    
    with st.sidebar: #Configuração da barra lateral
        markdown = st.session_state["markdown"]
        st.subheader(":green[Configurações das Explicabilidades]", divider="green", help="Use as configurações abaixo para\
                     \n mudar as configurações das explicabilidades")
        with st.expander("Clique para configurar a explicabilidade", expanded=True):
            instancia = st.number_input("Selecione um cliente para gerar explicação:", min_value=1, value=23,
                                         max_value=len(st.session_state["X_teste"]), help="Selecione um cliente para \
                                            \n exibir na explicabilidade local") #Número do cliente para exibir na explicabilidade local
            features = st.slider("Insira o número de Características que gostaria de exibir:", min_value=3, max_value=10, value=5, help="Use esse controle deslizante para selecionar o número\
                                 \n de atributos mais relevantes á serem exibidos" ) #Número de características para exibir nos gráficos
        processar = st.button("Mostrar Explicações")
        st.markdown(markdown, unsafe_allow_html=True)
if processar and instancia:    
        X_treinamento = st.session_state["X_treinamento"]
        y_treinamento = st.session_state["y_treinamento"]
        X_teste = st.session_state["X_teste"]
        y_teste = st.session_state["y_teste"]
        dados = st.session_state["dados"]
        modelo = st.session_state["modelo"]
        acuracia = st.session_state["acuracia"]
        encoders = st.session_state["encoders"]
        seletor = st.session_state["seletor"]        
        colunas= [col for col, support in zip(dados.columns, seletor.support_) if support] #Filtragem das colunas selecionadas por "RFE" para utilização nos gráficos de explicabilidade        
        explanation = explicabilidade_global(modelo, colunas, features) 
                                             

        #Exibição da Explicabilidade Global
        with st.spinner("Aguarde... Carregando os Modelos"):
            col1, col2 = st.columns([0.55,0.45], gap="large")
            with col1:                
                st.header("Explicabilidade Global", divider="green", help="Os gráficos são interativos e fornecem várias funcionalidades\
                          \n como zoom, tela cheia, download, filtragem, entre outros")                                            
                st.plotly_chart(explanation, use_container_width=True)                
                st.write("<div style='font-size:18px; font-weight:bold'>Descubra os atributos com maior influência\
                         sobre as decisões do modelo. Observe que, de um modo geral, o modelo tende a utilizar com mais frequência\
                         os atributos mais importantes em suas previsões. Esses atributos exercem grande impacto sobre as intenções dos clientes\
                         em relação à empresa. Isso significa que os valores desses atributos podem ser essencias para determinar\
                         se esses clientes abandonam a empresa ou não. O gráfico destaca que atributos como cobranças mensais e totais,\
                         tempo de relacionamento do cliente com a empresa e tipo de contrato podem refletir o comprometimento e a lealdade \
                         do cliente com a empresa, portanto podem ser considerados fatores determinantes para permanência do cliente na empresa.", unsafe_allow_html=True)

            #A explicabilidade Local será implementada diretamente para maior dinamismo
            with col2:                    
                st.header("Explicabilidade Local", divider="green", help="Os gráficos são interativos e fornecem várias funcionalidades\
                          \n como zoom, tela cheia, download, filtragem, entre outros" )
                nova_instancia = X_teste[instancia,:] #Localização da linha para explicar em X_teste                                                                                                                                

                # Inicializando o SHAP e obtendo os valores
                explainer = shap.Explainer(modelo)
                explain = explainer(nova_instancia)
                shap_values = explain.values[:,1]  # Extraindo os valores SHAP para a instância
                
                # Cores baseadas nos valores SHAP
                colors = ["Não Abandono" if value < 0 else "Abandono" for value in shap_values]

                # Criando o DataFrame para visualização
                shap_values_df = pd.DataFrame({
                    'Atributo': colunas,
                    'Valor SHAP': shap_values.round(2),
                    'Contribuição': colors
                })
                
                #Ordenação por valor absoluto para visualização mais intuitiva
                shap_values_df = shap_values_df.reindex(shap_values_df['Valor SHAP'].abs().sort_values(ascending=False).index).head(features)
                shap_values_df.sort_values("Valor SHAP", ascending=True, inplace=True) #Ordenação do maior para o menor
                
                # Criando o gráfico com Plotly
                fig = px.bar(
                    data_frame=shap_values_df,
                    x='Valor SHAP',
                    y='Atributo', title="Contribuição dos Atributos para a Previsão",
                    color='Contribuição',  # Utilizando as cores personalizadas
                    text='Valor SHAP',  # Exibindo os valores SHAP nos gráficos
                    color_discrete_map={"Abandono": "#FF1000", "Não Abandono": "#006000"},
                    orientation='h',  # Gráfico horizontal para melhor legibilidade                    
                    labels={
                        "Valor da Contribuição": "Contribuição SHAP",
                        "Atributo": "Característica"
                    })

                # Refinando o layout
                fig.update_traces(
                    texttemplate="%{text:.2f}",  # Formatação dos valores SHAP no gráfico
                    textposition='inside',  # Exibe os valores dentro das barras
                    marker=dict(line=dict(color='black', width=1.5))  # Adiciona bordas às barras
                )
                fig.update_layout(
                    title=dict(
                        font=dict(size=20),
                        x=0.25  # Centraliza o título
                    ),
                    xaxis=dict(title="Valor SHAP", title_font=dict(size=18), tickfont=dict(size=14)),
                    yaxis=dict(title="Atributos", title_font=dict(size=18), tickfont=dict(size=14)),
                    template="plotly_white"  # Layout mais clean
                    )
                fig.add_vline(x=0, line=dict(color="black", width=2.0, dash="solid"))

                # Exibindo o gráfico no Streamlit
                st.plotly_chart(fig, use_container_width=True)

                
                #Separação do valor previsto e real para comparação
                previsao = modelo.predict(reshape(nova_instancia, (1, -1)))
                valor_original = y_teste[instancia]

                #Transformação dos dados para sua estrutura original para maior clareza
                instancia_selecionada_df = pd.DataFrame([nova_instancia], columns=colunas, index=None)
                instancia_selecionada_df = instancia_selecionada_df.loc[:, instancia_selecionada_df.columns.isin(shap_values_df["Atributo"])]
                for col in instancia_selecionada_df.columns:
                    if col in encoders:
                        instancia_selecionada_df[col] = encoders[col].inverse_transform(instancia_selecionada_df[col].astype(int))
                mapeamento_classe = {0: "Não Abandonou", 1: "Abandonou"} #Mapeamento das classes para o português
                st.write("<div style='font-size:20px; font-weight:bold'>Valores originais do Cliente</div>", unsafe_allow_html=True)                                
                st.write(instancia_selecionada_df )
                st.write(f"<div style='font-size:19px; font-weight:bold'>   Ocorrência real: {mapeamento_classe[valor_original]}\
                     ---------  Ocorrência prevista: {mapeamento_classe[int(previsao)]}</div>", unsafe_allow_html=True)                              
                if previsao==valor_original:
                    st.write("<div style='color:green; font-size:25px; font-weight:bold'>A previsão do Modelo está correta ✅</div> ", unsafe_allow_html=True)
                else:
                    st.write("<div style='color:red; font-size:25px; font-weight:bold'> A previsão do Modelo está incorreta 🚨</div> ", unsafe_allow_html=True)
#Página de Explicação das funcionalidades
import streamlit as st


st.set_page_config(page_title="Visão Geral da Aplicação", layout="wide", page_icon=":speech_balloon:")


st.title("Explicação Geral das Funções da Aplicação")


consultar = st.button("Consultar Funcionalidades das Páginas")
if consultar:
    st.markdown("**Modelo:** Carregamento do Modelo Principal")
    st.write("""Essa é a página principal que carrega o modelo e permite visualizar as previsões do modelo selecionando os dados de um cliente específico...
                As previsões são mostradas de forma absoluta e em forma de probabilidade obtidas diretamente do Modelo """)



    st.markdown("**Explicabilidade:** Página de Explicabilidade")
    st.write("""Essa página contém 2 modelos: O primeiro é um modelo Generalista que exibe a importância dos atributos e consequentemente o
            impacto que cada um exerce na escolha da classe.... O segundo é um modelo de explicação local que explica um cliente específico
            do conjunto de dados de teste... A primeira caixa de seleção permite escolher um cliente específico do conjunto de dados, e a segunda
            permite escolher o número de atributos para exibir no gráfico... Os atributos que mais inflenciaram para esse determinado cliente são escolhidos automaticamente """)


    st.markdown("**Análise:** Página de Análise Exploratória dos Dados")
    st.write("""Essa página contém dois tipos de gráfico(Gráfico de Barras e Histograma) A pimeira caixa de seleção seleciona o atributo categórico a ser exibido
            A segunda seleciona o atributo numérico... A terceira seleciona a cor do gráfico de barras... E a quarta seleciona a cor do histograma """)

    st.markdown("**Financeiro:** Página de Relatório Financeiro")
    st.write("""Essa página permite visualizar de forma dinâmica os retornos financeiros obtidos com a utilização do modelo:
            Uma matriz é carregada automaticamente com  as previsões do modelo em dados não conhecidos pelo modelo... 
            A primeira caixa de seleção permite inserir a média de gastos mensal dos clientes... 
            A segunda permite inserir o valor gasto com clientes que não evadiram mas que foram previstos como evasivos pelo modelo
            E o terceiro botão permite selecionar a porcentagem de clientes com risco de evasão que foram retidos com o uso do modelo ...
            O cálculo final contém o valor líquido obtido deduzindo-se todos os outros valores...
             """)

    st.write("""Os clientes que foram corretamente previstos como \'sem risco de evasão\' não são considerados nos cálculos financeiros,
                porém um alto número de clientes classificados corretamente eleva a eficácia e a confiabilidade do modelo """)



    st.write("Algumas métricas adicionais são exibidas com explicações e todos os cálculos são feitos baseados na matriz de confusão")


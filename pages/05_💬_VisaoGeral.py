#Página de Explicação das funcionalidades
import streamlit as st


st.set_page_config(page_title="Visão Geral da Aplicação", layout="wide", page_icon=":speech_balloon:")


st.title("Explicação Geral das Funções da Aplicação")


consultar = st.button("Consultar Funcionalidades das Páginas")
if consultar:
    st.markdown("**Modelo:** Carregamento do Modelo Principal")
    st.write("""Essa é a página principal que carrega o modelo e permite visualizar as previsões do modelo selecionando os dados de um cliente específico...
                As previsões são mostradas de forma binária e em forma de probabilidade obtidas diretamente do Modelo """)



    st.markdown("**Explicabilidade:** Página de Explicabilidade")
    st.write(""" A primeira caixa de seleção permite escolher um cliente específico do conjunto de dados para exibir
             na explicabilidade local, e a segunda permite limitar o número de atributos exibidos no gráfico...
             O primeiro gráfico exibe um gráfico de explicabilidade global, as importâncias são extraídas diretamente do modelo de Florestas Aleatórias treinado.... 
           O segundo gráfico exibe uma explicação específica para um cliente, que pode ser escolhido na caixa de seleção à esquerda.
           Diferente da explicação global que é mais estática, a explicação local é altamente dinâmica e varia consideravelmente de acordo com
           as características únicas de cada cliente. Adicionalmente, as características originais do cliente são exibidas abaixo do gráfico para um entendimento
             sem complicações. E porfim, mas não menos importante, uma comparação é gerada automaticamente, informando a ocorrência real e a 
            ocorrência prevista pelo modelo fornecendo um entendimento rápido e claro da confiança que você pode ter na previsão...""")


    st.markdown("**Análise:** Página de Análise Exploratória dos Dados")
    st.write("""Essa página tem o intuito de fornecer um entendimento básico do conjunto de dados usado no treinamento do modelo.
             Por esse motivo ela pode se tornar um pouco complexa para pessoas não técnicas.
             Essa página contém dois tipos de gráfico(Gráfico de Barras e Histograma) A primeira caixa de seleção 
             seleciona o atributo categórico a ser exibido. A segunda seleciona o atributo numérico...  """)

    st.markdown("**Financeiro:** Página de Relatório Financeiro")
    st.write("""Essa página permite visualizar de forma dinâmica os retornos financeiros obtidos com a utilização do modelo:
            Uma matriz é carregada automaticamente com  as previsões do modelo ... 
            A primeira caixa de seleção permite inserir a média de gastos mensal dos clientes... 
            A segunda permite inserir o valor gasto com clientes que não evadiram mas que foram previstos como evasivos pelo modelo
            E o terceiro botão permite selecionar a porcentagem de clientes com risco de evasão que foram retidos com o uso do modelo ...
            """)    



    st.write("""Na segunda parte algumas métricas adicionais são exibidas com explicações simples e compreensíveis do desempenho do modelo
             aproveitando-se do contexto da análise ...Finalmente alguns cálculos são gerados de forma dinâmica.
             Eles são baseados na matriz de confusão que foi gerada e destacam todos os respectivos ganhos e perdas retornados com o uso do modelo
             O cálculo final contém o valor líquido obtido deduzindo-se todos os valores gastos com campanhas e com clientes perdidos.
             """)
    
    st.write("""PS: Os clientes que foram corretamente previstos como \'sem risco de evasão\' não são
             considerados nos cálculos financeiros, por não representarem um impacto financeiro direto.
             Porém um alto número de clientes classificados corretamente eleva a eficácia e a confiabilidade do modelo """)


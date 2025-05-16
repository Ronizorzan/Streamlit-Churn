#Página de Explicação das funcionalidades
import streamlit as st


st.set_page_config(page_title="Visão Geral da Aplicação", layout="wide", page_icon=":speech_balloon:")


st.title("Explicação Geral das Funções da Aplicação")


consultar = st.button("Consultar Funcionalidades das Páginas")
markdown = st.session_state["markdown"]
st.sidebar.markdown(markdown, unsafe_allow_html=True)
if consultar:
    st.markdown("**Modelo:** Carregamento do Modelo Principal")
    st.write("""Essa é a página principal que carrega o modelo e permite visualizar as previsões do modelo selecionando os dados de um cliente específico...
                As previsões são mostradas de forma binária e em forma de probabilidade obtidas diretamente do Modelo """)

        
    st.markdown("**Análise Descritiva:** Página de Análise Descritiva ")
    st.write("""Essa página exibe dois gráficos: O primeiro representa a taxa de Evasão em cada grupo de clientes.
             O segundo gráfico representa o aumento no risco de evasão em diferentes grupos.
             Essa comparação é feita em relação ao grupo que possui a menor taxa de Evasão 
             (ex: no atributo contrato o grupo de referência é o que possui o contrato de 2 anos )
             Os atributos para análise podem ser trocados através do botão na barra lateral (à esquerda)""")
    
    st.markdown("**Impacto das evasões:** Página de Análise de Taxa de Retenção e Evasão de clientes")
    st.write("""Essa página exibe um gráfico de barras empilhadas onde a parte vermelha representa a porcentagem de clientes
             que deixaram a empresa e a parte verde representa os clientes que continuam com a empresa. 
             A variação dessas taxas está diretamente ligada à eficácia das campanhas de marketing, representada
             pelo controle deslizante na barra lateral (à esquerda). Quanto maior a eficácia das campanhas
             de marketing direcionadas, maiores serão as taxas de retenção... (o Valor padrão é 75%)
             Todas as estimativas nessa página são baseadas apenas das previsões do modelo.""")


    st.markdown("**Explicabilidade:** Página de Explicabilidade")
    st.write(""" A primeira caixa de seleção permite escolher um cliente específico do conjunto de dados para exibir
             na explicabilidade local, e a segunda permite limitar o número de atributos exibidos no gráfico...
             O primeiro gráfico exibe um gráfico de explicabilidade global, as importâncias são extraídas diretamente do modelo de Florestas Aleatórias treinado.... 
           O segundo gráfico exibe uma explicação específica para um cliente, que pode ser escolhido na caixa de seleção à esquerda.
           Diferente da explicação global que é mais estática, a explicação local é altamente dinâmica e varia consideravelmente de acordo com
           as características únicas de cada cliente. Adicionalmente, as características originais do cliente são exibidas abaixo do gráfico para um entendimento
             sem complicações. E porfim, mas não menos importante, uma comparação é gerada automaticamente, informando a ocorrência real e a 
            ocorrência prevista pelo modelo fornecendo um entendimento rápido e claro da confiança que você pode ter na previsão...""")



    st.markdown("**Financeiro:** Página de Relatório Financeiro")
    st.write("""Essa página permite visualizar de forma dinâmica os retornos financeiros obtidos com a utilização do modelo:
            Uma matriz é carregada automaticamente com  as previsões do modelo ... 
            A primeira caixa de seleção permite inserir a média de gastos mensal dos clientes... 
            A segunda permite inserir o valor gasto com clientes que não evadiram mas que foram previstos como evasivos pelo modelo
            E o terceiro botão permite selecionar a porcentagem de clientes com risco de evasão que foram retidos com o uso do modelo (o valor padrão é 90%) ...
            """)    



    st.write("""Na segunda parte algumas métricas adicionais são exibidas com explicações simples e compreensíveis do desempenho do modelo
             aproveitando-se do contexto da análise ...Finalmente alguns cálculos são gerados de forma dinâmica.
             Eles são baseados na matriz de confusão que foi gerada e destacam todos os respectivos ganhos e perdas retornados com o uso do modelo
             O cálculo final contém o valor líquido obtido deduzindo-se todos os valores gastos com campanhas e com clientes perdidos.
             """)
    
    st.write("""PS: Os clientes que foram corretamente previstos como \'sem risco de evasão\' não são
             considerados nos cálculos financeiros, por não representarem um impacto financeiro direto.
             Porém um alto número de clientes classificados corretamente eleva a eficácia e a confiabilidade do modelo """)


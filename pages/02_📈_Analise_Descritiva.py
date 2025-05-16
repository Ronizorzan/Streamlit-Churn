import streamlit as st
from functions import *


st.set_page_config(page_title="Análise Descritiva", layout="wide", page_icon=":bar_chart:")
st.header("Análises de Probabilidades", divider="green")

with st.sidebar:
    # Definir os atributos para analisar
    attributes_for_analysis = ["Contrato", "Segurança Online", "Tempo na Empresa", "Cobranças Mensais",
                                "Serviço de Internet", "Método de Pagamento"]
    atributo = st.selectbox("Escolha o atributo para analisar", attributes_for_analysis, help="Escolha abaixo um atributo\
                            \npara gerar as análises")
    calcular = st.button("Mostrar análises")
    markdown = st.session_state["markdown"]
    st.markdown(markdown, unsafe_allow_html=True)

if calcular:
        df_original = load_new_data()
        df = df_original.copy() # Trabalhar com uma cópia


        # Coluna 'Churn' e outras que não devem ser atributos de análise
        cols_to_exclude_from_attributes = ['Churn'] 
        potential_attributes = [col for col in df.columns if col not in cols_to_exclude_from_attributes]

        # Filtrar para apenas os atributos que existem no DataFrame carregado
        attributes_for_analysis = [attr for attr in attributes_for_analysis if attr in df.columns]
        if not attributes_for_analysis:
            st.error("Nenhum dos atributos especificados para análise foi encontrado no DataFrame.")
            st.stop()

        selected_attribute = atributo
    
        churn_col = 'Churn' 

        if churn_col not in df.columns:
            st.error(f"Coluna de Churn '{churn_col}' não encontrada no DataFrame. Verifique os dados carregados.")
            st.stop()


        # Verificar se o atributo selecionado é numérico para discretização
        attribute_to_analyze = selected_attribute
        is_numeric = pd.api.types.is_numeric_dtype(df[selected_attribute])

        if is_numeric:
            # Criar um nome único para a coluna discretizada
            discretized_col_name = f"{selected_attribute}_Quartiles"
            df = discretize_to_quartiles(df.copy(), selected_attribute, discretized_col_name)
            attribute_to_analyze = discretized_col_name # Usar a coluna discretizada para análise
        else:
            # Se categórico, usar diretamente, mas converter para string para consistência no groupby
            df[selected_attribute] = df[selected_attribute].astype(str)

        # Calcular o impacto da evasão
        if attribute_to_analyze in df.columns:
            results = calculate_churn_impact(df, attribute_to_analyze, churn_col)                   

        # Obter informações da categoria de referência
        reference_row = results[results['É a referência'] == True].iloc[0]
        ref_category_label = str(reference_row['Categoria']) # str() para garantir que funciona com Intervalos de Quartis
        ref_churn_rate_val = reference_row['Taxa de Evasão']

        col1, col2 = st.columns(2)

        with col1:
            st.subheader(f"{selected_attribute}: Como Afeta a Evasão de Clientes")
            fig1 = plot_churn_rate_per_category(results, selected_attribute, ref_category_label)
            st.plotly_chart(fig1, use_container_width=True)
            
            st.markdown("<hr style='border: 1px solid grey'>", unsafe_allow_html=True) # linha de separação
            total_clientes_df = pd.DataFrame(results.set_index('Categoria')['Total_Customers'].T.reset_index())
            max_value = total_clientes_df[total_clientes_df["Total_Customers"]== total_clientes_df["Total_Customers"].max()]
            min_value = total_clientes_df[total_clientes_df["Total_Customers"]== total_clientes_df["Total_Customers"].min()]
            st.markdown(f"<div style='font-size: 35px; color: #40404A'>Insights adicionais", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size: 20px; color: black'>\"{max_value['Categoria'].values[0]}\" é a Categoria com maior número de Clientes:\
                        {max_value['Total_Customers'].values[0]}", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size: 20px; color: black'>\"{min_value['Categoria'].values[0]}\" é a Categoria com menor número de Clientes:\
                        {min_value['Total_Customers'].values[0]}", unsafe_allow_html=True)
                        
            

        with col2:
            st.subheader(f"{atributo}: Elevação no risco de Evasão")
            if results[~results['É a referência']].empty:
                st.info(f"Não há outras categorias para comparar com a referência '{ref_category_label}'.")
            else:
                fig2 = plot_increase_in_churn_rate(results, selected_attribute, ref_category_label, ref_churn_rate_val)
                st.plotly_chart(fig2, use_container_width=True)
                st.markdown("<hr style='border: 1px solid grey'>", unsafe_allow_html=True) # linha de separação                
                st.markdown(f"<div style='font-size: 35px; color: #40404A'>Insights adicionais", unsafe_allow_html=True)                            
                referencia = results.loc[results["É a referência"]]                
                st.markdown(f"""<div style='font-size: 20px; color: black'>\"{referencia['Categoria'].values[0]}\" é a Categoria de referência.
                            Apenas {referencia["Taxa de Evasão"].values[0]:.2f}% dos clientes nessa categoria deixaram a empresa.
                             O total de clientes atualmente nessa categoria é {referencia["Total_Customers"].values[0]} """, unsafe_allow_html=True)
                
                                
               

    




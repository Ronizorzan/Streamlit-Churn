import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import streamlit as st
import pandas as pd



def calcular_metricas(matriz_confusao, taxa_retencao_estimada):
    VN, FP = matriz_confusao[0][0], matriz_confusao[0][1]
    FN, VP = matriz_confusao[1][0], matriz_confusao[1][1]

    total_solicitacoes = VN + FP + FN + VP
    evasao_real_original = (FN + VP) / total_solicitacoes * 100

       
    
    total_evasao_potencial = VP + FN # Número real de evasões  
    total_evasoes_previstas = VP  
    clientes_retidos_estimados = total_evasoes_previstas * taxa_retencao_estimada # Estimativa de clientes retidos com base nos VP
    
    nova_taxa_evasao_estimada = ((total_evasao_potencial - clientes_retidos_estimados ) / total_solicitacoes) * 100 # Taxa de evasão com o uso do modelo
    reducao_evasao_percentual = (clientes_retidos_estimados / total_evasao_potencial) * 100 if total_evasao_potencial > 0 else 0 # Taxa de Clientes retidos em relação ao total de clientes em risco

    return {"Taxa_Evasão_atual": round(evasao_real_original, 2), # Taxa de Evasão atualmente
            "Clientes_retidos_atual": 100 - evasao_real_original, # Taxa de Clientes retidos atualmente
            "Total_Evasões_atuais": round(total_evasao_potencial, 2), # Número total de Clientes que evadiram atualmente
            "Estimativa_clientes_retidos": int(clientes_retidos_estimados), # Estimativa de clientes retidos com o uso do Modelo
            "Nova_taxa_evasão": round(nova_taxa_evasao_estimada, 2), #Taxa de evasão estimada com o uso do Modelo
            "Nova_taxa_retencão": 100 - nova_taxa_evasao_estimada, # Taxa de retenção estimada com o uso do Modelo 
            "Reducao_evasao_perc": round(reducao_evasao_percentual, 2)} # Taxa de Clientes retidos em relação ao total de clientes em risco

        

def plot_barras_empilhadas(resultado):
# Agrupando os resultados para o gráfico
    taxas = ['Taxas atuais', 'Taxas estimadas com uso do Modelo']
    evasao_atual   = [resultado["Taxa_Evasão_atual"], resultado["Nova_taxa_evasão"]] # Taxa de evasão com e sem modelo
    clientes_retidos   = [resultado["Clientes_retidos_atual"], resultado["Nova_taxa_retencão"]] # Taxa de clientes retidos
    
    x = np.arange(len(taxas))
    width = 0.6
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Plota um gráfico de barras empilhadas com retenção e evasão de clientes com e sem modelo
    ax.bar(x, clientes_retidos, width, label='Clientes que não evadiram', color='green', bottom=evasao_atual)
    ax.bar(x, evasao_atual, width, label='Clientes que evadiram', color='red')
          
    ax.set_xticks(x)    
    ax.set_xticklabels(taxas)
    ax.set_xlabel('Estratégia', fontsize=15)
    ax.set_ylabel('Taxa (%) ', fontsize=15)
    ax.set_title('Impacto Final: Taxa de retenção e evasão de clientes ', fontsize=15)    
    ax.legend(bbox_to_anchor=(0.15,-0.02))
    plt.tight_layout()

       
    return plt.gcf()



# --- 1. Carregamento dos Dados ---
@st.cache_data # Cache para não recarregar os dados a cada interação
def load_new_data():
    data = pd.read_csv("dados_tratados.csv")    
    df = pd.DataFrame(data)
    colunas = ['Contract' ,'OnlineSecurity','tenure', 'MonthlyCharges', "Churn", "InternetService", "PaymentMethod"]    
    mapeamento_colunas = {'Contract': "Contrato", 'OnlineSecurity': "Segurança Online", 'tenure':
                    "Tempo na Empresa", 'MonthlyCharges': "Cobranças Mensais", "Churn": "Churn",
                 "InternetService": "Serviço de Internet", "PaymentMethod": "Método de Pagamento"}    
    df = df[colunas]
    df.rename(columns=mapeamento_colunas, inplace=True)
            
            
    # Garantir que Churn seja inteiro
    df['Churn'] = df["Churn"].astype("category")
    df['Churn'] = df['Churn'].cat.codes
    return df

# --- 2. Função para Discretizar em Quartis ---
def discretize_to_quartiles(df, numeric_column_name, new_column_name):
    """Discretiza uma coluna numérica em quartis."""
    sufix = ['R$' if numeric_column_name=="Cobranças Mensais" else "Meses"]
    try:
        df[new_column_name] = pd.qcut(df[numeric_column_name], q=4, duplicates='drop')
        # Formatar rótulos para melhor visualização
        df[new_column_name] = df[new_column_name].apply(lambda x: f"de {x.left:.0f} à {x.right:.0f} {sufix[0]}" if pd.notnull(x) else "N/A")
    except Exception as e:
        st.warning(f"Não foi possível discretizar '{numeric_column_name}' em 4 quartis. Pode haver poucos valores únicos. Erro: {e}")
        # Tentar com menos quartis ou tratar como categórico se falhar muito
        try:
            df[new_column_name] = pd.qcut(df[numeric_column_name], q=2, duplicates='drop')
            df[new_column_name] = df[new_column_name].apply(lambda x: f"de {x.left:.0f} à {x.right:.0f} {sufix[0]}" if pd.notnull(x) else "N/A")
            st.info(f"'{numeric_column_name}' foi discretizado em 2 faixas (mediana).")
        except:
            df[new_column_name] = df[numeric_column_name].astype(str) # Último recurso
            st.info(f"'{numeric_column_name}' será tratado como categórico devido a problemas na discretização.")
    return df

# --- 3. Função Principal de Cálculo ---
def calculate_churn_impact(df, attribute_column, churn_column='Churn'):
    """
    Calcula a taxa de evasão e o aumento percentual relativo à categoria de referência.
    Retorna um DataFrame com 'Categoria', 'Taxa de Evasão', 'Aumento na Taxa de Evasão (%)', 'É a referência'.
    """
    if df[attribute_column].isnull().any():
        st.warning(f"A coluna '{attribute_column}' possui valores nulos. Eles serão ignorados nos cálculos.")
        df_analysis = df.dropna(subset=[attribute_column])
    else:
        df_analysis = df.copy()

    # Agrupar e calcular a taxa de evasão
    agg_data = df_analysis.groupby(attribute_column, observed=True).agg(
        Total_Customers=(churn_column, 'count'),
        Churned_Customers=(churn_column, 'sum')
    ).reset_index()

    agg_data['Taxa de Evasão'] = (agg_data['Churned_Customers'] / agg_data['Total_Customers']) * 100
    agg_data = agg_data.sort_values(by='Taxa de Evasão', ascending=True).reset_index(drop=True)

    # Definir categoria de referência (menor taxa de evasão)
    if not agg_data.empty:
        reference_category = agg_data.loc[0, attribute_column]
        reference_churn_rate = agg_data.loc[0, 'Taxa de Evasão']
        agg_data['É a referência'] = agg_data[attribute_column] == reference_category
    else:
        return pd.DataFrame(columns=['Categoria', attribute_column, 'Taxa de Evasão', 'Aumento na Taxa de Evasão (%)', 'É a referência', 'Total_Customers'])


    # Calcular aumento na taxa de evasão em relação à referência
    # Evitar divisão por zero se a taxa de referência for 0
    if reference_churn_rate > 0:
        agg_data['Aumento na Taxa de Evasão (%)'] = \
            ((agg_data['Taxa de Evasão'] - reference_churn_rate) / reference_churn_rate) * 100
    else:
        # Se a taxa de referência for 0, o aumento é infinito para taxas > 0, ou 0 para taxas = 0.        
        # Aqui, vamos mostrar a diferença absoluta como fallback para o texto do gráfico.
        agg_data['Aumento na Taxa de Evasão (%)'] = agg_data['Taxa de Evasão'] - reference_churn_rate


    agg_data.rename(columns={attribute_column: 'Categoria'}, inplace=True)
    return agg_data[['Categoria', 'Taxa de Evasão', 'Aumento na Taxa de Evasão (%)', 'É a referência', 'Total_Customers']]

# --- 4. Funções de Plotagem com Plotly Express ---
def plot_churn_rate_per_category(results_df, attribute_name, reference_category):
    """Gera gráfico de barras da Taxa de Evasão por Categoria."""
    results_df = round(results_df, 2)
    maior_taxa = results_df[results_df["Taxa de Evasão"]== results_df["Taxa de Evasão"].max()]
    menor_taxa = results_df[results_df["Taxa de Evasão"]== results_df["Taxa de Evasão"].min()]
    
    fig = px.bar(results_df,
                 x='Categoria',
                 y='Taxa de Evasão',
                 text='Taxa de Evasão',
                 color='É a referência',
                 color_discrete_map={True: '#2A9D8F', False: '#E63946'},
                 title=f'''Clientes com o valor \"{maior_taxa["Categoria"].values[0]}\" para o atributo {attribute_name}
                     <br>aprensentam a Maior Taxa de Evasão: ({maior_taxa["Taxa de Evasão"].values[0]}%) ''')
    
    y_axis_title='Taxa de Evasão (%)'
    x_axis_title=f'''Clientes com o valor \"{menor_taxa["Categoria"].values[0]}\" aprensentam\
<br>a Menor Taxa de Evasão: apenas ({menor_taxa["Taxa de Evasão"].values[0]}%)'''
    
    fig.update_traces(texttemplate='%{y:.2f}%', textposition='inside')
    fig.update_layout(yaxis=dict(title=y_axis_title, title_font=dict(size=17)),
                      legend_title_text=f'Referência: {reference_category}',
                      xaxis=dict(title=x_axis_title, title_font=dict(size=17)),
                      barmode="relative")
    return fig

def plot_increase_in_churn_rate(results_df, attribute_name, reference_category, reference_churn_rate):
    """Gera gráfico de barras do Aumento na Taxa de Evasão."""
    # Excluir a categoria de referência para este gráfico, pois o aumento é 0
    results_df = round(results_df, 2)
    plot_df = results_df[~results_df['É a referência']].copy()

    max_value = results_df[results_df['Aumento na Taxa de Evasão (%)']== results_df['Aumento na Taxa de Evasão (%)'].max()]    

    if reference_churn_rate == 0:
        y_axis_title = 'Aumento Absoluto (p.p.)'
        text_template = '%{y:.2f} p.p.'
        title = f'Aumento Absoluto na Taxa de Evasão por {attribute_name}'
    else:
        y_axis_title = 'Aumento no risco de Evasão (%)'
        text_template = '%{y:.0f}%'
        title = f'''Clientes com o valor \"{max_value["Categoria"].values[0]}\" para o atributo {attribute_name} aprensentam o maior
         <br> aumento no risco de evasão em relação ao valor de referência: ({max_value["Aumento na Taxa de Evasão (%)"].values[0]}%) '''
        x_axis_title=f'O valor de Referência é: \"{reference_category}\"'

    color_marker = plot_df[ "Aumento na Taxa de Evasão (%)"].values    
    colors = np.select([color_marker > 200, color_marker > 75], ['#E63946', '#E9C46A'], default='#2A9D8F' )
    
    fig = px.bar(plot_df,
                 x='Categoria',
                 y='Aumento na Taxa de Evasão (%)',
                 text='Aumento na Taxa de Evasão (%)',
                 color_discrete_sequence=[colors],
                 title=title, 
                 orientation="v")
    fig.update_traces(texttemplate=text_template, textposition='inside')
    fig.update_layout(yaxis=dict(title=y_axis_title, title_font=dict(size=17)),
                      xaxis=dict(title=x_axis_title, title_font=dict(size=17)))
    return fig


# Carregar Dados
# Para usar um arquivo enviado pelo usuário:
# uploaded_file = st.sidebar.file_uploader("Carregue seu arquivo CSV com os dados de clientes", type="csv")
# if uploaded_file is not None:
#     df = pd.read_csv(uploaded_file)





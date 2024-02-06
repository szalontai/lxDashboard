import streamlit as st
# import requests
import pandas as pd
import plotly.express as px
import pyodbc
import tempfile 
import os 
import chardet
from datetime import datetime

# from utils.sqlconnection import SqlConnection
# from utils.queryfetchtype_enum import QueryFetchType

## Parametros iniciais

st.set_page_config(layout='wide')

#params = st.query_params.to_dict()
params = st.query_params.get_all('server')

print(params)
st.subheader(params)

print(params.keys()) 

print(params.values())

@st.cache_resource
def init_connection():


    # baseConnString=(    
    #     "DRIVER="
    #     + st.secrets["driver"]
    #     +";SERVER="
    #     + st.secrets["server"]
    #     + ","
    #     + st.secrets["port"]
    #     + ";DATABASE="
    #     + st.secrets["database"]
    #     + ";ENCRYPT=no;"
    #     + ";UID="
    #     + st.secrets["username"]
    #     + ";PWD="
    #     + st.secrets["password"]
    # )

    baseConnString=(    
        "DRIVER={ODBC Driver 18 for SQL Server}"
        +";SERVER="
        + params['server']
        + ","
        + params["port"]
        + ";DATABASE="
        + params["database"]
        + ";ENCRYPT=no;"
        + ";UID="
        + params["username"]
        + ";PWD="
        + params["password"]
    )

    # return baseConnString
  
    return  pyodbc.connect(baseConnString)


def format_number(value,pref=''):
    for unit in ['','mil']:
        if value<1000:
            return f'{pref} {value:.2f} {unit}'
        value/=1000
        return f'{pref} {value:.2f} milhões'

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
# @st.cache_data(ttl=600)
# def run_query(query):
#     with conn.cursor() as cur:
#         cur.execute(query)
#         return cur.fetchall()

# def run_query01(query):
#     data, columns = SqlConnection().execute_query(query, QueryFetchType.ALL, "")

#     return data

#conn = init_connection()

#print(conn)


st.title("Dashboard de vendas - LINX")
st.subheader("Teste 1")


st.sidebar.title('Filtros')


# st.subheader(params[0])


SQL = """
select
v.gerente,p.grupo_produto,f.regiao,vp.entrega,valor_entregue,qtde_entregue
--,vp.*
from vendas_produto vp
inner join vendas v on vp.pedido = v.pedido
inner join produtos p on vp.produto = p.produto
inner join filiais f on v.filial = f.filial
where entrega>='20200101'
"""
#dados = pd.read_sql(SQL, conn)


# diretorio_pai = ""
# with tempfile.TemporaryDirectory() as temp_dir:
#     # Obtém o caminho do diretório temporário
#     caminho_temporario = temp_dir

#     # Obtém o diretório pai
#     diretorio_pai = os.path.dirname(caminho_temporario)

# caminho_arquivo_csv = os.path.join(diretorio_pai, 'Vendas.csv')

# st.subheader(diretorio_pai)

# Verifica se o arquivo de vendas existe
if True : 
    #not os.path.exists(caminho_arquivo_csv):
    st.subheader("Arquivo Vendas.csv não localizado ! ")
else:     
    
    # dados = pd.read_csv(caminho_arquivo_csv,   encoding='ISO-8859-1')

    # Verifica se tem registros no arquivo
    if dados.empty :
        st.subheader("Sem dados para o período informado ! ")
    else:

        # Montagem das datas inicial e final do filtro
        starDate = pd.to_datetime(dados['entrega'],format='%d/%m/%Y').min()
        endDate = pd.to_datetime(dados['entrega'],format='%d/%m/%Y').max()

        dateI = pd.to_datetime(st.sidebar.date_input("Data Inicial", starDate, format="DD/MM/YYYY"))
        dateF = pd.to_datetime(st.sidebar.date_input("Data Final",endDate, format="DD/MM/YYYY"))

        dados['entrega'] = pd.to_datetime(dados['entrega'],format='%d/%m/%Y')

        # Filtro por datas
        dados= dados[(dados["entrega"]>=dateI ) & (dados["entrega"]<=dateF)].copy()

        filtro_regiao = st.sidebar.multiselect('Região',dados['regiao'].unique())
        filtro_gerente = st.sidebar.multiselect('Gerente',dados['gerente'].unique())
        filtro_grupo = st.sidebar.multiselect('Grupo Produto',dados['grupo_produto'].unique())

        # dateI = pd.to_datetime(st.sidebar.date_input("Data Inicial",starDate))


        # Filtro por região
        if filtro_regiao:
            dados = dados[dados['regiao'].isin(filtro_regiao)]

        # Filtro por gerente
        if filtro_gerente:
            dados = dados[dados['gerente'].isin(filtro_gerente)]

        # Filtro por grupo
        if filtro_grupo:
            dados = dados[dados['grupo_produto'].isin(filtro_grupo)]

        ### Tabelas 

        ### Tabelas - Receitas
        receita_mensal = dados.set_index('entrega').groupby(pd.Grouper(freq='M'))['valor_entregue'].sum().reset_index()
        receita_mensal['Ano'] = receita_mensal['entrega'].dt.year
        receita_mensal['Mes'] = receita_mensal['entrega'].dt.month_name()
        receita_grupo = dados.groupby('grupo_produto')[['valor_entregue']].sum().sort_values('valor_entregue',ascending=False)
        receita_regiao = dados.groupby('regiao')[['valor_entregue']].sum().sort_values('valor_entregue',ascending=False)

        ### Tabelas - Gerentes
        gerentes = pd.DataFrame(dados.groupby('gerente')['valor_entregue'].agg(['sum','count']))

        ### Tabelas - Grupos
        grupos = pd.DataFrame(dados.groupby('grupo_produto')['valor_entregue'].agg(['sum','count']))


        ### Graficos
        graf_receita_mensal = px.line(receita_mensal,
                                    x='Mes',
                                    y = 'valor_entregue',
                                    markers=True,
                                    range_y=(0,receita_mensal.max()),
                                    color='Ano',
                                    line_dash='Ano',
                                    title='Venda Mensal '
                                    )
        graf_receita_mensal.update_layout(yaxis_title = "Venda")

        # graf_receita_grupo = px.bar(receita_grupo.head(),
        #                             x='grupo_produto',
        #                             y = 'valor_entregue',
        #                             text_auto=True,
        #                             title='Top Grupos (Vendas) '
        #                             )

        graf_receita_grupo = px.bar(receita_grupo,
                                    text_auto=True,
                                    title='Vendas por Grupo de Produto'
                                    )
        graf_receita_grupo.update_layout(yaxis_title = "Venda")
        graf_receita_grupo.update_layout(xaxis_title = "Grupo")

        graf_receita_regiao = px.pie(dados,
                                    values='valor_entregue',
                                    names='regiao',
                                    hole=0.5,
                                    title="% de Vendas por região"
                                    )
        graf_receita_regiao.update_traces(text=dados['regiao'])


        ## Tabs
        tab1,tab2,tab3 = st.tabs(['Vendas','Quantidades','Vendedores'])

        ## Colunas

        with tab1 : 

            col1,col2,col3 = st.columns(3)

            with col1:
                # date1 = pd.to_datetime(st.date_input("Data Inicial",starDate))
                st.subheader("Período")
                # st.metric('Valor Entregue',format_number(dados['valor_entregue'].sum(),"R$"))
                st.plotly_chart(graf_receita_mensal,use_container_width=True)
                # st.plotly_chart(graf_receita_regiao,use_container_width=True)


                # st.markdown('#### Gains/Losses')

                # first_state_name = 'Nome'
                # first_state_population = '100.00'
                # first_state_delta = '-1.00'
                # st.metric(label=first_state_name, value=first_state_population, delta=first_state_delta)


            with col2:
                st.subheader("Grupo")
                # date2 = pd.to_datetime(st.date_input("Data Final",endDate))
                # st.metric('Quantidade Entregue',format_number(dados['qtde_entregue'].sum()))
                st.plotly_chart(graf_receita_grupo,use_container_width=True)

            with col3:
                st.subheader("Região")
                # date2 = pd.to_datetime(st.date_input("Data Final",endDate))
                # st.metric('Quantidade Entregue',format_number(dados['qtde_entregue'].sum()))
                st.plotly_chart(graf_receita_regiao,use_container_width=True)

        with tab2 : 
            col1,col2 = st.columns(2)

            with col1:
                st.metric('Valor Entregue',format_number(dados['valor_entregue'].sum(),"R$"))
            with col2:
                st.metric('Quantidade Entregue',format_number(dados['qtde_entregue'].sum()))

        with tab3 : 

            qtde_gerente = st.number_input('Quantidade de Gerentes',2,10,5)
            col1,col2 = st.columns(2)

            with col1:
                st.metric('Valor Entregue',format_number(dados['valor_entregue'].sum(),"R$"))
                graf_receita_gerentes = px.bar(gerentes[['sum']].sort_values('sum',ascending=False).head(qtde_gerente),
                                            x='sum',
                                            y=gerentes[['sum']].sort_values('sum',ascending=False).head(qtde_gerente).index,
                                            text_auto=True,
                                            title=f'Top {qtde_gerente} gerentes (venda)')
                st.plotly_chart(graf_receita_gerentes,use_container_width=True)

            with col2:
                st.metric('Quantidade Entregue',format_number(dados['qtde_entregue'].sum()))
                graf_qtde_gerentes = px.bar(gerentes[['count']].sort_values('count',ascending=False).head(qtde_gerente),
                                            x='count',
                                            y=gerentes[['count']].sort_values('count',ascending=False).head(qtde_gerente).index,
                                            text_auto=True,
                                            title=f'Top {qtde_gerente} gerentes (Quantidade)')
                st.plotly_chart(graf_qtde_gerentes,use_container_width=True)

    # st.dataframe(dados)


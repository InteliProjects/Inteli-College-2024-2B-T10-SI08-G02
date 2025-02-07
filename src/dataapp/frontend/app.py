# Importar Dependências
import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from datetime import datetime
from dotenv import load_dotenv
import os
import json
from flask_login import login_user

############################################################################################################
######################################## FUNÇÃO DE AUTENTICAÇÃO ############################################
############################################################################################################

# Carregar .env
load_dotenv()

# Importar credenciais do JSON
auth_config_str = os.getenv("STREAMLIT_AUTH")
auth_config = []
if auth_config_str:
    try:
        auth_config = json.loads(auth_config_str)
    except json.JSONDecodeError as e:
        st.error(f"Erro ao carregar as configurações de autenticação: {e}")

# Criando um dicionário de credenciais
credentials = {user['username']: user for user in auth_config}

# Função para autenticar o usuário
def authenticate_user(username, password):
    user_data = credentials.get(username)
    if user_data:
        return user_data.get("password") == password
    return False
    
def main():
    st.set_page_config(page_title="Dashboard", layout="wide")

    if 'username' not in st.session_state:
        with st.form("login_form"):
            username = st.text_input("Usuário")
            password = st.text_input("Senha", type="password")
            login_button = st.form_submit_button("Entrar")

        if login_button:
            if authenticate_user(username, password):
                st.session_state['username'] = username
                st.success("Login realizado com sucesso!")
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos.")
    else:
        username = st.session_state['username']
        user_data = credentials.get(username, {})
        st.sidebar.write(f"Bem-vindo, {user_data.get('username', username)}!")

if __name__ == "__main__":
    main()

############################################################################################################
######################################## CARREGAR DADOS DA API #############################################
############################################################################################################

# Função para buscar dados da API
@st.cache_data
def fetch_data_from_api(url, params=None):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if "data" in data:
            return pd.DataFrame(data["data"])
        else:
            st.error("Resposta inesperada da API.")
            return pd.DataFrame()
    except requests.exceptions.RequestException as e:
        st.error(f"Erro de conexão com a API: {e}")
        return pd.DataFrame()

# Exemplo de chamada
url_example = "http://127.0.0.1:5000/get-resumo-diario-movimentacoes"
data_resumo = fetch_data_from_api(url_example)


# CARREGAR DADOS DA API: DATA_MOV_QTDE_SAIDA
@st.cache_data
def fetch_data_mov_qtde_saida(start_date=None, end_date=None, min_output=None):
    try:
        url = "http://127.0.0.1:5000/get-data-mov-qtde-saida"
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "min_output": min_output
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Erro ao buscar dados da API: {e}")

        return pd.DataFrame()
    
# CARREGAR DADOS DA API: MATERIAIS_MAIS_REQUISITADOS
@st.cache_data
def fetch_most_requested_materials(produto=None, min_quantidade=None):
    try:
        params = {}
        if produto:
            params['produto'] = produto
        if min_quantidade is not None:
            params['min_quantidade'] = min_quantidade

        url = "http://127.0.0.1:5000/get-materiais-mais-requisitados"
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if "data" in data:
            return pd.DataFrame(data["data"])
        else:
            st.error("Resposta inesperada da API.")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Erro ao buscar dados da API: {e}")
        return pd.DataFrame()
    
# CARREGAR DADOS DA API: GET_CONSUMO_MATERIAL_TEMPO
@st.cache_data
def fetch_material_consumption_over_time(start_date=None, end_date=None):
    try:
        url = "http://127.0.0.1:5000/get-consumo-material-tempo"
        params = {
            'start_date': start_date.strftime('%Y-%m-%d') if start_date else None,
            'end_date': end_date.strftime('%Y-%m-%d') if end_date else None
        }
        # Remove parâmetros que são None
        params = {k: v for k, v in params.items() if v is not None}
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if "data" in data:
            return pd.DataFrame(data["data"])
        else:
            st.error("Resposta inesperada da API.")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Erro ao buscar dados da API: {e}")
        return pd.DataFrame()
    
# CARREGAR DADOS DA API: HISTORICO_QTDE_SAIDA
@st.cache_data
def fetch_all_data():
    try:
        url = "http://127.0.0.1:5000/get-historico-qtde-saida"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if "data" in data:
            return pd.DataFrame(data["data"])
        else:
            st.error("Unexpected response from API.")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching data from API: {e}")
        return pd.DataFrame()
    
data = fetch_all_data()
historico_options = ['All'] + sorted(data['historico'].unique().tolist()) if not data.empty else []

# CARREGAR DADOS DA API: FREQUENCIA_HISTORICO
@st.cache_data
def fetch_frequency_history(description=None, min_frequency=None):
    try:
        params = {
            'description': description,
            'min_frequency': min_frequency
        }
        url = "http://127.0.0.1:5000/get-frequencia-historico"
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if "data" in data:
            return pd.DataFrame(data["data"])
        else:
            st.error("Resposta inesperada da API.")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Erro ao buscar dados da API: {e}")
        return pd.DataFrame()
    

# CARREGAR DADOS DA API: VW_MATERIAIS_RES75
@st.cache_data
def fetch_vw_materiais_res75():
    try:
        url = "http://127.0.0.1:5000/get-materiais-res75"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if "data" in data:
            return pd.DataFrame(data["data"])
        else:
            st.error("Resposta inesperada da API.")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Erro ao buscar dados da API: {e}")
        return pd.DataFrame()

        
############################################################################################################
################################## CÓDIGO PARA A INTERFACE DO USUÁRIO ######################################
############################################################################################################

if 'username' in st.session_state:

    tabs = st.tabs(["Visão Geral", "Tabela Consumo 2019 - 2024", "Tabela REQ_MATERIAIS", "Tabela RES 75", "Infográfico"])

# VISÃO GERAL
    with tabs[0]:
        st.title("Visão Geral")
        st.write("Aqui você encontra uma visão geral dos dados.")

        st.write(fetch_frequency_history())

    with tabs[1]:
        st.title("Tabela Consumo 2019 - 2024")
        st.write("Aqui você encontra uma tabela com o consumo de materiais de 2019 a 2024.")

        
        # Gráfico Rosquinha: Frequência de Saída por Histórico
        st.subheader("Quantidade de Saída por Histórico")
        df_qsh = fetch_frequency_history()
        if not df_qsh.empty:
            fig_donut = px.pie(df_qsh, values='frequency', names='description',
                               title="Quantidade de Saída por Histórico")
            st.plotly_chart(fig_donut, use_container_width=True)
        else:
            st.write("No data available for the selected filters.")

        # Carregar dados da API
        df_consumo = fetch_material_consumption_over_time()

        if not df_consumo.empty:
            # Converter a coluna 'movement_date' para datetime para extrair o ano
            df_consumo['year'] = pd.to_datetime(df_consumo['movement_date']).dt.year

            # Criar dropdown para seleção do ano
            anos_disponiveis = sorted(df_consumo['year'].unique())
            ano_selecionado = st.selectbox("Selecione o ano:", anos_disponiveis)

            # Filtrar dados para o ano selecionado
            df_filtrado = df_consumo[df_consumo['year'] == ano_selecionado]

            # Tabela de dados
            st.subheader(f"Dados de Consumo em {ano_selecionado}")
            st.dataframe(df_filtrado)

            # Gráfico de linha: Consumo de Materiais ao Longo do Tempo
            st.subheader(f"Consumo de Materiais em {ano_selecionado}")
            fig_line = px.line(df_filtrado, x='movement_date', y='total_consumed',
                               title=f"Consumo Total de Materiais em {ano_selecionado}")
            fig_line.update_layout(xaxis_title="Data", yaxis_title="Quantidade Total Consumida")
            st.plotly_chart(fig_line, use_container_width=True)

        else:
            st.error("Não foi possível carregar os dados de consumo de materiais.")

    with tabs[2]:
        st.title("Tabela REQ_MATERIAIS")
        st.write("Aqui você encontra uma tabela com os materiais mais requisitados.")
        st.write(fetch_most_requested_materials())

        # GRÁFICO: MATERIAIS MAIS REQUISITADOS (apenas p gráfico geral, sem filtros)
        st.subheader("Materiais Mais Requisitados")
        df = fetch_most_requested_materials()
        if not df.empty:
            fig = px.bar(df, x='produto', y='quantidade', title="Materiais Mais Requisitados")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("No data available for the selected filters.")

        st.write(fetch_data_mov_qtde_saida())
        start_date = st.date_input("Data inicial")
        end_date = st.date_input("Data final")
        min_output = st.number_input("Quantidade mínima de saída", min_value=0.0, step=0.1)
        
        # Botão para buscar dados
        if st.button("Buscar dados"):
            df = fetch_data_mov_qtde_saida(
                start_date=start_date.strftime("%Y-%m-%d") if start_date else None,
                end_date=end_date.strftime("%Y-%m-%d") if end_date else None,
                min_output=min_output if min_output > 0 else None
            )
            
            if not df.empty:
                st.write("Dados obtidos:")
                st.dataframe(df)
                
                # Crie um gráfico de linha
                fig = px.line(df, x='movement_date', y='total_output', 
                              title="Quantidade de Saída por Data",
                              labels={'movement_date': 'Data', 'total_output': 'Quantidade de Saída'})
                st.plotly_chart(fig)
            else:
                st.write("Nenhum dado encontrado para os filtros selecionados.")

    with tabs[3]:
        st.title("Tabela RES 75")
        st.write("Aqui você encontra uma tabela com a média de tempo de requisição por produto.")
        st.write(fetch_vw_materiais_res75())

        # Gráfico: Produtos em Estoque - Da maior para menor quantidade
        st.subheader("Produtos em Estoque")
        df = fetch_vw_materiais_res75()
        if not df.empty:
            df['descricao'] = df['descricao'].apply(lambda x: x.split()[0])  # Mostrar apenas a primeira palavra da descrição
            df = df.sort_values(by='qtde_estoque', ascending=False)  # Ordenar por quantidade em estoque em ordem decrescente
            fig = px.bar(df, x='descricao', y='qtde_estoque', title="Produtos em Estoque (Ordem Decrescente)")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("No data available for the selected filters.")

    with tabs[4]:
        st.image("https://res.cloudinary.com/dajxsyf98/image/upload/v1733816939/infografico_gptm_pmjev1.png")
        

import streamlit as st
import requests 
from deep_translator import GoogleTranslator
import json

@st.cache_resource
def busca(url, headers):
    try:
        resposta = requests.get(url=url, headers=headers)
        if resposta.status_code == 403:
            st.error(f"Erro 403: Acesso proibido. Cabeçalhos: {resposta.headers}")
            return None
        dados = resposta.json()
        return dados
    except requests.exceptions.RequestException as e:
        st.error(f"Erro na requisição: {e}")
        return None

@st.cache_resource
def carregar_traducoes():
    with open("Clash_Royale_API/traducao_cartas.json", "r", encoding="utf-8") as f:
        return json.load(f)

# --- Função para traduzir nome da carta ---
def traduzir_carta(nome, traducoes):
    return traducoes.get(nome, nome)

def cartas():
    
    API_KEY = st.secrets["API"]["API_KEY"]
    
    url = "https://api.clashroyale.com/v1/cards"

    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    dados = busca(url=url,headers=headers)

    traducoes = carregar_traducoes()

    
    for cartas in dados['items']:
        
        
        with st.container(border=1):
            col1 , col2 ,col3 =st.columns(3)
            
            with col1:
                st.markdown(f"## {traduzir_carta(cartas['name'], traducoes)} :")
                
                #st.markdown(f"#### Custo de exilir : :violet[{cartas['elixirCost']}]")
                
                st.write(cartas['rarity'].capitalize())
                
                st.write(cartas['maxLevel'])
                
            with col2:
                st.image(cartas['iconUrls']['medium'])
                
            with col3:
                if 'evolutionMedium' in cartas['iconUrls']:
                    st.image(cartas['iconUrls']['evolutionMedium'])


st.html("""
        
        <h1 align="center">
        <font size = 7>
            Clash Royale API : 
        </font>
        </h1>
        
        """)

with st.sidebar:

    escolha =st.selectbox("Escolha uma função :",("Cartas"))

if escolha=="Cartas":
    cartas()










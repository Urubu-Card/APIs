import streamlit as st
import requests




@st.cache_resource
def busca(url):

    try:
        resposta = requests.get(url=url)
        dados = resposta.json()
        return dados
    
    except requests.exceptions.RequestException: 
        return None
import streamlit as st
import requests



def busca(url:str ):
    
    try:
        resposta = requests.get(url)
        
        return resposta.json()
    
    except requests.exceptions.RequestException:
        return None
    
    
    
url_base="https://genshin.jmp.blue/characters/"

perso_busca = busca(url_base)


lista_perso = [personagens.capitalize() for personagens in perso_busca]


escolha_perso = st.selectbox("Teste: ",lista_perso)

personagem = escolha_perso.lower()

url_perso = f"{url_base}{personagem}"

dados = busca(url_perso)

st.write(dados)
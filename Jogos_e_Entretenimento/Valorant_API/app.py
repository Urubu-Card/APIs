import streamlit as st
import requests
import os 

st.set_page_config(layout="wide")

@st.cache_resource
def busca(url):

    try:
        resposta = requests.get(url=url)
        dados = resposta.json()
        return dados
    
    except requests.exceptions.RequestException: 
        return None

def agentes():

    url_agentes="https://valorant-api.com/v1/agents?language=pt-BR&isPlayableCharacter=True"

    dados= busca(url=url_agentes)

    for personagem in dados['data']:

        background=personagem['background']
        corpotodo=personagem['fullPortraitV2']
        container_id = f"personagem-{personagem['uuid']}"
        
        
        col_texto, col_imagem = st.columns([1, 1])


        with col_texto:
            st.html(f'''<h2 style="text-align: center;font-size: 45px;">{personagem['displayName']} : </h2>''')
            st.markdown(f"### **{personagem['description']}**")
            
            
            colimg , colname = st.columns([1,4])
            
            with colimg:
                st.image(personagem['role']['displayIcon'],width=100)
                
            with colname:
                st.markdown(f"## **{personagem['role']['displayName']}** :" )
                st.markdown(f" {personagem['role']['description']}" )
                
            st.divider()  
            st.html('''<h2 style="text-align: center;font-size: 45px; margin-top: -25px;">Habilidades : </h2>''')
            colhab1 , colhab2 , colgranada, colult = st.columns([1,1,1,1])
            
            def modelo(habilidade):
                
                st.image(habilidade['displayIcon'])
                st.markdown(f"##### {habilidade['displayName']}")
                
            for habilidade in personagem['abilities']:
                
                if habilidade['slot'] == 'Ability1':
                    with colhab1:
                        modelo(habilidade)    
                
                if habilidade['slot'] == 'Ability2':
                    with colhab2:
                        modelo(habilidade)          
                
                if habilidade['slot'] == 'Grenade':
                    with colgranada:
                        modelo(habilidade)

                if habilidade['slot'] == 'Ultimate':
                    with colult:
                        modelo(habilidade)          

        with col_imagem:
            st.html(f"""
            <style>
                /* O container principal */
                #{container_id} {{
                    position: relative; 
                    width: 100%; 
                    max-width: 700px;
                    height: 800px; 
                    margin: auto; 
                    overflow: hidden; 
                }}

                /* O background (fundo) */
                #{container_id}::before {{
                    content: '';
                    position: absolute;
                    inset: 0;
                    z-index: 1; 

                    background-image: url('{background}'); 
                    background-size: cover;
                    background-position: center;

                    /* 1. Estado inicial: SEM blur */
                    filter: blur(0px); 
                    
                    /* 2. Transição suave para o blur */
                    transition: filter 0.3s ease;
                }}

                /* A imagem do personagem (frente) */
                #{container_id} .img-personagem {{
                    position: absolute; 
                    top: 0; left: 0;
                    width: 100%; height: 100%;
                    object-fit: contain;
                    z-index: 2; 

                    /* 3. Estado inicial: SEM zoom */
                    transform: scale(1.0);
                    
                    /* 4. Transição suave para o zoom */
                    transition: transform 0.3s ease; 
                }}

                /* 5. QUANDO O MOUSE PASSAR NO CONTAINER... */

                /* ...aplica o blur no fundo (::before) */
                #{container_id}:hover::before {{
                    filter: blur(5px);
                }}

                /* ...e aplica o zoom na imagem (.img-personagem) */
                #{container_id}:hover .img-personagem {{
                    transform: scale(1.1);
                }}
            </style>

            <div id="{container_id}">
                <img src="{corpotodo}" class="img-personagem"
            </div>
            """)
        st.divider()
        
with st.sidebar:
    
    escolha = st.selectbox("Escolha uma função",("Agentes","Armas"))
    
if escolha      ==  "Agentes":
    agentes()
    
elif escolha    == "Armas":
    st.warning("⚠️ Área em Desenvolvimento")

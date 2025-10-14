import streamlit as st                  
import requests                                
from streamlit_theme import st_theme    

#*  Blibiotecas utilizadas : 

st.set_page_config(page_title="R&M API",page_icon="icone_light.png",layout="wide")


def session_state():
    """
*   Define os Sessions States da paginas o que faz a pagina não quebrar com dois ou tres cliques e salvar dados* 
    """
    if 'next_url' not in st.session_state:
        st.session_state['next_url'] = None
        
    if 'current_data' not in st.session_state:
        st.session_state['current_data'] = []
        
    if 'dados' not in st.session_state:
        st.session_state['dados'] = None


@st.cache_resource
def busca(url):
    """
*   Faz a busca simples indo a busca da url entregando a resposta em JSON  *
    """
    
    resposta = requests.get(url=url)
    
    dados = resposta.json()
    
    return dados


def dizer_atributos(personagem,container_coluna):
    """    
*---    Diz o : nome, status(Vivo,Morto ou Desconhecido),gênero(Masculino,Feminino,Sem Gênero ou Desconhecido) junto com a foto do personagem   ---*
    """
    
    with container_coluna:
    
        with st.container(border=1):
            
                    col1 , col2 = st.columns([2,1])
                    
                    
                    with col1:
                        
                        st.subheader(f"{personagem['name']} : ")
                        
                        st.markdown("Status : ")
                        
                        if personagem['status'] =='Alive':
                            st.markdown("🟢 **Vivo**")
                            
                        elif personagem['status'] =='Dead':
                            st.markdown("🔴 **Morto**")
                        
                        else:
                            st.markdown("❓ **Desconhecido** ")
                        
                        
                        st.markdown("Gênero : ")
                        
                        genero_perso = personagem['gender']
                        
                        if genero_perso == 'Male':
                            st.markdown("🚹 **Masculino** ")
                            
                        elif genero_perso =='Female':
                            st.markdown("🚺 **Feminino**")
                            
                        elif genero_perso =='Genderless':
                            st.markdown("❌ **Sem género** ")
                        
                        else:
                            st.subheader("❓ **Desconhecido** ")
                        
                        with st.expander("Ver Episodios com o Personagem : "):
                            
                            for episodio in personagem['episode']:
                                with st.container(border=True):
                                    buscar_ep = busca(episodio)
                                    
                                    st.markdown(f"Nome do Episodio : **{buscar_ep['name']}**")
                                    
                                    st.markdown(f"Episodio : **{buscar_ep['episode']}**")
                        
                    
                    with col2:
                        
                        st.image(personagem['image'],caption=personagem['name'])


def avancar_pag():
    """
    * Faz a bsuca da proxima URL e mostra os dados continuos
    """
    
    url_proxima = st.session_state['next_url'] 

    if url_proxima:
        
        buscar_novasInfos = busca(url_proxima)
        
        
        st.session_state['current_data'].extend(buscar_novasInfos['results'])

        
        st.session_state['next_url'] = buscar_novasInfos['info']['next']
        
        
def thema_def():
    """
*---    Define o titulo do Site e sua imagem dependendo do tema escolhido ---*
    """
    
    theme = st_theme()
    tema = 'dark'
    
    if theme:
        tema = theme.get('base')

    img , titulo = st.columns([1,10])

    with img:
        if tema == 'light':
            
                st.image(image="https://raw.githubusercontent.com/Urubu-Card/API/refs/heads/main/Rick_And_Morty_APi/icone_dark.png",)

        else:
            st.image(image="https://raw.githubusercontent.com/Urubu-Card/API/refs/heads/main/Rick_And_Morty_APi/icone_light.png")
        
    with titulo:
        st.html("""
                
                <h1 style="text-align:center">Rick and Morty API : </1>
                <br>
                """)


def main():
    
    session_state()
    thema_def()
 
 
    nome_Perso = st.text_input("Insira o nome do persongaem de Rick and Morty : ",placeholder="Ex: Rick Sanchez")

    st.set_page_config(layout="wide")
    if st.button("Fazer Busca : ") :
        
        url = f"https://rickandmortyapi.com/api/character?name={nome_Perso}"
        
        dados = busca(url)
        
        st.session_state['dados'] = dados
        
        if 'error' in dados:
        
            st.markdown("""
                
                    <h4 style=  "text-align:center; 
                                background-color:#3e2328; 
                                border-radius:10px;">
                        ⚠ Error: Personagem não encontrado.
                    </h4>        
                            
                    """,unsafe_allow_html=1)
            
            st.session_state['current_data'] = []
            
        else:
            
        
            st.session_state['current_data'] = []
            
          
            st.session_state['current_data'].extend(dados['results']) 
            
            #* Guarda a URL da próxima página
            st.session_state['next_url'] = dados['info']['next']
            
            
    if st.session_state['current_data']:
    
        dados_exibir = st.session_state['current_data']
        
        COLUNAS_POR_LINHA = 3 #* <----Modificavel pra qualquer quantidade
        
        
        for i in range(0, len(dados_exibir), COLUNAS_POR_LINHA):
            
           
            cols = st.columns(COLUNAS_POR_LINHA, gap="small") 
            
            
            for j in range(COLUNAS_POR_LINHA):
                
                idx = i + j
                if idx < len(dados_exibir):
                    personagem = dados_exibir[idx]
                    coluna_atual = cols[j]
                    
                    
                    dizer_atributos(personagem, coluna_atual)
                
        if st.session_state['next_url']:
            st.button("Proxima Página : ",on_click=avancar_pag)
            
        st.caption(f"{st.session_state['dados']['info']['count']} personagems encontrados.")
          
        
if __name__ == "__main__":
    main()
        
        






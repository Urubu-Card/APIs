import streamlit as st
import requests
import os 

st.set_page_config(layout="wide")

class Valorant_API:
    """Responsável por buscar dados da API do Valorant."""
    BASE_URL = "https://valorant-api.com/v1"

    @staticmethod
    @st.cache_resource
    def get(endpoint):
        try:
            resposta = requests.get(f"{Valorant_API.BASE_URL}/{endpoint}")
            return resposta.json()
        except requests.exceptions.RequestException:
            return None

class Agente:
    
    
    def __init__(self,dados):
        self.nome        = dados['displayName']
        self.descricao   = dados['description']
        self.fundo       = dados["background"]
        self.imagem      = dados["fullPortraitV2"]
        self.habilidades = dados["abilities"]
        self.role        = dados['role']


    def mostrar(self):
        container_id = f"personagem-{self.nome.lower().replace(' ', '-').replace('/', '')}"
        col_texto, col_imagem = st.columns([1, 1])
        
        with col_texto:
            st.html(f"<h2 style='text-align:center;font-size:45px;'>{self.nome}</h2>")
            st.markdown(f"### {self.descricao}")
            colimg , coldesc = st.columns([1,4])
            
            with colimg:
                st.image(self.role['displayIcon'],width=100)
                
            with coldesc:
                st.markdown(f"## {self.role['displayName']}: ")
                st.markdown(self.role['description'])
                
            st.divider()
            
            st.html("<h2 style='text-align:center;font-size:45px;margin-top:-25px;'>Habilidades:</h2>")
            cols = st.columns(4)
            for habilidade in self.habilidades:
                slot = habilidade['slot']
                
                if slot in  ["Ability1", "Ability2", "Grenade", "Ultimate"]:
                    idx = ["Ability1", "Ability2", "Grenade", "Ultimate"].index(slot)
                    
                    with cols[idx]:
                        st.image(habilidade["displayIcon"])
                        st.markdown(f"##### {habilidade['displayName']}")
                    
        with col_imagem:
            self._mostrar_imagem(container_id)            
            
            
    def _mostrar_imagem(self, container_id):
        st.html(f"""
         <style>

                #{container_id} {{
                    position: relative; 
                    width: 100%; 
                    max-width: 700px;
                    height: 800px; 
                    margin: auto; 
                    overflow: hidden; 
                }}

                #{container_id}::before {{
                    content: '';
                    position: absolute;
                    inset: 0;
                    z-index: 1; 

                    background-image: url('{self.fundo}'); 
                    background-size: cover;
                    background-position: center;
                    filter: blur(0px); 
                    transition: filter 0.3s ease;
                }}

                #{container_id} .img-personagem {{
                    position: absolute; 
                    top: 0; left: 0;
                    width: 100%; height: 100%;
                    object-fit: contain;
                    z-index: 2; 
                    transform: scale(1.0);
                    
                    transition: transform 0.3s ease; 
                }}

                #{container_id}:hover::before {{
                    filter: blur(5px);
                }}


                #{container_id}:hover .img-personagem {{
                    transform: scale(1.1);
                }}
            </style>

            <div id="{container_id}">
                <img src="{self.imagem}" class="img-personagem"
            </div>
            """)

class App:
    def __init__(self):
        self.api = Valorant_API()

    def exibir_agentes(self):
        dados = self.api.get("agents?language=pt-BR&isPlayableCharacter=True")
        for personagem in dados["data"]:
            agente = Agente(personagem)
            agente.mostrar()
            st.divider()


    def run(self):
        with st.sidebar:
            escolha = st.selectbox("Escolha uma função", ("Agentes", "Armas"))

        if escolha == "Agentes":
            self.exibir_agentes()
        else:
            st.warning("⚠️ Área em Desenvolvimento")

    


# Execução do app
if __name__ == "__main__":
    app = App()
    app.run()
        
                    

import streamlit as st
import requests
from datetime import datetime




    
class Chess_API:
    
    
    BASE_URL="https://api.chess.com/pub"
    
    
    @staticmethod
    @st.cache_resource
    def buscar(endpoint):
        
        try:
            
            url = f"{Chess_API.BASE_URL}/{endpoint}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }#*Importante para conseguir fazer o requests sem ter o erro 403
                     
            resposta = requests.get(url,headers=headers)
            resposta.raise_for_status()
            
            return resposta.json()
        
        except requests.exceptions.JSONDecodeError:
            st.warning("JSONDecodeError occurred.")
            st.write(f"Status code  :{resposta.raise_for_status}")
            st.write(resposta.text)
            
        except requests.exceptions.RequestException as e:
            st.error(f"Request Error : {e}")


class Players:
    
    
    def __init__(self,dados):
        self.nome           = dados.get('name')
        self.username       = dados.get('username')
        self.avatar         = dados.get('avatar')
        self.streamer       = dados.get('is_streamer')
        self.seguidores     = dados.get('followers')
        self.league         = dados.get('league')
        self.status         = dados.get('status')
        self.pais           = dados.get('country')
        self.plataformas    = dados.get('streaming_platforms')
        self.rapid          = dados.get('chess_rapid')
        self.bullet         = dados.get('chess_bullet')
        self.daily          = dados.get('chess_daily')
        self.blitz          = dados.get('chess_blitz')
        self.tatics         = dados.get('tactics')
        
        
        
        
        
        
    def basico_player(self):
        
        if self.avatar:
            coltext ,colimg =st.columns([2,1])
            tem_avatar = 1
        else:
            coltext, = st.columns([1])
            tem_avatar = 0
        
        
        with coltext:
            if self.nome:
                st.html(f'''<h1 style="align: center; font-size:42px;"> {self.nome}({self.username.capitalize()})<h1>''')
            else:
                st.html(f'''<h1 style="align: center; font-size:42px;">{self.username.capitalize()}<h1>''')    
            
            colseg ,collegue ,colstatus = st.columns([1.5,1.5,1.5])
            with colseg:
                st.badge(f"Seguidores: **{self.seguidores}**",icon=":material/groups:")
        
            with collegue:
                st.badge(f"Liga: **{self.league}**",icon=":material/trophy:",color='yellow')
    
            with colstatus:
                st.badge(f"Nivel: **{self.status.capitalize()}**",icon=":material/handshake:" , color= "orange")
                
            st.html("""
                    <style>
                    
                        h2{
                            text-align: center;
                            font-size:  42px;
                        }
                    
                    
                    </style>
                    <h2>Partidas : <h2>
       
                    """)
        
        if tem_avatar:        
            with colimg:
                st.image(self.avatar)

                if self.streamer:
                    for plataforma in self.plataformas:

                        # TWITCH
                        if plataforma.get("type") == "twitch":
                            st.html(
                                f"""
                                <div style="display:flex; align-items:center; gap:10px; margin-bottom:8px;">
                                    <img src="https://assets.twitch.tv/assets/favicon-32-e29e246c157142c94346.png" width="30">
                                    <a href="{plataforma['channel_url']}" target="_blank">{self.username.capitalize()}</a>
                                </div>
                                """,
                            )
                        if plataforma.get("type") == "youtube":
                            st.html(
                                f"""
                                <div style="display:flex; align-items:center; gap:10px; margin-bottom:8px;">
                                    <img src="https://www.youtube.com/s/desktop/9c0f82da/img/favicon_144x144.png" width="28">
                                    <a href="{plataforma['channel_url']}" target="_blank">{self.username.capitalize()}</a>
                                </div>
                                """,
                                
                            )

    def stats_player(self) :
        
        
        st.json(self.rapid)
        with st.container():
            
            st.markdown(
                "<div style='padding: 15px; border-radius: 12px; background-color:#111;'>",
                unsafe_allow_html=True
            )

            st.markdown(f"### **Daily**")
                
            self.card_rating(self.daily['last'],self.daily.get('best'))
            
            
            st.markdown("</div>", unsafe_allow_html=True)
            
        st.json(self.bullet)
        st.json(self.blitz)
        st.json(self.daily)
        st.json(self.tatics)
        


    def format_date(self,ts):
        return datetime.fromtimestamp(ts).strftime("%d/%m/%Y") if ts else "-"


    def card_rating(self,last, best=None):
        st.markdown(f"""
            - **Rating atual:** {last['rating']}
            - **Data:** {self.format_date(last.get('date'))}
            - **RD:** {last.get('rd', '-')}
        """)
        
        if best:
            st.markdown(f"""
            - **Melhor rating:** {best['rating']}
            - **Desde:** {self.format_date(best.get('date'))}
            - **Partida:** {best.get('game', '-') }
            """)

    def card_record(record):
        st.markdown(f"""
            - **Vitórias:** {record['win']}
            - **Derrotas:** {record['loss']}
            - **Empates:** {record['draw']}
        """)
            
            
        
        

class App:
    
    
    def __init__(self):
        self.api = Chess_API()
            
            
    def exibir_jogador(self,username):
        
        endpoint_Base = f"player/{username}"
        
        dados = self.api.buscar(f"{endpoint_Base}")    
        player = Players(dados)
        player.basico_player()
        
        dados2 = self.api.buscar(f"{endpoint_Base}/stats")
        playerContinuação = Players(dados2)
        playerContinuação.stats_player()
                
                
            
    def rodar(self):
                
        with st.sidebar:
            escolha = st.selectbox("Escolha uma ação : ",("Players","Lideres","Outras ações"))
        
        if escolha =="Players":
            
            jogador = st.text_input("Escreva o nome do jogador para buscar : ").lower()
            
            if st.button("Buscar jogador : "):
                if not jogador:
                    st.warning("User do jogador não foi inserido ❌")
                
                else:
                    self.exibir_jogador(jogador)    
                    
 
if __name__ =="__main__":
    app = App()
    app.rodar()       

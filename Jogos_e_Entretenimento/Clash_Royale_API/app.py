import streamlit as st
import requests 
import json

@st.cache_resource
def busca(url,headers):

    try:
        resposta = requests.get(url=url,headers=headers)
        dados = resposta.json()
        return dados
    
    except requests.exceptions.RequestException: 
        return None


@st.cache_resource
def carregar_traducoes():
    with open("Jogos_e_Entretenimento/Clash_Royale_API/traducao_cartas.json", "r", encoding="utf-8") as f:
        return json.load(f)


def traduzir_carta(nome, traducoes):
    return traducoes.get(nome, nome)


def cartas():
    
    API_KEY =st.secrets["API_KEY"] 
    url = "https://api.clashroyale.com/v1/cards"

    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    dados = busca(url=url,headers=headers)


    traducoes = carregar_traducoes()

    st.write(dados)
    
    for cartas in dados['items']:
        
        
        with st.container(border=1):
            if 'evolutionMedium' in cartas['iconUrls']:
                col1 , col2 ,col3 =st.columns(3)
            else:
                col1 , col2  =st.columns(2)
            with col1:
                st.markdown(f"## {traduzir_carta(cartas['name'], traducoes)} :")
                
                if cartas['id'] ==28000006: #*ID do Espelho para nao dar erro
                    st.markdown(f"#### Custo de Elixir : :violet[ ?]")
                    
                else:   
                    st.markdown(f"#### Custo de Elixir : :violet[{cartas['elixirCost']}]")

                colTipo,colImg = st.columns(2)

                if cartas['rarity'] == 'common':
                    with colTipo:
                        st.markdown("### :blue[Comum]")
                        
                    with colImg:
                        st.image("Jogos_e_Entretenimento/Clash_Royale_API/carta_Comum.png",width=50)    
                    
                elif cartas['rarity'] == 'rare':
                    with colTipo:
                        st.markdown("### :orange[Raro]")
                        
                    with colImg:
                        st.image("Jogos_e_Entretenimento/Clash_Royale_API/carta_Rara.png",width=50)  
                        
                elif cartas['rarity'] == 'epic':
                    with colTipo:
                        st.markdown("### :violet[Épica]")
                        
                    with colImg:
                        st.image("Jogos_e_Entretenimento/Clash_Royale_API/carta_Epica.png",width=50)  
                        
                elif cartas['rarity'] == 'legendary':
                    with colTipo:
                        st.markdown("#### :rainbow[Lendaria]")
                        
                    with colImg:
                        st.image("Jogos_e_Entretenimento/Clash_Royale_API/carta_Lendaria.png",width=50) 
                        
                elif cartas['rarity'] == 'champion':
                    with colTipo:
                        st.markdown("#### :yellow[Campeão]")
                        
                    with colImg:
                        st.image("Jogos_e_Entretenimento/Clash_Royale_API/carta_Campeao.png",width=50)
                
                
            with col2:
                st.image(cartas['iconUrls']['medium'])
                
            with col3:
                if 'evolutionMedium' in cartas['iconUrls']:
                    st.image(cartas['iconUrls']['evolutionMedium'])


def players():
    
    id_jogador = st.text_input("Insira o ID de um Jogador : (Observação sem # Hashtag)",placeholder="Exemplo: P7VCQJP12").upper()
    st.caption("Não sabe o ID?  [Veja aqui como achar](https://www.google.com/search?q=Onde+fica+o+id+do+Clash+Royale%3F&client=opera-gx&sca_esv=14e63447f7ec96c7&biw=1875&bih=933&sxsrf=AE3TifMqmirlZ6IXOh375v3FJXf_B8kl6Q%3A1760393219014&ei=A3jtaJpRodvWxA_2h63hCA&ved=0ahUKEwja3u_jl6KQAxWhrZUCHfZDK4wQ4dUDCBA&uact=5&oq=Onde+fica+o+id+do+Clash+Royale%3F&gs_lp=Egxnd3Mtd2l6LXNlcnAaAhgCIh9PbmRlIGZpY2EgbyBpZCBkbyBDbGFzaCBSb3lhbGU_MgYQABgWGB4yBhAAGBYYHjIIEAAYgAQYogQyBRAAGO8FSIKfAVDqIFjCnAFwCHgBkAEAmAGkAaAB_x6qAQQ1LjMwuAEDyAEA-AEBmAIroAKUIKgCFMICChAAGLADGNYEGEfCAgcQIxgnGOoCwgINECMY8AUYJxjJAhjqAsICEBAAGAMYtAIY6gIYjwHYAQHCAhAQLhgDGLQCGOoCGI8B2AEBwgIQECMY8AUYgAQYJxjJAhiKBcICChAjGIAEGCcYigXCAhAQLhiABBixAxhDGIMBGIoFwgIKEAAYgAQYQxiKBcICChAuGIAEGEMYigXCAhAQABiABBixAxhDGIMBGIoFwgINEAAYgAQYQxiKBRiLA8ICEBAAGIAEGLEDGEMYigUYiwPCAggQLhiABBixA8ICBxAjGCcYyQLCAgQQIxgnwgILEAAYgAQYsQMYgwHCAg0QLhiABBhDGNQCGIoFwgIXEC4YgAQYsQMY0QMY0gMYxwEYqAMYiwPCAg4QABiABBixAxiDARiLA8ICCxAAGIAEGLEDGIsDwgIKECMY8AUYJxjJAsICCxAAGIAEGJIDGIoFwgIGEAAYCBgewgIFEAAYgATCAg0QABiABBgUGIcCGIsDwgIIEAAYgAQYiwPCAgUQIRigAZgDCfEFf64gkTWmzvOIBgGQBgi6BgYIARABGAqSBwUxMC4zM6AH8oUCsgcEMi4zM7gH7h_CBwkyLjI3LjEzLjHIB3Q&sclient=gws-wiz-serp)")
    
    if st.button("Buscar Jogador : "):
        API_KEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjAyYzY0OGY1LWQ3ZjYtNGE3Ni05OTk1LWJlZWE5MWIyY2UyMyIsImlhdCI6MTc1OTgwMDExMywic3ViIjoiZGV2ZWxvcGVyLzQwYzRiMTZhLWUyM2MtOWE3YS1jNGE4LTM1ZGM0N2JmZmFhZSIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIxMzguMjA0LjIxMS4xNDkiXSwidHlwZSI6ImNsaWVudCJ9XX0.wj3eoQo_X2RJ7kRefN4FRxek7kbeROe2urjBo8Ji94ZApAJfwigwReFLbaVJQVBQJ9KpsG1hZeS8mZtIEvnKZA"
        
        url = f"https://api.clashroyale.com/v1/players/%23{id_jogador}"

        headers = {
            "Authorization": f"Bearer {API_KEY}"
        }

        dados = busca(url=url,headers=headers)

        
        if 'reason' in dados :
            st.error("Erro: O ID do jogador inserido não foi encontrado.")
            
        else:
            with st.container(border=1):
                col1 , col2 = st.columns(2)
                vitorias = dados['wins']
                    
                trescoroas = dados['threeCrownWins']
                    
                porcentagem= round(trescoroas/vitorias*100)
                with col1:
                    st.markdown(f"## {dados['name']}")#*Nome
                    st.markdown(f"### Troféus atuais: {dados['trophies']}🏆")#*Trofeis Atuais
              
             
                    st.markdown(f"### Batalhas no Total: {dados['battleCount']}")#*Batalhas feitas
                    
                    st.markdown(f"#### -✅Batalhas com vitoria: {dados['wins']}")#*Batalhas ganha
                    st.caption(f" {porcentagem}% de vitorias com Três Coroas")
                    
                    st.markdown(f"#### -❌Batalhas com derrota: {dados['losses']}")#*Batalhas perdida
                
                with col2:
                    st.markdown(f"### Nível: {dados['expLevel']}")#*Nivel
                    st.markdown(f"### Máx. de troféus: {dados['bestTrophies']}🏆")#*Maximo de trofeis adiquirido

                    col3,col4 =st.columns(2)
                    
                    #st.markdown(f"### Clã: {dados}")#*Nome do clan
                    
                    
                    st.subheader("Arena:")
                    st.write(dados['arena'])
                    st.json(f" {dados['currentDeck']}")#*Decka tual
          
     

st.html("""
        
        <h1 align="center">
        <font size = 7>
            Clash Royale API : 
        </font>
        </h1>
        
        """)

with st.sidebar:

    escolha =st.selectbox("Escolha uma função :",("Cartas","Jogadores"),)

if escolha=="Cartas":
    cartas()

if escolha =="Jogadores":
    players()



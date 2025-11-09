import streamlit as st
import requests
from deep_translator import GoogleTranslator
import plotly.express as px

st.set_page_config(page_title="PokéAPI",page_icon="icone.png")


def traduzir_texto(texto, linguagem='pt'):
    traducao = GoogleTranslator(source='en', target=linguagem).translate(texto)
    return traducao


@st.cache_resource
def busca(url):
    """
    !---   Faz a busca simples indo a busca da url entregando a resposta em JSON ---!
    """
    try:
        resposta = requests.get(url=url)
        dados = resposta.json()
        return dados
    except requests.exceptions.RequestException: 
        return None


def falar_caracteristicas(dados):
    col1, col2 = st.columns(2)

    with col1:
        
        st.title(f"{dados['name'].replace('-',' ').capitalize()} : ")
        
        st.subheader(f"Número da Pokedex : {dados['id']}")
        
        
#*          Fala os tipos de pokemon em duas colunas de acordo com o tanto de tipos
        st.markdown("###  Tipos do Pokemon :")
        
        cols_tipos = st.columns(len(dados['types']))
       
        for i, tipo in enumerate(dados['types']):
            url_tipo =busca(tipo['type']['url'])
            
            with cols_tipos[i]:
                st.image(url_tipo['sprites']['generation-vii']['lets-go-pikachu-lets-go-eevee']['name_icon'],width=200)
                
#*          Diz os atributos do pokemon(vida,ataque...)
        st.markdown("### Atributos do Pokemon :")
        
        for status in dados['stats']:
            if status['stat']['name'] == 'hp':
                vida =   status['base_stat']
    
            if status['stat']['name'] == 'attack':
                ataque = status['base_stat']
                
            if status['stat']['name'] == 'defense':
                defesa = status['base_stat']
                
            if status['stat']['name'] == 'speed':
                velocidade = status['base_stat']
                
        
        st.markdown(f"#####     -:heart: HP = {vida}")
        st.markdown(f"#####     -:hocho: Ataque = {ataque}")
        st.markdown(f"#####     -:shield: Defesa = {defesa}")
        st.markdown(f"#####     -:footprints: Velocidade = {velocidade}")
        with st.popover("Grafico de Barras"):        
            categorias = ['Ataque', 'Defesa', 'HP', 'Velocidade']
            valores = [ataque, defesa, vida, velocidade]

            # Criando o gráfico com Plotly
            fig = px.bar(x=valores, y=categorias, labels={'x': 'Valor', 'y': 'Características'}, title="Gráfico de Barras :")

            # Rotacionando os rótulos do eixo X
            fig.update_layout(xaxis_tickangle=90)

            # Exibindo o gráfico no Streamlit
            st.plotly_chart(fig)
                
        
#*          Fala a Altura e Peso do Pokemon
        altura = int(dados['height']) / 10
        st.markdown(f"#### Altura : {altura}m")
        
        peso = int(dados['weight']) / 10
        st.markdown(f"#### **Peso** : {peso}kg")


        with st.popover("Habilidades :"):
            for habilidades in dados['abilities']:
                buscar_habil = busca(habilidades['ability']['url'])
                if buscar_habil:
                    
                    nome_habilidade = traduzir_texto(buscar_habil['name']).capitalize()
                    st.markdown(f"##### {nome_habilidade} :")
                    
                    for efeito in buscar_habil['effect_entries']:
                        if 'en' in efeito['language']['name']:
                            efeito_habilidade = traduzir_texto(efeito['effect'].capitalize())
                            st.write(efeito_habilidade)

    with col2:
        opcoes_imagem = {}
        
        imagens = dados['sprites']['other']
        
        #
        if imagens['official-artwork']['front_default']:
            opcoes_imagem['Arte Oficial'] = imagens['official-artwork']['front_default']
        if imagens['official-artwork']['front_shiny']:
            opcoes_imagem['Arte Oficial (Shiny)'] = imagens['official-artwork']['front_shiny']
        if imagens['dream_world']['front_default']:
            opcoes_imagem['Dream World'] = imagens['dream_world']['front_default']
        if imagens['home']['front_default']:
            opcoes_imagem['Home'] = imagens['home']['front_default']
        if imagens['home']['front_shiny']:
            opcoes_imagem['Home (Shiny)'] = imagens['home']['front_shiny']
        if imagens['showdown']['front_default']:
            opcoes_imagem['Showdown'] = imagens['showdown']['front_default']
        if imagens['showdown']['front_shiny']:
            opcoes_imagem['Showdown (Shiny)'] = imagens['showdown']['front_shiny']
        
        if opcoes_imagem:
            lista_opcoes = list(opcoes_imagem.keys())

            if 'arte_selecionada' not in st.session_state or st.session_state.arte_selecionada not in lista_opcoes:
                st.session_state.arte_selecionada = lista_opcoes[0] 

            
            url_imagem_exibir = opcoes_imagem[st.session_state.arte_selecionada]
            
            
            st.image(url_imagem_exibir,width=310)

            
            st.selectbox(
                "Selecione uma arte:",
                options=lista_opcoes,
                key='arte_selecionada' 
            )
        else:
            st.image(dados['sprites']['front_default'])


def main():
    
    st.html("""
        <h1 align="center">
        <font size = 7>
            Pokémon API : 
        </font>
        </h1>
        """)
    
    if 'dados_pokemon' not in st.session_state:
        st.session_state.dados_pokemon = None
    if 'dados2' not in st.session_state:
        st.session_state.dados2 = None
    if 'variedade_selecionada' not in st.session_state:
        st.session_state.variedade_selecionada = None

    nome_poke = st.text_input("Digite o nome de um pokemon", placeholder="Ex: Gengar")

    def buscar_pokemon_selecionado():
        escolha = st.session_state.variedade_selecionada
        if escolha:
            url = f"https://pokeapi.co/api/v2/pokemon/{escolha.lower()}"
            dados3 = busca(url)
            st.session_state.dados_pokemon = dados3
            st.session_state.dados2 = None 
            st.session_state.variedade_selecionada = None 

    if st.button("Realizar Busca : "):
        st.session_state.dados_pokemon = None
        st.session_state.dados2 = None
        st.session_state.variedade_selecionada = None 
        
        if not nome_poke:
            st.error("⚠️ Nome do Pokémon não inserido !")
        else:
            url = f"https://pokeapi.co/api/v2/pokemon/{nome_poke.lower()}"
            dados = busca(url)

            if dados is not None:
                st.session_state.dados_pokemon = dados
            else:
                url_species = f"https://pokeapi.co/api/v2/pokemon-species/{nome_poke.lower()}"
                dados_species = busca(url_species)
                
                if dados_species is not None:
                    st.session_state.dados2 = dados_species
                else:
                    st.error("Erro : Pokémon não encontrado ou não está na API")
    
    if st.session_state.dados2 and not st.session_state.dados_pokemon:
        dados2 = st.session_state.dados2
        
        pokemons_pra_escolher = [p['pokemon']['name'].capitalize() for p in dados2['varieties']]
        
        st.pills(
            "Escolha uma versão do Pokémon:", 
            options=pokemons_pra_escolher, 
            key='variedade_selecionada',
            on_change=buscar_pokemon_selecionado
        )

    if st.session_state.dados_pokemon:
        with st.container():
            falar_caracteristicas(st.session_state.dados_pokemon)

if __name__ == '__main__':
    main()
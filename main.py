import requests
from bs4 import BeautifulSoup
import streamlit as st

st.set_page_config(layout='wide', initial_sidebar_state='expanded')
st.title("Esse app filtra as notícias atuais do Globo.com.")
st.write("Com atualizações no código, ele pode puxar notícias apenas sobre um assunto específico")
st.write("Além do Globo, com a mesma lógica, `podem ser puxados de outros sites de notícias`")

# Defina o User-Agent no cabeçalho
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'"
}

def get_news():
    url = 'https://www.globo.com/'
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')

    noticias = soup.find_all('a')
    tgt_class1 = 'post__title'
    tgt_class2 = 'post-multcontent__link--title__text'

    news_list = []

    for noticia in noticias:
        if (noticia.h2 is not None) and (tgt_class1 in noticia.h2.get('class', [])):
            news_list.append((noticia.h2.text, noticia['href']))
        if (noticia.h2 is not None) and (tgt_class2 in noticia.h2.get('class', [])):
            news_list.append((noticia.h2.text, noticia['href']))

    return news_list

news = get_news()

st.write("Notícias:")
search_query = st.text_input("Pesquisar links:")

# Divida a consulta de pesquisa em palavras individuais
search_words = search_query.lower().split()

filtered_news = [news_item for news_item in news if all(word in news_item[1].lower() for word in search_words)]

if filtered_news:
    for title, link in filtered_news:
        st.markdown(f"[{title}]({link})")
else:
    st.write("Nenhum link encontrado com a pesquisa atual.")


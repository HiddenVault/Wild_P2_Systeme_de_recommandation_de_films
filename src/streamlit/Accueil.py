import streamlit as st

# Lecture du css particulier à appliquer à la page
def lire_css(fichier):
    with open(fichier, 'r', encoding='utf-8') as f:
        return f.read()
    
# Lire le fichier de styles perso
contenu_html = lire_css('pages/st.css')
st.markdown(contenu_html, unsafe_allow_html = True)

st.header('Choisir un type d\'algorithme de ML')

import streamlit as st

# Fonction pour lire le contenu HTML
def lire_html(fichier):
    with open(fichier, 'r', encoding='utf-8') as f:
        return f.read()

# Lire le fichier HTML
contenu_html = lire_html('./pages/fichier.html')

# Afficher le contenu HTML dans Streamlit
st.markdown(contenu_html, unsafe_allow_html=True)

# HTML avec la classe CSS appliquée
st.markdown('<div class="custom-css">Texte avec CSS personnalisé 1</div>', unsafe_allow_html=True)

st.markdown('<div class="custom-css2">Texte avec CSS personnalisé 2</div>', unsafe_allow_html=True)

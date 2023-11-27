import streamlit as st

st.sidebar.title("Navigation")

# Séparateur
st.sidebar.markdown("---")

# Options de navigation
pages = ["Accueil", "Page 1", "Page 2"]
page_selectionnee = st.sidebar.radio("Choisissez une page :", pages)

# Affichage du contenu en fonction de la page sélectionnée
if page_selectionnee == "Accueil":
    st.title("Bienvenue sur l'Accueil")
    # Contenu de l'Accueil
elif page_selectionnee == "Page 1":
    st.title("Page 1")
    # Contenu de la Page 1
elif page_selectionnee == "Page 2":
    st.title("Page 2")
    # Contenu de la Page 2


# CSS personnalisé
st.markdown("""
    <style>
    .custom-css {
        color: green;
        background-color: yellow;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# HTML avec la classe CSS appliquée
st.markdown('<div class="custom-css">Texte avec CSS personnalisé</div>', unsafe_allow_html=True)

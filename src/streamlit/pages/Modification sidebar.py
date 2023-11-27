import streamlit as st
st.markdown('<html>', unsafe_allow_html=True)



# Fonction pour lire le contenu HTML
def lire_html(fichier):
    with open(fichier, 'r', encoding='utf-8') as f:
        return f.read()

# Lire le fichier HTML
contenu_html = lire_html('./pages/fichier.html')

# Afficher le contenu HTML dans Streamlit
st.markdown(contenu_html, unsafe_allow_html=True)


'test??'


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

st.markdown('<a href="lien"> lien hypertexte </a>',unsafe_allow_html=True) 

'''
st.markdown(
    """
    <style>
    .block-container {
        background-color: #ff0099; 
    }
   .sidebar .sidebar-content {
        background: rgb(0, 255, 162); 
    }
    </style>
    """,
    unsafe_allow_html=True
)
'''






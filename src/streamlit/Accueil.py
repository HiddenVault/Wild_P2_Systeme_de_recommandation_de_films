import streamlit as st

# Lecture du css particulier à appliquer à la page
def lire_css(fichier):
    with open(fichier, 'r', encoding='utf-8') as f:
        return f.read()

# Use the full page instead of a narrow central column
st.set_page_config(layout="centered")
# Lire le fichier de styles perso
contenu_html = lire_css('pages/st.css')
st.markdown(contenu_html, unsafe_allow_html = True)

st.title('Choisir une méthode de recommandation...')

st.markdown('''
            ## **Caractéristiques utilisées :**
            
            Pour les 2 méthodes utilisés, les caractéristiques prises en compte dans le modèle sont les suivantes :
            L'année de sortie, le budget, la recette, la note moyenne, le nombre de votes, la durée et le genre
            ''')

st.markdown('''
            ## **Méthode du Clustering :**
            
            Cet algorithme de Machine Learning permet sur compartimenter les films par groupe de caractéristiques similaires.
            Dans le cas présent les films sont divisés en 3 groupes.
            ''')

st.markdown('''
            ## **Méthode du KNN :**
            
            Cet algorithme de Machine Learning permet de retrouver les 5 films les plus proches en combinant toutes les caractéristiques d'un film avec ces plus proches voisins
            ''')

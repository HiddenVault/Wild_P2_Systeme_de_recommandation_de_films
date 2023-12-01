import pandas as pd
import streamlit as st
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import warnings

# Les avertissements sont ignorés
warnings.filterwarnings("ignore")

# Chargement du dataframe à partir du fichier CSV
df = pd.read_csv('ML_F2_merged_data_v3.csv', sep=',', encoding='UTF-8', low_memory=False)

# Sélection des colonnes numériques du dataframe
df_numeric = df.select_dtypes(include=['float64', 'int64'])

# Normalisation des données numériques
scaler = StandardScaler()
df_numeric_normalized = scaler.fit_transform(df_numeric)

# Utilisation de KMEANS pour regrouper les films en clusters
n_clusters = 9
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
df['cluster'] = kmeans.fit_predict(df_numeric_normalized)

# Menu Streamlit
# Lecture du css à appliquer à la page
def lire_css(fichier):
    with open(fichier, 'r', encoding='utf-8') as f:
        return f.read()
contenu_html = lire_css('./pages/st.css')

# Application de la css
st.markdown(contenu_html, unsafe_allow_html = True)

st.header("Notre recommandation...")

# Tri des valeurs uniques par ordre alphabétique
unique_movie_titles = sorted(df['TI_primaryTitle'].unique())

# Utilisation de la liste triée dans la liste déroulante
selected_movie_title = st.selectbox("Saisir un nom de film :", unique_movie_titles, key='movie_selectbox', index=None)

    # Sélection du film
if  selected_movie_title:
    # Filtrage du dataframe en fonction du film sélectionné
    selected_movie_info = df[df['TI_primaryTitle'] == selected_movie_title].iloc[0]

    # Normalisation des données du film sélectionné
    movie_data_normalized = scaler.transform(selected_movie_info[df_numeric.columns].values.reshape(1, -1))

    # Prédiction du cluster du film sélectionné
    selected_movie_cluster = kmeans.predict(movie_data_normalized)

    # Filtrage des films du même cluster
    cluster_movies = df[df['cluster'] == selected_movie_cluster[0]]
    cluster_movies = cluster_movies[cluster_movies['TI_primaryTitle'] != selected_movie_info['TI_primaryTitle']]

    # Sélection des films recommandés
    recommended_movies = cluster_movies.loc[:, ['TI_primaryTitle', 'TI_startYear', 'RA_averageRating', 'RA_numVotes', 'TI_overview', 'TI_poster_path']]

    # Affichage des informations du film sélectionné
    st.header(f"Film sélectionné :")
    st.subheader(f"{selected_movie_info['TI_primaryTitle']}")

    # Présention sur deux colonnes
    col1, col2 = st.columns([1, 2])

    col1.image(selected_movie_info['TI_poster_path'], width=400, use_column_width=True)

    with col2:
        st.write(f"Date de sortie : {round(selected_movie_info['TI_startYear'])}")
        st.write(f"Note moyenne : {selected_movie_info['RA_averageRating']}")
        st.write(f"Votes : {round(selected_movie_info['RA_numVotes'])}")
        st.write(f"Résumé :<br>{selected_movie_info['TI_overview']}", unsafe_allow_html=True)

    st.header("Films recommandés :")

    # Affichage des recommandations
    for _, row in recommended_movies.head(5).iterrows():
        st.subheader(f"{row['TI_primaryTitle']}")

        col1, col2 = st.columns([1, 2])

        col1.image(row['TI_poster_path'], width=400, use_column_width=True)

        with col2:
            st.write(f"Date de sortie : {round(row['TI_startYear'])}")
            st.write(f"Note moyenne : {row['RA_averageRating']}")
            st.write(f"Votes : {round(row['RA_numVotes'])}")
            st.write(f"Résumé :<br>{row['TI_overview']}", unsafe_allow_html=True)
        
        st.markdown("---")

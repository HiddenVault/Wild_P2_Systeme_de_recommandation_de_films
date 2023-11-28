import pandas as pd
import streamlit as st
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import warnings
from PIL import Image

# Ignorer les avertissements
warnings.filterwarnings("ignore")

# Charger le DataFrame à partir du fichier CSV
df = pd.read_csv('./data/preparation/ML_F2_merged_data_v3.csv', sep=',', encoding='UTF-8', low_memory=False)

# Sélection des colonnes numériques du DataFrame
df_numeric = df.select_dtypes(include=['float64', 'int64'])

# Normalisation des données numériques
scaler = StandardScaler()
df_numeric_normalized = scaler.fit_transform(df_numeric)

# Utiliser KMeans pour regrouper les films en clusters
n_clusters = 9
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
df['cluster'] = kmeans.fit_predict(df_numeric_normalized)

# Menu Streamlit
# Affichage de la bannière
image_url= 'http://hiddenvault.fr/P2_Systeme_de_recommandation_de_films/banner.png'
code_html = f"<img src='{image_url}' width='100%'/>"
st.markdown(code_html, unsafe_allow_html = True)

st.title("Movie recommendations")

st.markdown(
    """
    <style>
        body {
            background-color: #000000; /* Noir */
            color: #FFFFFF; /* Blanc */
            margin: 20px !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Saisie du nom du film
user_input = st.text_input("Enter movie name :")

if user_input:
    # Recherche et recommandation des films
    matching_movies = df[df['TI_primaryTitle'].str.contains(user_input, case=False, na=False)]

    if matching_movies.empty:
        st.warning(f"Aucun film trouvé avec la correspondance '{user_input}'. Veuillez réessayer.")
    else:
        # Affichage des films correspondants dans une liste déroulante
        selected_movie = st.selectbox("Select movie :", matching_movies['TI_primaryTitle'])

        # Récupération des informations sur le film sélectionné
        selected_movie_info = matching_movies[matching_movies['TI_primaryTitle'] == selected_movie].iloc[0]

        # Normalisation des données du film sélectionné
        movie_data_normalized = scaler.transform(selected_movie_info[df_numeric.columns].values.reshape(1, -1))

        # Prédiction du cluster du film sélectionné
        selected_movie_cluster = kmeans.predict(movie_data_normalized)

        # Filtrage des films du même cluster
        cluster_movies = df[df['cluster'] == selected_movie_cluster[0]]
        cluster_movies = cluster_movies[cluster_movies['TI_primaryTitle'] != selected_movie_info['TI_primaryTitle']]

        # Sélection des films recommandés
        recommended_movies = cluster_movies.loc[:, ['TI_primaryTitle', 'TI_startYear', 'TI_budget', 'TI_revenue', 'RA_averageRating', 'TI_runtimeMinutes', 'TI_overview', 'RA_numVotes', 'TI_region', 'TI_language','TI_poster_path']].head(5)

        # Affichage des informations du film sélectionné
        st.header("Selected Movie:")
        
        col1, col2 = st.columns([1, 3])
        col1.image(selected_movie_info['TI_poster_path'], width=400, use_column_width=True)

        title_container = col2.empty()
        release_container = col2.empty()
        ratings_container = col2.empty()
        votes_container = col2.empty()

        title_container.text_input("Title :", key="title_selected", value=selected_movie_info['TI_primaryTitle'])
        release_container.text_input("Release :", key="release_selected", value=selected_movie_info['TI_startYear'])
        ratings_container.text_input("Average Ratings :", key="ratings_selected", value=selected_movie_info['RA_averageRating'])
        votes_container.text_input("Votes :", key="votes_selected", value=selected_movie_info['RA_numVotes'])

        st.write(f"Summary :")
        st.write(f"{selected_movie_info['TI_overview']}")

        st.header("Recommended movies :")

        # Affichage des recommandations
        for index, row in recommended_movies.iterrows():
            movie_title = row['TI_primaryTitle']
            poster_path = row['TI_poster_path']
            overview = row['TI_overview']
            start_year = row['TI_startYear']
            average_rating = row['RA_averageRating']
            num_votes = row['RA_numVotes']

            col1, col2 = st.columns([1, 3])
            col1.image(poster_path, width=400, use_column_width=True)

            title_container = col2.empty()
            release_container = col2.empty()
            ratings_container = col2.empty()
            votes_container = col2.empty()

            title_container.text_input("Title :", key=f"title_{index}", value=movie_title)
            release_container.text_input("Release :", key=f"release_{index}", value=start_year)
            ratings_container.text_input("Average Ratings :", key=f"ratings_{index}", value=average_rating)
            votes_container.text_input("Votes :", key=f"votes_{index}", value=num_votes)

            st.write(f"Summary :")
            st.write(f"{overview}")

            st.markdown("<hr>", unsafe_allow_html=True)

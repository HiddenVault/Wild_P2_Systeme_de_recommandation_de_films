import pandas as pd
import streamlit as st
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import warnings

# Ignorer les avertissements
warnings.filterwarnings("ignore")

# Charger le DataFrame à partir du fichier CSV
df = pd.read_csv('./data/preparation/ML_F2_merged_data_v3.csv.csv_explore.csv', sep=',', encoding='UTF-8', low_memory=False)

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
st.title("Recommandations de films")

# Saisie du nom du film
user_input = st.text_input("Entrez le nom du film:")

if user_input:
    # Recherche et recommandation des films
    matching_movies = df[df['TI_primaryTitle'].str.contains(user_input, case=False, na=False)]

    if matching_movies.empty:
        st.warning(f"Aucun film trouvé avec la correspondance '{user_input}'. Veuillez réessayer.")
    else:
        # Affichage des films correspondants dans une liste déroulante
        selected_movie = st.selectbox("Sélectionnez un film:", matching_movies['TI_primaryTitle'])

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
        recommended_movies = cluster_movies.loc[:, ['TI_primaryTitle', 'TI_startYear', 'TI_budget', 'TI_revenue', 'RA_averageRating', 'TI_runtimeMinutes', 'RA_numVotes', 'TI_region', 'TI_language','TI_poster_path']].head(5)

        # Affichage des recommandations
        st.header("Films recommandés:")

        # Afficher les recommandations sous forme de texte (exemple)
        #for index, row in recommended_movies.iterrows():
        #    st.write(f"{row['TI_primaryTitle']} ({row['TI_startYear']}), Note moyenne: {row['RA_averageRating']}, Votes: {row['RA_numVotes']}")

        for index, row in recommended_movies.iterrows():
            movie_title = row['TI_primaryTitle']
            start_year = row['TI_startYear']
            average_rating = row['RA_averageRating']
            num_votes = row['RA_numVotes']
            poster_path = row['TI_poster_path']
        
            # Afficher les informations textuelles
            display_text = (
                f"{movie_title} ({start_year}), "
                f"Note moyenne: {average_rating}, "
                f"Votes: {num_votes}"
            )
            st.write(display_text)
        
            # Afficher l'image
            st.image(poster_path, caption=movie_title, use_column_width=True)



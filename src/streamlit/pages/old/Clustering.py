import pandas as pd
import streamlit as st
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import warnings
from PIL import Image

def dataframe_with_selections(df):
    df_with_selections = df.copy()
    df_with_selections.insert(0, "Select", False)

    # Get dataframe row-selections from user with st.data_editor
    edited_df = st.data_editor(
        df_with_selections,
        hide_index=True,
        column_config={"Select": st.column_config.CheckboxColumn(required=True)},
        disabled=df.columns,
    )

    # Filter the dataframe using the temporary column, then drop the column
    selected_rows = edited_df[edited_df.Select]
    return selected_rows.drop('Select', axis=1)


# Lecture du css particulier à appliquer à la page
def lire_css(fichier):
    with open(fichier, 'r', encoding='utf-8') as f:
        return f.read()

# Lire le fichier de styles perso
contenu_html = lire_css('pages/st.css')

# Ignorer les avertissements
warnings.filterwarnings("ignore")

# Charger le DataFrame à partir du fichier CSV
df = pd.read_csv('../data/preparation/ML_F2_merged_data_v3.csv', sep=',', encoding='UTF-8', low_memory=False)

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
st.markdown(contenu_html, unsafe_allow_html = True)

st.header("Notre recommandation par la méthode du clustering")

PrimTitleList = df.sort_values('TI_primaryTitle')
user_input = st.selectbox("Saisir un nom de film :", PrimTitleList['TI_primaryTitle'], None)

if user_input:
    # Recherche et recommandation des films
    matching_movies = df[df['TI_primaryTitle'].str.contains(user_input, case=False, na=False)]

    selected_movie_info = dataframe_with_selections(matching_movies)
    
    # Si un film est selectionné (df <> vide)
    if selected_movie_info.empty == False:
        # Normalisation des données du film sélectionné
        movie_data_normalized = scaler.transform(selected_movie_info[df_numeric.columns].values.reshape(1, -1))

        # Prédiction du cluster du film sélectionné
        selected_movie_cluster = kmeans.predict(movie_data_normalized)

        # Filtrage des films du même cluster
        cluster_movies = df[df['cluster'] == selected_movie_cluster[0]]

        cluster_movies = cluster_movies[cluster_movies['TI_primaryTitle'] != selected_movie_info.iloc[0]['TI_primaryTitle']]
        cluster_movies = cluster_movies[cluster_movies['TI_primaryTitle'] != selected_movie_info.iloc[0]['TI_primaryTitle']]

        # Sélection des films recommandés
        recommended_movies = cluster_movies.loc[:, ['TI_primaryTitle', 'TI_startYear', 'TI_budget', 'TI_revenue', 
                                                    'RA_averageRating', 'TI_runtimeMinutes', 'TI_overview', 'RA_numVotes', 
                                                    'TI_region', 'TI_language','TI_poster_path']].head(5)

        # Affichage des informations du film sélectionné
        st.header("Film sélectionné :")
        
        col1, col2 = st.columns([1, 2])
        col1.image(selected_movie_info.iloc[0]['TI_poster_path'], width=400, use_column_width=True)

        title_container = col2.empty()
        release_container = col2.empty()
        ratings_container = col2.empty()
        votes_container = col2.empty()

        title_container.text_input("Titre :", key="title_selected", value=selected_movie_info.iloc[0]['TI_primaryTitle'])
        release_container.text_input("Date de sortie :", key="release_selected", value=round(selected_movie_info.iloc[0]['TI_startYear']))
        ratings_container.text_input("Note moy. :", key="ratings_selected", value=selected_movie_info.iloc[0]['RA_averageRating'])
        votes_container.text_input("Votes :", key="votes_selected", value=round(selected_movie_info.iloc[0]['RA_numVotes']))

        st.write(f"Résumé :")
        st.write(f"{selected_movie_info.iloc[0]['TI_overview']}")

        st.header("Films recommandés :")

        # Affichage des recommandations
        for index, row in recommended_movies.iterrows():
            movie_title = row['TI_primaryTitle']
            poster_path = row['TI_poster_path']
            overview = row['TI_overview']
            start_year = round(row['TI_startYear'])
            average_rating = row['RA_averageRating']
            num_votes = round(row['RA_numVotes'])

            col1, col2 = st.columns([1, 2])
            col1.image(poster_path, width=400, use_column_width=True)

            title_container = col2.empty()
            release_container = col2.empty()
            ratings_container = col2.empty()
            votes_container = col2.empty()

            title_container.text_input("Titre :", key=f"title_{index}", value=movie_title)
            release_container.text_input("Date de sortie :", key=f"release_{index}", value=start_year)
            ratings_container.text_input("Note moy. :", key=f"ratings_{index}", value=average_rating)
            votes_container.text_input("Votes :", key=f"votes_{index}", value=num_votes)

            st.write(f"Résumé :")
            st.write(f"{overview}")

            st.markdown("<hr>", unsafe_allow_html=True)

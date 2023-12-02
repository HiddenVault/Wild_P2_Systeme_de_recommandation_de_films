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

# Retourne le ou les genre des film dans une liste.
# df_row correspond à une serie réprésentant une seule ligne de dataset
def donne_genre_film(sr_row) :
    liste_g = [col for i, col in enumerate(sr_row.index) if sr_row.index.str.startswith('GE')[i]]
    valeur_g = [genre.replace('GE_', '') for genre in liste_g if sr_row.loc[genre, '0'] == 1]
    return valeur_g


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
n_clusters = 3
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
df['cluster'] = kmeans.fit_predict(df_numeric_normalized)

# Use the full page instead of a narrow central column
st.set_page_config(layout="wide")
# Menu Streamlit
# Affichage de la bannière
st.markdown(contenu_html, unsafe_allow_html = True)

st.title("Notre recommandation par la méthode du clustering")

col1, col2 = st.columns([1, 1])

PrimTitleList = df.sort_values('TI_primaryTitle')
user_input = col1.selectbox("Saisir un nom de film :", PrimTitleList['TI_primaryTitle'], None)

if user_input:
    # Recherche et recommandation des films
    matching_movies = df[df['TI_primaryTitle'].str.contains(user_input, case=False, na=False)].head(1)

    selected_movie_info = matching_movies.copy() # dataframe_with_selections(matching_movies)

    # Si un film est selectionné (df <> vide)
    if selected_movie_info.empty == False:
        # Normalisation des données du film sélectionné
        movie_data_normalized = scaler.transform(selected_movie_info[df_numeric.columns].values.reshape(1, -1))

        # Prédiction du cluster du film sélectionné
        selected_movie_cluster = kmeans.predict(movie_data_normalized)
        
        # Filtrage des films du même cluster
        cluster_movies = df[df['cluster'] == selected_movie_cluster[0]]

        cluster_movies = cluster_movies[cluster_movies['TI_primaryTitle'] != selected_movie_info.iloc[0]['TI_primaryTitle']]

        # Sélection des films recommandés
        recommended_movies = cluster_movies.loc[:, ['TI_primaryTitle', 'TI_startYear', 'TI_budget', 'TI_revenue', 
                                                    'RA_averageRating', 'TI_runtimeMinutes', 'TI_overview', 'RA_numVotes', 
                                                    'TI_region', 'TI_language','TI_poster_path',
                                                    'GE_Action', 'GE_Adult', 'GE_Adventure', 'GE_Animation', 'GE_Biography',
                                                    'GE_Comedy', 'GE_Crime', 'GE_Documentary', 'GE_Drama', 'GE_Family',
                                                    'GE_Fantasy', 'GE_Film-Noir', 'GE_History', 'GE_Horror', 'GE_Music',
                                                    'GE_Musical', 'GE_Mystery', 'GE_Romance', 'GE_Sci-Fi', 'GE_Sport',
                                                    'GE_Thriller', 'GE_War', 'GE_Western']].head(5)
        recommended_movies['TI_poster_path'].fillna('http://www.clipartbest.com/cliparts/yio/66g/yio66g5eT.jpg',inplace=True)

        # Affichage des informations du film sélectionné
        col1.header("Film sélectionné :")
        
        col11, col12 = col1.columns([1, 2])

        col11.image(selected_movie_info.iloc[0]['TI_poster_path'], width=200, use_column_width=True)
        # ajout du/des genres
        # selected_movie_info.iloc[0]
        # liste_genre = ', '.join(donne_genre_film(selected_movie_info.iloc[0]))

        detail_film = f'''
                **Titre :** {selected_movie_info.iloc[0]['TI_primaryTitle']} \n
                **Date de sortie :** {round(selected_movie_info.iloc[0]['TI_startYear'])} \n
                **Note moy. :** {selected_movie_info.iloc[0]['RA_averageRating']} \n
                **Votes :** {round(selected_movie_info.iloc[0]['RA_numVotes'])} \n
                **Résumé :**   {selected_movie_info.iloc[0]['TI_overview']}
            '''
        col12.markdown(detail_film) 

        col2.header("Films recommandés :")
        tab1_reco = col2.tabs(["#1", "#2", "#3", "#4", "#5"])

        # Affichage des recommandations
        index = 0
        for _, row in recommended_movies.iterrows():

            movie_title = row['TI_primaryTitle']
            poster_path = row['TI_poster_path']
            overview = row['TI_overview']
            start_year = round(row['TI_startYear'])
            average_rating = row['RA_averageRating']
            num_votes = round(row['RA_numVotes'])

            with tab1_reco[index]:
                col21, col22 = tab1_reco[index].columns([1, 2])
                col21.image(poster_path, width=400, use_column_width=True)
                # row
                # ajout du/des genres
                # liste_genre = ', '.join(donne_genre_film(row.to_frame()))
                detail_film_reco = f'''
                        **Titre :** {movie_title} \n
                        **Date de sortie :** {start_year} \n
                        **Note moy. :** {average_rating} \n
                        **Votes :** {num_votes} \n
                        **Résumé :**   {overview}
                    '''
                col22.markdown(detail_film_reco) 

            index += 1

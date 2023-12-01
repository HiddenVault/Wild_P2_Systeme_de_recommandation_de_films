import pandas as pd
import streamlit as st
from sklearn.neighbors import NearestNeighbors
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


# Utilisation de NearestNeighbors pour trouver les voisins les plus proches
n_neighbors = 6  # Nombre de voisins souhaité / Nombre de voisins + 1 car le film recherché est considéré comme son propre voisin
# algorithm='brute' examine toutes les combinaisons possibles sans utiliser de méthodes d'optimisation ou d'index pour accélérer le processus.
# metric='cosine' mesure la similarité entre les points (films).
neighbors_model = NearestNeighbors(n_neighbors=n_neighbors, algorithm='brute', metric='cosine')
neighbors_model.fit(df_numeric_normalized)

# Use the full page instead of a narrow central column
st.set_page_config(layout="wide")
# Menu Streamlit
# Affichage de la bannière
st.markdown(contenu_html, unsafe_allow_html = True)

st.title("Notre recommandation par la méthode KNN")

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
        _, neighbor_indices = neighbors_model.kneighbors(movie_data_normalized)
        # Récupération des 5 films les plus proches
        neighbor_indices = neighbor_indices[0][1:]
        recommended_movies = df.iloc[neighbor_indices][['TI_primaryTitle', 'TI_startYear', 'TI_budget', \
                                                        'TI_revenue', 'RA_averageRating', 'TI_runtimeMinutes',  \
                                                        'TI_overview', 'RA_numVotes', 'TI_region', 'TI_language', \
                                                        'TI_poster_path']]
        recommended_movies['TI_poster_path'].fillna('http://www.clipartbest.com/cliparts/yio/66g/yio66g5eT.jpg',inplace=True)

        # Affichage des informations du film sélectionné
        col1.header("Film sélectionné :")
        
        col11, col12 = col1.columns([1, 2])
        col11.image(selected_movie_info.iloc[0]['TI_poster_path'], width=200, use_column_width=True)
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

                detail_film_reco = f'''
                        **Titre :** {movie_title} \n
                        **Date de sortie :** {start_year} \n
                        **Note moy. :** {average_rating} \n
                        **Votes :** {num_votes} \n
                        **Résumé :**   {overview}
                    '''
                col22.markdown(detail_film_reco) 

            index += 1

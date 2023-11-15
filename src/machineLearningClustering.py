import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import pairwise_distances_argmin_min
from sklearn.pipeline import make_pipeline

df = pd.read_csv('./data/preparation/F2_merged_data.csv', sep=',', encoding='UTF-8', low_memory=False)

# Sélection des colonnes pertinentes pour le clustering
selected_columns = ['tconst', 'TI_primaryTitle', 'TI_startYear', 'TI_runtimeMinutes',
                     'GE_Action', 'GE_Adult', 'GE_Adventure', 'GE_Animation', 'GE_Biography', 'GE_Comedy', 
                     'GE_Crime', 'GE_Documentary', 'GE_Drama', 'GE_Family', 'GE_Fantasy', 'GE_Film-Noir', 
                     'GE_History', 'GE_Horror', 'GE_Music', 'GE_Musical', 'GE_Mystery', 'GE_Romance', 'GE_Sci-Fi', 
                     'GE_Sport', 'GE_Thriller', 'GE_War', 'GE_Western', 'RA_averageRating', 'RA_numVotes']

# Création d'un dataFrame avec les colonnes sélectionnées
df_movies = df[selected_columns]

# Les valeurs manquantes sont remplacées avec des zéros
df_movies = df_movies.fillna(0)

# Conversion des colonnes nécessaires en types numériques
df_movies[['TI_startYear', 'TI_runtimeMinutes', 'RA_averageRating', 'RA_numVotes']] = df_movies[
          ['TI_startYear', 'TI_runtimeMinutes', 'RA_averageRating', 'RA_numVotes']].apply(pd.to_numeric)

# Normalisation des données
scaler = StandardScaler()
df_movies_normalized = scaler.fit_transform(df_movies.drop(['tconst', 'TI_primaryTitle'], axis=1))

# On peut utiliser KMeans
n_clusters = 50  # Nombre de clusters souhaité
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
df_movies['cluster'] = kmeans.fit_predict(df_movies_normalized)

# Fonction pour recommander des films en fonction du nom
def movie_recommendation(movie_name, num_recommendations = 5):
    matching_movies = df_movies[df_movies['TI_primaryTitle'].str.contains(movie_name, case=False, na=False)]

    if matching_movies.empty:
        print("Aucun film trouvé avec le titre partiel fourni.")
        return pd.DataFrame()  # On retourne un DataFrame vide si aucun film n'est trouvé

    # Recherche des correspondances partielles dans les titres
    movie_info = matching_movies.iloc[0]

    # Normalisation des données entrées pour la prédiction du cluster
    movie_info_normalized = scaler.transform([movie_info.drop(['tconst', 'TI_primaryTitle', 'cluster'])])

    # Prédiction du cluster pour le film donné
    movie_cluster = kmeans.predict(movie_info_normalized)[0]

    # Normalisation des données du film recherché
    movie_data = scaler.transform([movie_info.drop(['tconst', 'TI_primaryTitle', 'cluster'])])

    # Sélection des films du même cluster
    cluster_movies = df_movies[df_movies['cluster'] == movie_cluster]

    # Exclusion du film à l'origine de la recommandation
    cluster_movies = cluster_movies[cluster_movies['TI_primaryTitle'] != movie_name]

    # Films les plus proches en termes de genres et de popularité
    distances = pairwise_distances_argmin_min(movie_data, 
                                           cluster_movies.drop(['tconst', 'TI_primaryTitle', 'cluster'], axis=1))

    recommended_movies_indices = distances[0]
    #recommended_movies = cluster_movies.iloc[recommended_movies_indices][['TI_primaryTitle', 'RA_averageRating', 'RA_numVotes']]
    recommended_movies = cluster_movies.iloc[recommended_movies_indices][:num_recommendations][['TI_primaryTitle', 'RA_averageRating', 'RA_numVotes']]

    return recommended_movies

# Menu avec boucle while
while True:
    user_input = input("Entrez le nom du film (ou 'quitter' pour sortir) : ")
    
    if user_input.lower() == 'quitter':
        break  # Quitter la boucle si l'utilisateur saisit "quitter"
    
    recommended_movies = movie_recommendation(user_input)
    
    if recommended_movies.empty:
        print("Aucun film recommandé.")
    else:
        print("Films recommandés :")
        print(recommended_movies)

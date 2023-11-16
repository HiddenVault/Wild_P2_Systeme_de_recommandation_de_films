import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import pairwise_distances_argmin_min
from sklearn.pipeline import make_pipeline
from sklearn.metrics import davies_bouldin_score
import warnings

warnings.filterwarnings("ignore")

df = pd.read_csv('./data/preparation/F2_merged_data.csv', sep=',', encoding='UTF-8', low_memory=False)

# Sélection des colonnes pertinentes pour le clustering
selected_columns = ['tconst', 'TI_primaryTitle', 'TI_startYear', 'TI_runtimeMinutes',
                     'GE_Action', 'GE_Adult', 'GE_Adventure', 'GE_Animation', 'GE_Biography', 'GE_Comedy', 
                     'GE_Crime', 'GE_Documentary', 'GE_Drama', 'GE_Family', 'GE_Fantasy', 'GE_Film-Noir', 
                     'GE_History', 'GE_Horror', 'GE_Music', 'GE_Musical', 'GE_Mystery', 'GE_Romance', 'GE_Sci-Fi', 
                     'GE_Sport', 'GE_Thriller', 'GE_War', 'GE_Western', 'RA_averageRating', 'RA_numVotes']

# Création d'un DataFrame avec les colonnes sélectionnées
df_movies = df[selected_columns]

# Les valeurs manquantes sont remplacées par des zéros
df_movies = df_movies.fillna(0)

# Conversion des colonnes nécessaires en types numériques
df_movies[['TI_startYear', 'TI_runtimeMinutes', 'RA_averageRating', 'RA_numVotes']] = df_movies[
          ['TI_startYear', 'TI_runtimeMinutes', 'RA_averageRating', 'RA_numVotes']].apply(pd.to_numeric)

# Groupement par le titre du film et agrégation des données
df_movies_grouped = df_movies.groupby('TI_primaryTitle').agg({
    'TI_startYear': 'mean',
    'TI_runtimeMinutes': 'mean',
    'RA_averageRating': 'mean',
    'RA_numVotes': 'mean',
}).reset_index()

print("Premières lignes du DataFrame groupé :")
print(df_movies_grouped.head())

# Normalisation des données (en excluant la colonne 'cluster')
scaler = StandardScaler()
df_movies_grouped_normalized = scaler.fit_transform(df_movies_grouped.drop(['TI_primaryTitle'], axis=1))

# On peut utiliser KMeans
n_clusters = 9  # Nombre de clusters souhaité
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
df_movies_grouped['cluster'] = kmeans.fit_predict(df_movies_grouped_normalized)

# Calcul de l'index de Davies-Bouldin. -> C'est tout simplement l'inertie.
db_score = davies_bouldin_score(df_movies_grouped_normalized, kmeans.labels_)
print(f"Index de Davies-Bouldin : {db_score}")

# Fonction pour recommander des films en fonction du nom
def movie_recommendation(movie_name, num_recommendations=5, scaler=None):
    matching_movies = df_movies_grouped[df_movies_grouped['TI_primaryTitle'].str.contains(movie_name, case=False, na=False)]

    if matching_movies.empty:
        print("Aucun film trouvé avec le titre partiel fourni.")
        return pd.DataFrame()  # Pour retourner un DataFrame vide si aucun film n'est trouvé

    # Recherche des correspondances partielles dans les titres
    movie_info = matching_movies.iloc[0]

    # Utilisation du même scaler
    if scaler is None:
        raise ValueError("Scaler requit pour la normalisation.")
    
    movie_info_normalized = scaler.transform([movie_info.drop(['TI_primaryTitle', 'cluster'])])

    # Prédiction du cluster pour le film donné
    movie_cluster = kmeans.predict(movie_info_normalized)[0]
    print("Cluster prédit :", movie_cluster)

    # Normalisation des données du film recherché
    movie_data = scaler.transform([movie_info.drop(['TI_primaryTitle', 'cluster'])])

    # Sélection des films du même cluster
    cluster_movies = df_movies_grouped[df_movies_grouped['cluster'] == movie_cluster]

    print("Films du cluster :")
    print(cluster_movies)

    # Exclusion du film à l'origine de la recommandation
    cluster_movies = cluster_movies[cluster_movies['TI_primaryTitle'] != movie_name]

    # Films les plus proches en termes de genres et de popularité
    distances = pairwise_distances_argmin_min(movie_data, 
                                           cluster_movies.drop(['TI_primaryTitle', 'cluster'], axis=1),
                                           metric='cosine')  # Utilisation de la distance cosinus pour la similarité

    recommended_movies_indices = distances[0]
    recommended_movies = cluster_movies.iloc[recommended_movies_indices][:num_recommendations][['TI_primaryTitle', 'RA_averageRating', 'RA_numVotes']]

    return recommended_movies

# Menu avec boucle while
while True:
    user_input = input("Entrez le nom du film (ou 'quitter' pour sortir) : ")
    
    if user_input.lower() == 'quitter':
        break  # Quitter la boucle si l'utilisateur saisit "quitter"
    
    recommended_movies = movie_recommendation(user_input, scaler=scaler)
    
    if recommended_movies.empty:
        print("Aucun film recommandé.")
    else:
        print("Films recommandés :")
        print(recommended_movies)

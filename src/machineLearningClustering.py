'''
Explications :
1. Chargement du dataframe à partir d'un fichier CSV.
2. Normalisation pour ajuster les valeurs pour qu'elles soient sur une échelle similaire.
3. Clustering avec KMeans : Regroupement des films en groupes similaires en fonction de certaines caractéristiques communes. 
    KMeans examine les caractéristiques des films et les place dans des clusters. Ici, il s'agit des groupes de films similaires.
4. La fonction movie_recommendation permet de lancer la recommandation des films. 
    Elle utilise le nom d'un film fourni par l'utilisateur pour trouver des films similaires dans le même cluster. 
5. Avec le menu, l'utilisateur peut saisir le nom d'un film sans avoir à recharger le script après chaque recherche.
'''

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
import warnings

# On ignore les avertissements
warnings.filterwarnings("ignore")

df = pd.read_csv('./data/preparation/ML_F2_merged_data.csv.csv_explore.csv', sep=',', encoding='UTF-8', low_memory=False)

# Sélection des colonnes numériques du DataFrame
df_numeric = df.select_dtypes(include=['float64', 'int64'])

# Normalisation des données numériques dans le but de les rendre comparables
scaler = StandardScaler()
df_numeric_normalized = scaler.fit_transform(df_numeric)

# Utilisation de KMeans pour regrouper les films en clusters
n_clusters = 9  # Nombre de clusters souhaité
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
df['cluster'] = kmeans.fit_predict(df_numeric_normalized)

# Fonction pour recommander des films en fonction du nom
def movie_recommendation(movie_name, num_recommendations=5):
    # Recherche du film recherché
    movie_info = df[df['TI_primaryTitle'].str.contains(movie_name, case=False, na=False)].iloc[0]

    # Prédiction du cluster auquel le film appartient
    movie_data_normalized = scaler.transform(movie_info[df_numeric.columns].values.reshape(1, -1))
    movie_cluster = kmeans.predict(movie_data_normalized)[0]
    print("Cluster prédit :", movie_cluster)

    # Sélection des films du même cluster
    cluster_movies = df[df['cluster'] == movie_cluster].reset_index(drop=True)[['TI_primaryTitle'] + list(df_numeric.columns)]
    
    # Exclusion du film à l'origine de la recommandation
    cluster_movies = cluster_movies[cluster_movies['TI_primaryTitle'] != movie_info['TI_primaryTitle']]
    
    # Calcul des similarités avec les autres films du cluster
    similarities = cosine_similarity(movie_data_normalized, scaler.transform(cluster_movies.drop(['TI_primaryTitle'], axis=1)))
    recommended_movies_indices = similarities.argsort(axis=1)[:, ::-1][0][:num_recommendations]
    recommended_movies = cluster_movies.iloc[recommended_movies_indices][['TI_primaryTitle', 'RA_averageRating', 'RA_numVotes']]

    # Affichage des informations sur les films du cluster
    print("Films du cluster :")
    print(cluster_movies)

    # Affichage des similarités avec les films du cluster
    print("Similarités avec les films du cluster :")
    print(similarities)

    # Afficher le titre du film saisi
    print("Titre du film saisi :", movie_info['TI_primaryTitle'])

    return recommended_movies

# Menu (pour éviter d'avoir à relancer le script)
while True:
    user_input = input("Entrez le nom du film (ou 'quitter' pour sortir) : ")

    if user_input.lower() == 'quitter':
        break  # Pour quitter le menu

    # Recommandations pour le film saisi
    recommended_movies = movie_recommendation(user_input)

    # Affichage des recommandations
    if recommended_movies.empty:
        print("Aucun film recommandé.")
    else:
        print("Films recommandés :")
        print(recommended_movies)

'''
Explications :
1. Chargement du dataframe à partir d'un fichier CSV.
2. Normalisation pour ajuster les valeurs pour qu'elles soient sur une échelle similaire.
3. Clustering avec KMeans : Regroupement des films en groupes similaires en fonction de certaines caractéristiques communes. 
    KMeans examine les caractéristiques des films et les place dans des clusters qui regroupe des films similaires.
4. La fonction movie_recommendation :
    prend en entrée le nom d'un film, 
    recherche le film dans le DataFrame, 
    normalise ses données, 
    utilise Kmeans pour trouver les films les plus proches dans le cluster, 
    recommande d'autres films similaires.     
5. Avec le menu, l'utilisateur peut saisir le nom d'un film sans avoir à recharger le script après chaque recherche.
'''

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
import warnings
from tabulate import tabulate

# On ignore les avertissements
warnings.filterwarnings("ignore")

df = pd.read_csv('./src/data/preparation/ML_F2_merged_data_v3.csv.csv_explore.csv', sep=',', encoding='UTF-8', low_memory=False)

# Voir s'il est utile de dimensionner la largeur du dataframe et de ses colonnes
# Définition de la largeur d'affichage maximale
pd.set_option('display.width', None)

# Définition de la largeur d'affichage maximale pour une colonne
pd.set_option('display.max_colwidth', None)

# Sélection des colonnes numériques du DataFrame
df_numeric = df.select_dtypes(include=['float64', 'int64'])

# Normalisation des données numériques dans le but de les rendre comparables
scaler = StandardScaler()
df_numeric_normalized = scaler.fit_transform(df_numeric)

# Utilisation de KMeans pour regrouper les films en clusters
n_clusters = 9  # Nombre de clusters souhaité
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
df['cluster'] = kmeans.fit_predict(df_numeric_normalized)

# Initialisation de selected_movie_info avec une valeur par défaut pour éviter l'erreur "UnboundLocalError"
# si l'utilisateur saisit 0, selected_movie_info n'est pas définie, mais le reste du code tente de l'utiliser.
selected_movie_info = None  

# Fonction pour recommander des films en fonction du nom
def movie_recommendation(movie_name):
    # Initialisation de selected_movie_info avec une valeur par défaut
    selected_movie_info = pd.Series()  # Utilisez pd.Series() ou pd.DataFrame() en fonction de vos besoins

    # Recherche du film recherché
    matching_movies = df[df['TI_primaryTitle'].str.contains(movie_name, case=False, na=False)]

    # On vérifie si la recherche retourne un résultat
    # Si on retourne un résultat vide, on affiche un message d'information
    if matching_movies.empty:
        print(f"Aucun film trouvé avec la correspondance '{movie_name}'. Veuillez réessayer.")
        # On retourne un DataFrame vide en cas d'erreur pour signaler qu'aucun résultat n'est disponible.
        return pd.DataFrame()

    # Si plusieurs films correspondent au nom saisi par l'utilisateur, On affiche une liste des films
    if len(matching_movies) > 1:
        print(f"Plusieurs films correspondent à la recherche '{movie_name}':")
        for i, movie in enumerate(matching_movies['TI_primaryTitle']):
            print(f"{i + 1}. {movie}")

        while True:
            try:
                selected_movie_index = int(input("Veuillez sélectionner le numéro du film souhaité : "))

                if 0 <= selected_movie_index <= len(matching_movies):
                    if selected_movie_index != 0:
                        selected_movie_info = matching_movies.iloc[selected_movie_index - 1]
                    else:
                        # Si l'utilisateur saisit 0
                        print("Vous avez sélectionné 0. Veuillez entrer un numéro valide.")
                        # Est-il utile de continuer la boucle pour redemander à l'utilisateur de saisir un numéro valide ?
                    break
                else:
                    print("Veuillez entrer un numéro valide.")
            except ValueError:
                print("Veuillez entrer un numéro valide.")
    else:
        selected_movie_info = matching_movies.iloc[0]

    # Normalisation des données du film recherché
    if not selected_movie_info.empty:  # Vérifier si selected_movie_info n'est pas vide
        # selected_movie_info[df_numeric.columns] : Extraction des données numériques du film spécifique à partir du DataFrame df (qui contient les informations sur plusieurs films).
        # .values: Conversion des données en un tableau numpy.
        # .reshape(1, -1): 
        #   Modification de la forme du tableau :
        #       pour n'avoir qu'une seule ligne (un film utilisé pour la recherche) 
        #       et autant de colonnes que nécessaire (avec -1 on conserve le nombre approprié de colonnes, ajusté automatiquement en fonction de la taille des données existantes.).
        # scaler.transform(bla bla): 
        #   Application de la  normalisation sur ces données. On cherche à ajuster des valeurs pour qu'elles soient sur une échelle similaire.
        # movie_data_normalized: Stockage du résultat de la transformation normalisée dans la variable movie_data_normalized. 
        #   Les caractéristiques du film sont normalisées pour être rendues comparables avec d'autres films dans le modèle de recommandation.
        movie_data_normalized = scaler.transform(selected_movie_info[df_numeric.columns].values.reshape(1, -1))

        # Utilisation de KMeans pour prédire le cluster du film recherché
        selected_movie_cluster = kmeans.predict(movie_data_normalized)

        # Filtrage des films du même cluster que le film recherché
        cluster_movies = df[df['cluster'] == selected_movie_cluster[0]]

        # Exclusion du film à l'origine de la recommandation
        cluster_movies = cluster_movies[cluster_movies['TI_primaryTitle'] != selected_movie_info['TI_primaryTitle']]

        # Sélection des films recommandés
        # Liste des colonnes disponibles
        # 'TI_startYear', 'TI_runtimeMinutes', 'RA_averageRating', 'RA_numVotes', 
        # 'TI_budget', 'TI_revenue', 'TI_poster_path', 'TI_production_companies_name', 
        # 'TI_region', 'TI_language'
        recommended_movies = cluster_movies.loc[:, ['TI_primaryTitle', 'TI_startYear', 'TI_budget', \
                                                        'TI_revenue', 'RA_averageRating', 'TI_runtimeMinutes',  \
                                                        'RA_numVotes', 'TI_region', 'TI_language' \
                                                        ]].head(5)
        # Renommage des colonnes
        recommended_movies.columns = ['Titre', 'Année de début', 'Budget', 'Revenu', 'Note moyenne', \
                                 'Durée', 'Nombre de votes', 'Région', 'Langue']
                
        # Affichage du titre du film saisi
        print("Titre du film saisi :", selected_movie_info['TI_primaryTitle'])       

        # Affichage des informations sur le film sélectionné
        movie_info_df = pd.DataFrame(selected_movie_info[['TI_primaryTitle', 'TI_startYear', 'TI_budget', \
                                   'TI_revenue', 'RA_averageRating', 'TI_runtimeMinutes', \
                                   'RA_numVotes', 'TI_region', 'TI_language']]).transpose()
        movie_info_df.columns = ['Titre', 'Année de début', 'Budget', 'Revenu', 'Note moyenne', \
                                 'Durée', 'Nombre de votes', 'Région', 'Langue']
        print(tabulate(movie_info_df, headers='keys', tablefmt='pretty',colalign=("left")))

        return recommended_movies

    else:
        print("Aucun film sélectionné.")
        return pd.DataFrame()

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
        print(tabulate(recommended_movies, headers='keys', tablefmt='pretty',colalign=("left")))

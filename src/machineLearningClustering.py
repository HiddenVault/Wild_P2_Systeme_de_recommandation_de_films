'''
Explications : 
1. Chargement du dataframe à partir d'un fichier CSV.
2. Sélection des colonnes numériques du DataFrame. On ne se concentre que sur les caractéristiques numériques pour la recommandation.
3. Normalisation pour ajuster les valeurs pour qu'elles soient sur une échelle similaire.
4. Un modèle de Nearest Neighbors est créé avec 
    l'algorithme 'brute' (Recherche exhaustive pour trouver les voisins les plus proches),
    la mesure de similarité cosinus (Mesure la similarité entre deux films. Un score élevé indique une grande similarité.).
5. La fonction movie_recommendation :
    prend en entrée le nom d'un film, 
    recherche le film dans le DataFrame, 
    normalise ses données, 
    utilise Nearest Neighbors pour trouver les voisins les plus proches, 
    et recommande d'autres films similaires.
6. Avec le menu, l'utilisateur peut saisir le nom d'un film sans avoir à recharger le script après chaque recherche.
'''

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import cosine_similarity
import warnings

# On ignore les avertissements
warnings.filterwarnings("ignore")

df = pd.read_csv('./src/data/preparation/ML_F2_merged_data.csv.csv_explore.csv', sep=',', encoding='UTF-8', low_memory=False)

# Sélection des colonnes numériques du DataFrame
df_numeric = df.select_dtypes(include=['float64', 'int64'])

# Normalisation des données numériques dans le but de les rendre comparables
scaler = StandardScaler()
df_numeric_normalized = scaler.fit_transform(df_numeric)

# Utilisation de NearestNeighbors pour trouver les voisins les plus proches
n_neighbors = 6  # Nombre de voisins souhaité / Nombre de voisins + 1 car le film recherché est considéré comme son propre voisin
# algorithm='brute' examine toutes les combinaisons possibles sans utiliser de méthodes d'optimisation ou d'index pour accélérer le processus.
# metric='cosine' mesure la similarité entre les points (films).
neighbors_model = NearestNeighbors(n_neighbors=n_neighbors, algorithm='brute', metric='cosine')
neighbors_model.fit(df_numeric_normalized)

# Initialisation de selected_movie_info avec une valeur par défaut pour éviter l'erreur "UnboundLocalError"
# si l'utilisateur saisit 0, selected_movie_info n'est pas définie, mais le reste du code tente de l'utiliser.
selected_movie_info = None  

# Fonction pour recommander des films en fonction du nom
def movie_recommendation(movie_name):
    # Recherche du film recherché
    matching_movies = df[df['TI_primaryTitle'].str.contains(movie_name, case=False, na=False)]

    # On vérifier si la recherche retourne un résultat
    # Si on retourne un résultat vide, on affiche un message d'information
    if matching_movies.empty: 
        print(f"Aucun film trouvé avec la correspondance '{movie_name}'. Veuillez réessayer.")
        # On retourner un DataFrame vide en cas d'erreur pour signaler qu'aucun résultat n'est disponible.
        return pd.DataFrame()  
                                                                                                                                                                                                                                                                                                                                                                                                                   
    # Si plusieurs films correspondent au nom saisi par l'utilisateur, On affiche une liste des films
    if len(matching_movies) > 1:
        print(f"Plusieurs films correspondent à la recherche '{movie_name}':")
        # Pour chaque boucle, i prend la valeur de l'index et movie prend la valeur de l'élément (dans ce cas, le titre du film).
        for i, movie in enumerate(matching_movies['TI_primaryTitle']):
            # Le numéro de ligne commence à 1 au lieu de 0
            print(f"{i + 1}. {movie}") 
       
        # Affichage d'un menu qui va permettre la sélection d'un film
        while True: # La boucle continue jusqu'à ce qu'on saisisse un numéro de ligne
            try: 
                selected_movie_index = int(input("Veuillez sélectionner le numéro du film souhaité : "))

                # Condition pour vérifier si la valeur est différente de 0
                if selected_movie_index != 0:
                    # On retire 1 car les indices dans Python commencent à 0
                    # La numérotation des films présentée à l'utilisateur commence à 1. 
                    # Pour accéder à la première ligne du DataFrame, on utilise l'index 0, on doit soustraire 1.
                    selected_movie_info = matching_movies.iloc[selected_movie_index - 1]
                break
            # Si le numéro de ligne est incorrect, on affiche un message
            except (ValueError, IndexError):
                print("Veuillez entrer un numéro valide.")
    # Si on a un seul résultat, on attribue les informations de l'unique film de la variable matching_movies à la variable selected_movie_info. 
    # Autrement dit, on sélectionne automatiquement le film correspond.
    else:
        selected_movie_info = matching_movies.iloc[0]

    # Normalisation des données du film recherché
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

    # Recherche des voisins les plus proches
    #   neighbors_model.kneighbors(movie_data_normalized) renvoie une paire de valeurs : Distance et indice des valeurs
    #   _ est utilisé (conviention et lisibilité du code) pour ignorer ou stocker temporairement des valeurs que le programme ne prévoit pas d'utiliser.
    #   Ici le résultat de neighbors_model.kneighbors(movie_data_normalized) a deux parties, mais seule la seconde partie (neighbor_indices) est nécessaire.
    #   On ignore la première  valeur retournée par kneighbors. Elle n'est pas utilisée dans le contexte de ce programme.
    #   On ne stocke que la deuxième partie (neighbor_indices)
    _, neighbor_indices = neighbors_model.kneighbors(movie_data_normalized)

    # Exclusion du film à l'origine de la recommandation
    # neighbor_indices[0] est une liste contenant une liste d'indices pour chaque film.
    # [1:]: On sélectionne tous les indices à partir du deuxième (index 1 jusqu'à la fin)
    neighbor_indices = neighbor_indices[0][1:]

    # Sélection des films recommandés
    recommended_movies = df.iloc[neighbor_indices][['TI_primaryTitle', 'RA_averageRating', 'RA_numVotes']]

    # Afficher le titre du film saisi
    print("Titre du film saisi :", selected_movie_info['TI_primaryTitle'])

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

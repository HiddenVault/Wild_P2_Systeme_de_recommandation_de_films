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

        # Boucle infinie pour permettre la sélectionner d'un film (La boucle continue jusqu'à ce que l'utilisateur fasse une sélection valide.)
        while True:
            try:
                # Saisie du numéro de film souhaité et conversion en entier.
                selected_movie_index = int(input("Veuillez sélectionner le numéro du film souhaité : "))
                # Le numéro sélectionné est-il dans la plage (de 0 à la longueur des films correspondants).
                if 0 <= selected_movie_index <= len(matching_movies):
                    # On vérifie si l'utilisateur a saisi 0 (pour annuler la sélection)
                    if selected_movie_index != 0:
                        # Assignation des informations du film sélectionné à selected_movie_info
                        selected_movie_info = matching_movies.iloc[selected_movie_index - 1]
                    else:
                         # Si l'utilisateur saisit 0, affiche un message d'erreur et continuation de la boucle
                        print("Vous avez sélectionné 0. Veuillez entrer un numéro valide.")
                        # Est-il utile de continuer la boucle pour redemander à l'utilisateur de saisir un numéro valide ?
                    # Sortie de la boucle après une sélection valide
                    break
                else:
                    # Affichage d'un message si le numéro est en dehors de la plage
                    print("Veuillez entrer un numéro valide.")
            except ValueError:
                # Affichage d'un message si la conversion en entier échoue
                print("Veuillez entrer un numéro valide.")
    else:
        # Si on a un unique résultat, les informations de ce film assignées à selected_movie_info
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

        # Recherche des voisins les plus proches
        # neighbors_model.kneighbors(movie_data_normalized) renvoie une paire de valeurs : Distance et indice des valeurs
        # _ est utilisé (conviention et lisibilité du code) pour ignorer ou stocker temporairement des valeurs que le programme ne prévoit pas d'utiliser.
        # Ici le résultat de neighbors_model.kneighbors(movie_data_normalized) a deux parties, mais seule la seconde partie (neighbor_indices) est nécessaire.
        # On ignore la première  valeur retournée par kneighbors. Elle n'est pas utilisée dans le contexte de ce programme.
        # On ne stocke que la deuxième partie (neighbor_indices)
        _, neighbor_indices = neighbors_model.kneighbors(movie_data_normalized)

        # Exclusion du film à l'origine de la recommandation
        # neighbor_indices[0] est une liste contenant une liste d'indices pour chaque film.
        # [1:]: On sélectionne tous les indices à partir du deuxième (index 1 jusqu'à la fin)
        neighbor_indices = neighbor_indices[0][1:]

        # Sélection des films recommandés
        # Liste des colonnes disponibles
        # 'TI_startYear', 'TI_runtimeMinutes', 'RA_averageRating', 'RA_numVotes', 
        # 'TI_budget', 'TI_revenue', 'TI_poster_path', 'TI_production_companies_name', 
        # 'TI_region', 'TI_language'
        # Sélection des informations des films recommandés à partir des indices des voisins
        # iloc permet d'accéder aux lignes du DataFrame df en utilisant des indices. neighbor_indices doit être une liste d'indices représentant les voisins.
        recommended_movies = df.iloc[neighbor_indices][['TI_primaryTitle', 'TI_startYear', 'TI_budget', \
                                                        'TI_revenue', 'RA_averageRating', 'TI_runtimeMinutes',  \
                                                        'RA_numVotes', 'TI_region', 'TI_language' \
                                                        ]]
        # Conversion des colonnes dans movie_info_df
        # astype(int) : Conversion de la colonne en entier
        recommended_movies['TI_startYear'] = recommended_movies['TI_startYear'].astype(int)
        # .map('{:,.0f}'.format) : Mise en place du séparateur de milliers avec la virgule
        # .str.replace(',', '.') : Remplace de la virgule par un point
        recommended_movies['TI_budget'] = recommended_movies['TI_budget'].map('{:,.0f}'.format).str.replace(',', '.') + ' $'
        recommended_movies['TI_revenue'] = recommended_movies['TI_revenue'].map('{:,.0f}'.format).str.replace(',', '.') + ' $'
        recommended_movies['TI_runtimeMinutes'] = recommended_movies['TI_runtimeMinutes'].astype(int)
        recommended_movies['RA_numVotes'] = recommended_movies['RA_numVotes'].map('{:,.0f}'.format).str.replace(',', '.')
        # str.upper() : Conversion de toutes les lettres de la chaîne en majuscules
        recommended_movies['TI_language'] = recommended_movies['TI_language'].str.upper()
        
        # Renommage des colonnes
        recommended_movies.columns = ['Titre', 'Sortie', 'Budget', 'Revenu', 'Note moyenne', \
                                 'Durée', 'Nombre de votes', 'Région', 'Langue']
                
        # Affichage du titre du film saisi
        print("Titre du film saisi :", selected_movie_info['TI_primaryTitle'])       

        # Affichage des informations sur le film sélectionné
        # Sélection des colonnes
        movie_info_df = pd.DataFrame(selected_movie_info[['TI_primaryTitle', 'TI_startYear', 'TI_budget', \
                                   'TI_revenue', 'RA_averageRating', 'TI_runtimeMinutes', \
                                   'RA_numVotes', 'TI_region', 'TI_language']]).transpose()
        
        # Conversion des colonnes dans movie_info_df
         # astype(int) : Conversion de la colonne en entier
        movie_info_df['TI_startYear'] = movie_info_df['TI_startYear'].astype(int)
        # .map('{:,.0f}'.format) : Mise en place du séparateur de milliers avec la virgule
        # .str.replace(',', '.') : Remplace de la virgule par un point
        movie_info_df['TI_budget'] = movie_info_df['TI_budget'].map('{:,.0f}'.format).str.replace(',', '.') + ' $'
        movie_info_df['TI_revenue'] = movie_info_df['TI_revenue'].map('{:,.0f}'.format).str.replace(',', '.') + ' $'
        movie_info_df['TI_runtimeMinutes'] = movie_info_df['TI_runtimeMinutes'].astype(int)
        movie_info_df['RA_numVotes'] = movie_info_df['RA_numVotes'].map('{:,.0f}'.format).str.replace(',', '.')
        # str.upper() : Conversion de toutes les lettres de la chaîne en majuscules
        movie_info_df['TI_language'] = movie_info_df['TI_language'].str.upper()
        
        # Renommage des colonnes
        movie_info_df.columns = ['Titre', 'Sortie', 'Budget', 'Revenu', 'Note moyenne', \
                                 'Durée', 'Nombre de votes', 'Région', 'Langue']
        # Affichage des informations sur le film sélectionné sous forme de tableau
        print(tabulate(movie_info_df, headers='keys', tablefmt='pretty',colalign=("left")))

        # On retourne la liste des films recommandés
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
        #print(recommended_movies)
        print(tabulate(recommended_movies, headers='keys', tablefmt='pretty',colalign=("left")))

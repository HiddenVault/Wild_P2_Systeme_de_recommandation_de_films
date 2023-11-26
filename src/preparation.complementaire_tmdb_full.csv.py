'''
Explications :
1. Le script commence par importer différents modules nécessaires et définir des variables, 
    telles que le dictionnaire `files_dict` qui contient les détails des fichiers à traiter et le préfixe pour les fichiers HTML et CSV.
2. Ensuite, il parcourt chaque fichier spécifié dans le dictionnaire et effectue une série d'opérations, 
    y compris le téléchargement ou la lecture du fichier, la création d'un répertoire pour les fichiers CSV, 
    la manipulation du DataFrame, la création de fichiers CSV, et enfin la création d'un fichier HTML avec des informations détaillées.
'''

import moduleOS
import moduleCSV
import moduleDownload
import moduleOS
import moduleDataframe
import modulePreparationHTML
import time
import pandas as pd
import numpy as np
import re
import ast

# Dictionnaire avec les noms des fichiers, leurs emplacements, leur type de séparateur et le nombre de lignes
files_dict = {
   'complementaire_tmdb_full.csv': ('./src/data/sources', ',', -1, 13, 14, 15)
}

# Préfixe pour les fichiers HTML et CSV
file_prefix = 'P_'

# Début du chronomètre
import time
start_time = time.time()

# Parcours du dictionnaire de fichiers
for file_name, (path, separator, nrows_value, first_rows, sample_rows, last_rows) in files_dict.items():
    # Téléchargement ou lecture du contenu du fichier
    content = moduleDownload.download_or_read_file(file_name, path, separator, nrows_value)
    
    # Utilisez la fonction pour créer le répertoire des fichiers .csv
    csv_directory = './data/preparation'
    moduleOS.create_csv_directory(csv_directory)
    
    if content is not None:
        # Création d'un DataFrame original à partir du contenu du fichier
        df_original = moduleDataframe.create_dataframe(content, separator, nrows_value)

        if df_original is not None:
            # Création d'une copie du DataFrame original pour les manipulations
            df_copy = df_original.copy()

            # Remplacement des retours à la ligne indésirables dans les champs de texte
            df_copy = df_copy.applymap(lambda x: x.replace('\n', '') if isinstance(x, str) else x)

            # Remplacemenent de toutes les occurrences de "NaN" par None dans le DataFrame
            df_copy = df_copy.replace(np.nan, None)

            # Renommage de la colonne 'imdb_id' en 'tconst'
            df_copy = df_copy.rename(columns={'imdb_id': 'tconst'})

            # Fonction pour ajouter un préfixe à la colonne 'poster_path'
            def add_prefix(path):
                if path is not None:
                    return 'https://image.tmdb.org/t/p/original' + str(path)
                return None

            df_copy['poster_path'] = df_copy['poster_path'].apply(add_prefix)

            df_copy['poster_path'].fillna(value=np.nan, inplace=True)

            df_copy['production_companies_name'] = df_copy['production_companies_name'].apply(ast.literal_eval)
            df_copy = df_copy.explode('production_companies_name')
            df_copy['production_companies_name'] = df_copy['production_companies_name'].astype(str)

            # Suppression des colonnes indiquées
            columns_to_drop = ['adult', 'genres','homepage','id','original_language','original_title','release_date','title','runtime','status','production_countries','spoken_languages','production_companies_country','backdrop_path','video','vote_average','vote_count']
            df_copy = df_copy.drop(columns=columns_to_drop)

            # Réinitialiser les index si nécessaire
            # df_copy.reset_index(drop=True, inplace=True)
                
            # Créez les noms des fichiers avec le préfixe
            csv_file_name = f'{file_prefix}{file_name}.csv'
            html_file_name = f'{file_prefix}{file_name}.html'
            html_file_name_with_prefix = html_file_name

            # Fonction pour créer des fichiers CSV
            moduleCSV.create_csv_files(df_copy, csv_directory, csv_file_name, first_rows, sample_rows, last_rows, nrows_value)
            
            local_file_path = f'./data/preparation/{html_file_name}'  # Déclaration de local_file_path
            
            # Fonction pour créer un fichier HTML à partir du DataFrame
            modulePreparationHTML.create_html_file(df_copy, html_file_name, nrows_value, start_time, files_dict, local_file_path, file_prefix='P_')

            # Fonction pour obtenir les informations du DataFrame
            moduleDataframe.get_dataframe_info(df_copy)

            # Fonction pour télécharger un fichier depuis une URL ou lire depuis un chemin local
            moduleDownload.download_or_read_file(file_name, path, separator, nrows_value)

            # Fonction pour créer un DataFrame à partir du contenu du fichier
            moduleDataframe.create_dataframe(content, separator, nrows_value)

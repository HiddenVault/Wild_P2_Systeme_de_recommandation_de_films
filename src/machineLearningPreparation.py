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

# Dictionnaire avec les noms des fichiers, leurs emplacements, leur type de séparateur et le nombre de lignes
files_dict = {
   'F2_merged_data.csv': ('./data/preparation/', ',', -1, 10, 10, 10)
}

# Préfixe pour les fichiers HTML et CSV
file_prefix = 'ML_'

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

            selected_columns = ['tconst', 'TI_primaryTitle', 'TI_startYear', 'TI_runtimeMinutes',
                                 'GE_Action', 'GE_Adult', 'GE_Adventure', 'GE_Animation', 'GE_Biography', 'GE_Comedy', 
                                 'GE_Crime', 'GE_Documentary', 'GE_Drama', 'GE_Family', 'GE_Fantasy', 'GE_Film-Noir', 
                                 'GE_History', 'GE_Horror', 'GE_Music', 'GE_Musical', 'GE_Mystery', 'GE_Romance', 'GE_Sci-Fi', 
                                 'GE_Sport', 'GE_Thriller', 'GE_War', 'GE_Western', 'RA_averageRating', 'RA_numVotes']

            # Remplacer les valeurs NaN dans la colonne 'TI_runtimeMinutes' par 0
            df_copy['TI_runtimeMinutes'] = df_copy['TI_runtimeMinutes'].fillna(0)

            df_copy = df_copy[selected_columns]

            df_copy = df_copy.groupby('tconst').agg({
                'TI_primaryTitle': 'first',  # Utilisation de 'first' pour conserver la première valeur
                **{col: 'max' for col in df_copy.columns if col.startswith('GE_')},
                'TI_startYear': 'mean',
                'TI_runtimeMinutes': 'mean',
                'RA_averageRating': 'mean',
                'RA_numVotes': 'mean'
            }).reset_index()

            nombre_nan_par_colonne = df_copy.isna().sum()
            print(nombre_nan_par_colonne)

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
            #modulePreparationHTML.create_html_file(df_copy, html_file_name, nrows_value, start_time, files_dict, local_file_path, file_prefix='P_')

            # Fonction pour obtenir les informations du DataFrame
            moduleDataframe.get_dataframe_info(df_copy)

            # Fonction pour télécharger un fichier depuis une URL ou lire depuis un chemin local
            moduleDownload.download_or_read_file(file_name, path, separator, nrows_value)

            # Fonction pour créer un DataFrame à partir du contenu du fichier
            moduleDataframe.create_dataframe(content, separator, nrows_value)

import moduleOS
import moduleCSV
import moduleDownload
import moduleOS
import moduleDataframe
import modulePreparationHTML
import time
import pandas as pd
import numpy as np

# Dictionnaire avec les noms des fichiers, leurs emplacements, leur type de séparateur et le nombre de lignes
files_dict = {
    'title.principals.tsv': ('./data/sources', '\t', -1, 19, 20, 21)
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
    
    # Appel de la fonction pour créer le répertoire des fichiers .csv
    csv_directory = './data/preparation'
    moduleOS.create_csv_directory(csv_directory)
    
    if content is not None:
        # Création d'un DataFrame original à partir du contenu du fichier
        df_original = moduleDataframe.create_dataframe(content, separator, nrows_value)  
        
        if df_original is not None:
            # Création d'une copie du DataFrame original pour les manipulations
            df_copy = df_original.copy()

            # Remplacement de toutes les occurrences de "\\N" par NaN dans le DataFrame en utilisant un caractère d'échappement
            df_copy = df_copy.replace('\\N', None)

            # Suppression des colonnes 'ordering', 'job', 'characters'
            columns_to_drop = ['ordering', 'job', 'characters']
            df_copy = df_copy.drop(columns=columns_to_drop)

            # Renommage de la colonne 'nconst' en 'nconst_tp'
            df_copy = df_copy.rename(columns={'nconst': 'nconst_tp'})

            # Réinitialiser les index si nécessaire
            # df_copy.reset_index(drop=True, inplace=True)    

            # Création des noms des fichiers avec le préfixe
            csv_file_name = f'{file_prefix}{file_name}.csv'
            html_file_name = f'{file_prefix}{file_name}.html'

            # Appel de la fonction pour créer des fichiers CSV
            moduleCSV.create_csv_files(df_copy, csv_directory, csv_file_name, first_rows, sample_rows, last_rows, nrows_value)

            local_file_path = f'./data/preparation/{html_file_name}'  # Déclaration de local_file_path

            # Appel de la fonction pour créer un fichier HTML à partir du DataFrame
            modulePreparationHTML.create_html_file(df_copy, html_file_name, nrows_value, start_time, files_dict, local_file_path, file_prefix='P_')

            # Appel de la fonction pour obtenir les informations du DataFrame
            moduleDataframe.get_dataframe_info(df_copy)

            # Appel de la fonction pour télécharger un fichier depuis une URL ou lire depuis un chemin local
            moduleDownload.download_or_read_file(file_name, path, separator, nrows_value)

            # Appel de la fonction pour créer un DataFrame à partir du contenu du fichier
            moduleDataframe.create_dataframe(content, separator, nrows_value)

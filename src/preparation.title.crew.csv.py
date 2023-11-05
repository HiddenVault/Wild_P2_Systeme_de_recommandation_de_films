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
    'title.crew.tsv': ('C:\Temp/Dataframes', '\t', -1, 25, 26, 27)
}

# Préfixe pour les fichiers HTML et CSV
file_prefix = 'P_'

# Début du chronomètre
import time
start_time = time.time()

# Parcours du dictionnaire de fichiers
for file_name, (path, separator, nrows_value, first_rows, sample_rows, last_rows) in files_dict.items():
    content = moduleDownload.download_or_read_file(file_name, path, separator, nrows_value)
    
    # Appel de la fonction pour créer le répertoire des fichiers .csv
    csv_directory = './data/preparation'
    moduleOS.create_csv_directory(csv_directory)
    
    if content is not None:
        df_original = moduleDataframe.create_dataframe(content, separator, nrows_value)  
        if df_original is not None:
            df_copy = df_original.copy()

            # Remplacement de toutes les occurrences de "\\N" par NaN dans le DataFrame
            df_copy = df_copy.replace('\\N', None)

            # Trouvez le nombre maximal d'éléments dans une cellule
            max_elements_directors = df_copy['directors'].str.count(',') + 1
            max_elements_directors = int(max_elements_directors.max())

            max_elements_writers = df_copy['writers'].str.count(',') + 1
            max_elements_writers = int(max_elements_writers.max())        

            # Division de la colonne "directors" en plusieurs colonnes distinctes
            for i in range(max_elements_directors):
                df_copy[f'directors{i+1}'] = df_copy['directors'].str.split(',', expand=True, n=i+1)[i]

            # Division de la colonne "writers" en plusieurs colonnes distinctes
            for i in range(max_elements_writers):
                df_copy[f'writers{i+1}'] = df_copy['writers'].str.split(',', expand=True, n=i+1)[i]

            # Suppression des colonnes 'directors', 'writers'
            columns_to_drop = ['directors', 'writers']
            df_copy = df_copy.drop(columns=columns_to_drop)

            # Réinitialiser les index si nécessaire
            # df_copy.reset_index(drop=True, inplace=True)    

            # Création des noms des fichiers avec le préfixe
            csv_file_name = f'{file_prefix}{file_name}.csv'
            html_file_name = f'{file_prefix}{file_name}.html'
            html_file_name_with_prefix = html_file_name

            moduleCSV.create_csv_files(df_copy, csv_directory, csv_file_name, first_rows, sample_rows, last_rows, nrows_value) # Fonction pour créer des fichiers CSV
            local_file_path = f'./data/preparation/{html_file_name}'  # Déclaration de local_file_path
            modulePreparationHTML.create_html_file(df_copy, html_file_name, nrows_value, start_time, files_dict, local_file_path, file_prefix='P_') # Fonction pour créer un fichier HTML à partir du DataFrame

            # Fonction pour obtenir les informations du DataFrame
            moduleDataframe.get_dataframe_info(df_copy)

            # Fonction pour télécharger un fichier depuis une URL ou lire depuis un chemin local
            moduleDownload.download_or_read_file(file_name, path, separator, nrows_value)

            # Fonction pour créer un DataFrame à partir du contenu du fichier
            moduleDataframe.create_dataframe(content, separator, nrows_value)




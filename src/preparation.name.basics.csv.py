import moduleOS
import moduleCSV
import moduleDownload
import moduleOS
import moduleDataframe
import modulePreparationHTML
import time
import pandas as pd

# Dictionnaire avec les noms des fichiers, leurs emplacements, leur type de séparateur et le nombre de lignes
files_dict = {
#    'title.akas.tsv': ('C:\Temp\Dataframes', '\t', 1000, 10, 11, 12),
#    'complementaire_tmdb_full.csv': ('C:\Temp/Dataframes', ',', 1000, 13, 14, 15),
#    'title.ratings.tsv': ('C:\Temp/Dataframes', '\t', 500, 16, 17, 18),
#    'title.principals.tsv': ('C:\Temp/Dataframes', '\t', 800, 19, 20, 21),
#    'title.episode.tsv': ('C:\Temp/Dataframes', '\t', 300, 22, 23, 24),
#    'title.crew.tsv': ('C:\Temp/Dataframes', '\t', 700, 25, 26, 27),
#    'title.basics.tsv': ('C:\Temp/Dataframes', '\t', 1200, 28, 29, 30),
    'name.basics.tsv': ('C:\Temp/Dataframes', '\t', 900, 31, 32, 33)
}

# Préfixe pour les fichiers HTML et CSV
file_prefix = 'P_'

# Début du chronomètre
import time
start_time = time.time()

# Parcours du dictionnaire de fichiers
for file_name, (path, separator, nrows_value, first_rows, sample_rows, last_rows) in files_dict.items():
    content = moduleDownload.download_or_read_file(file_name, path, separator, nrows_value)
    
    # Utilisez la fonction pour créer le répertoire des fichiers .csv
    csv_directory = './data/preparation'
    moduleOS.create_csv_directory(csv_directory)
    
    if content is not None:
        df_original = moduleDataframe.create_dataframe(content, separator, nrows_value)  
        if df_original is not None:
            df_copy = df_original.copy()

            # Suppression des colonnes 'birthYear' et 'deathYear'
            columns_to_drop = ['birthYear', 'deathYear']
            df_copy = df_original.drop(columns=columns_to_drop)

            # Création des colonnes de valeurs dummies pour 'primaryProfession'
            dummies = df_copy['primaryProfession'].str.get_dummies(sep=',')
            df_copy = pd.concat([df_copy, dummies], axis=1)

            # Renommage de la colonne 'knownForTitles' en 'tconst'
            df_copy = df_copy.rename(columns={'knownForTitles': 'tconst'})
            # Division de la colonne 'tconst' en listes de valeurs
            df_copy['tconst'] = df_copy['tconst'].str.split(',')
            df_copy = df_copy.explode('tconst')

            # Supprimer la colonne 'primaryProfession'
            columns_to_drop = ['primaryProfession']
            df_copy = df_copy.drop(columns=columns_to_drop)

            # Réinitialiser les index si nécessaire
            # df_copy.reset_index(drop=True, inplace=True)    

            # Créez les noms des fichiers avec le préfixe
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




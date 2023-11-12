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
    'name.basics.tsv': ('./data/sources', '\t', -1, 31, 32, 33)
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

            # Conversion de la colonne 'birthYear' en numérique en gérant les erreurs
            df_copy['birthYear'] = pd.to_numeric(df_copy['birthYear'], errors='coerce')
            
            # Remplacement des valeurs NaN par 0
            df_copy['birthYear'].fillna(0, inplace=True)
            
            # Filtrage des dates de naissance supérieures à 1920 ou égales à 0
            df_copy = df_copy[(df_copy['birthYear'] >= 1920)]
            #df_copy = df_copy[(df_copy['birthYear'] >= 1920) | (df_copy['birthYear'] == 0)] # Trop gourmand en ressources

            # Suppression des colonnes indiquées
            columns_to_drop = ['birthYear', 'deathYear']
            df_copy = df_copy.drop(columns=columns_to_drop)

            # Création des colonnes de valeurs dummies pour 'primaryProfession'
            dummies = df_copy['primaryProfession'].str.get_dummies(sep=',')
            df_copy = pd.concat([df_copy, dummies], axis=1)

            # Renommage de la colonne 'knownForTitles' en 'tconst'
            df_copy = df_copy.rename(columns={'knownForTitles': 'tconst'})

            # Renommage de la colonne 'nconst' en 'nconst_nb'
            df_copy = df_copy.rename(columns={'nconst': 'nconst_nb'})

            # Division de la colonne 'tconst' en listes de valeurs
            df_copy['tconst'] = df_copy['tconst'].str.split(',')
            df_copy = df_copy.explode('tconst')

            # Supprimer la colonne 'primaryProfession'
            columns_to_drop = ['primaryProfession']
            df_copy = df_copy.drop(columns=columns_to_drop)
            
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

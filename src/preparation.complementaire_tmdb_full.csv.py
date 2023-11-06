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
   'complementaire_tmdb_full.csv': ('C:\Temp/Dataframes', ',', -1, 13, 14, 15)
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

            # Remplacez toutes les occurrences de "NaN" par None dans le DataFrame
            df_copy = df_copy.replace(np.nan, None)

            df_copy = df_copy.rename(columns={'imdb_id': 'tconst'})

            def add_prefix(path):
                if path is not None:
                    return 'https://image.tmdb.org/t/p/original' + str(path)
                return None

            df_copy['backdrop_path'] = df_copy['backdrop_path'].apply(add_prefix)

            df_copy['poster_path'] = df_copy['poster_path'].apply(add_prefix)
            
            df_copy['production_countries'] = df_copy['production_countries'].apply(lambda x: ','.join(re.findall(r"'(.*?)'", x)))
            dummies = df_copy['production_countries'].str.get_dummies(sep=',')
            dummies = dummies.add_prefix('production_countries_')
            df_copy = pd.concat([df_copy, dummies], axis=1)

            df_copy['spoken_languages'] = df_copy['spoken_languages'].apply(lambda x: ','.join(re.findall(r"'(.*?)'", x)))
            df_copy['spoken_languages'] = df_copy['spoken_languages'].str.upper()
            dummies = df_copy['spoken_languages'].str.get_dummies(sep=',')
            dummies = dummies.add_prefix('spoken_languages_')
            df_copy = pd.concat([df_copy, dummies], axis=1)

            #df_copy['production_companies_name'] = df_copy['production_companies_name'].apply(lambda x: ','.join(re.findall(r"'(.*?)'", x)))
            df_copy['production_companies_country'] = df_copy['production_companies_country'].apply(lambda x: ','.join(re.findall(r"'(.*?)'", x)) if x is not None else '')
            df_copy['production_companies_name'] = df_copy['production_companies_name'].str.upper()
            df_copy = df_copy.explode('production_companies_name')

            df_copy['production_companies_country'] = df_copy['production_companies_country'].apply(lambda x: ','.join(re.findall(r"'(.*?)'", x)))
            df_copy['production_companies_country'] = df_copy['production_companies_country'].str.strip(',')
            dummies = df_copy['production_companies_country'].str.get_dummies(sep=',')
            dummies = dummies.add_prefix('production_companies_country_')
            df_copy = pd.concat([df_copy, dummies], axis=1)

            # Suppression des colonnes 'adult', 'budget', 'genres','homepage','id','original_language','original_title','release_date','runtime','status','production_countries','spoken_languages','production_companies_name','production_companies_country'
            columns_to_drop = ['adult', 'budget', 'genres','homepage','id','original_language','original_title','release_date','runtime','status','production_countries','spoken_languages','production_companies_name','production_companies_country']
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



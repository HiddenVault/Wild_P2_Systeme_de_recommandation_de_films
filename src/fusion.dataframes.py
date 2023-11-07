import moduleOS
import moduleCSV
import moduleDownload
import moduleOS
import moduleDataframe
import modulePreparationHTML
import time
import pandas as pd
import numpy as np
import os

# Dictionnaire avec les noms des fichiers, leurs emplacements, leur type de séparateur et le nombre de lignes
files_dict = {
    'P_title.episode.tsv.csv_explore.csv' :('./data/preparation', ',', -1, 10, 10, 10),
    'P_title.principals.tsv.csv_explore.csv' :('./data/preparation', ',', -1, 10, 10, 10),
    'P_title.akas.tsv.csv_explore.csv' :('./data/preparation', ',', -1, 10, 10, 10),
    'P_complementaire_tmdb_full.csv.csv_explore.csv' :('./data/preparation', ',', -1, 10, 10, 10),
    'P_title.ratings.tsv.csv_explore.csv' :('./data/preparation', ',', -1, 10, 10, 10),
    'P_title.crew.tsv.csv_explore.csv' :('./data/preparation', ',', -1, 10, 10, 10),
    'P_title.basics.tsv.csv_explore.csv' :('./data/preparation', ',', -1, 10, 10, 10),
    'P_name.basics.tsv.csv_explore.csv' :('./data/preparation', ',', -1, 10, 10, 10),
}

# Préfixe pour le fichier CSV
file_prefix = 'F_'

# Début du chronomètre
import time
start_time = time.time()

dataframes = {}  # Dictionnaire pour stocker les DataFrames

for file_name, (directory, separator, lines, *_) in files_dict.items():
    file_path = os.path.join(directory, file_name)
    try:
        if os.path.exists(file_path):
            if lines == -1:
                df = pd.read_csv(file_path, sep=separator)
            else:
                df = pd.read_csv(file_path, sep=separator, nrows=lines)
            dataframes[file_name] = df
    except Exception as e:
        print(f"Erreur lors de la lecture de {file_name}: {e}")

print(dataframes)

merged_df = pd.merge(dataframes['P_title.basics.tsv.csv_explore.csv'], dataframes['P_title.akas.tsv.csv_explore.csv'], left_on='tconst', right_on='tconst', how='inner')
merged_df = pd.merge(merged_df, dataframes['P_complementaire_tmdb_full.csv.csv_explore.csv'], left_on='tconst', right_on='tconst', how='inner')
merged_df = pd.merge(merged_df, dataframes['P_title.ratings.tsv.csv_explore.csv'], left_on='tconst', right_on='tconst', how='inner')
merged_df = pd.merge(merged_df, dataframes['P_title.crew.tsv.csv_explore.csv'], left_on='tconst', right_on='tconst', how='inner')
merged_df = pd.merge(merged_df, dataframes['P_title.principals.tsv.csv_explore.csv'], left_on='tconst', right_on='tconst', how='inner')
merged_df = pd.merge(merged_df, dataframes['P_name.basics.tsv.csv_explore.csv'], left_on='tconst', right_on='tconst', how='inner')
merged_df = pd.merge(merged_df, dataframes['P_title.episode.tsv.csv_explore.csv'], left_on='tconst', right_on='tconst', how='left')

print(merged_df)

# Fichier de sortie
output_filename = f"{file_prefix}merged_data.csv"

# Chemin complet du fichier de sortie en utilisant os.path.join
output_file_path = os.path.join(directory, output_filename)

# Enregistrement du dataFrame dans un fichier CSV
merged_df.to_csv(output_file_path, index=False)

print(f"Le fichier CSV a été enregistré sous : {output_file_path}")
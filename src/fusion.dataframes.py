import os
import pandas as pd

# Dictionnaire avec les noms des fichiers, leurs emplacements, leur type de séparateur et le nombre de lignes
files_dict = {
    'P_title.basics.tsv.csv_explore.csv': ('./data/preparation', ',', -1),
    'P_name.basics.tsv.csv_explore.csv': ('./data/preparation', ',', -1),
    'P_title.principals.tsv.csv_explore.csv': ('./data/preparation', ',', -1),
    'P_title.crew.tsv.csv_explore.csv': ('./data/preparation', ',', -1),
    'P_complementaire_tmdb_full.csv.csv_explore.csv': ('./data/preparation', ',', -1),
    'P_title.akas.tsv.csv_explore.csv': ('./data/preparation', ',', -1),
    'P_title.ratings.tsv.csv_explore.csv': ('./data/preparation', ',', -1),
#    'P_title.episode.tsv.csv_explore.csv': ('./data/preparation', ',', -1)
}

# Préfixe pour le fichier CSV
file_prefix = 'F_'

dataframes = {}  # Dictionnaire pour stocker les DataFrames en mémoire

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

# Fusion des DataFrames en utilisant la colonne tconst
merged_data = None  # Initialisation dictionnaire à zéro.

for df_name, df in dataframes.items():
    if merged_data is None:
        merged_data = df
        print(f"Merging {df_name}...")        
    else:
        print(f"Merging {df_name}...")
        merged_data = merged_data.merge(df, on='tconst', how='inner')
        print(merged_data.head())

# Fichier de sortie
output_filename = f"{file_prefix}merged_data.csv"

# Chemin complet du fichier de sortie en utilisant os.path.join
output_file_path = os.path.join(directory, output_filename)

# Enregistrement du DataFrame fusionné dans un fichier CSV
merged_data.to_csv(output_file_path, index=False)

print(f"Le fichier CSV a été enregistré sous : {output_file_path}")
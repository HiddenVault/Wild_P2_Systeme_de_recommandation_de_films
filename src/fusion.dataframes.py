'''
Explications :
1. Le code commence par définir un dictionnaire (`files_dict`) contenant les noms des fichiers, 
    leurs emplacements, le type de séparateur, et le nombre de lignes à lire (-1 pour tout lire).
2. Un préfixe pour le fichier de sortie (`file_prefix`) est défini.
3. Un DataFrame (`merged_data`) est initialisé à `None` pour stocker les données fusionnées.
4. Les fichiers CSV sont lus un par un, et s'ils existent, 
    ils sont fusionnés dans le DataFrame `merged_data` en utilisant la colonne 'tconst'.
5. Le DataFrame fusionné est ensuite enregistré dans un fichier CSV 
    avec un nom généré à partir du préfixe défini.
6. Des messages sont affichés pour informer l'utilisateur de l'avancement du processus.
'''

# Importation des modules nécessaires
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
    # 'P_title.episode.tsv.csv_explore.csv': ('./data/preparation', ',', -1)
}

# Préfixe pour le fichier CSV
file_prefix = 'F_'

merged_data = None  # Initialisation du DataFrame fusionné à zéro.

# Fusion des DataFrames en utilisant la colonne tconst
for file_name, (directory, separator, lines, *_) in files_dict.items():
    file_path = os.path.join(directory, file_name)
    try:
        if os.path.exists(file_path):
            if lines == -1:
                # Lecture du fichier CSV avec toutes les lignes si le nombre est à -1
                df = pd.read_csv(file_path, sep=separator)
            else:
                # Lecture du fichier CSV avec le nombre de lignes spécifié s'il est différent de -1
                df = pd.read_csv(file_path, sep=separator, nrows=lines)
            
            if merged_data is None:
                # Si c'est le premier fichier, on l'assigne directement à merged_data
                merged_data = df
                print(f"Merging {file_name}...")
            else:
                # Si ce n'est pas le premier fichier, on le fusionne avec merged_data en utilisant la colonne 'tconst'
                print(f"Merging {file_name}...")
                merged_data = merged_data.merge(df, on='tconst', how='inner')
                print(merged_data.head())
    except Exception as e:
        print(f"Erreur lors de la lecture de {file_name}: {e}")

# Fichier de sortie
output_filename = f"{file_prefix}merged_data_v3.csv"

# Chemin complet du fichier de sortie en utilisant os.path.join
output_file_path = os.path.join(directory, output_filename)

# Enregistrement du DataFrame fusionné dans un fichier CSV
print(f"Le fichier CSV est en cours de génération...")
merged_data.to_csv(output_file_path, index=False)

print(f"Le fichier CSV a été enregistré sous : {output_file_path}")

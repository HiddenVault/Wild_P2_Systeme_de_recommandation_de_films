'''
Explications :
1. La fonction `create_csv_files` prend en paramètre un DataFrame (`df`), 
    un répertoire de destination pour les fichiers CSV (`csv_directory`), 
    un nom de fichier (`file_name`), 
    le nombre de premières lignes à inclure dans certains fichiers CSV (`first_rows`), 
    le nombre de lignes à inclure dans un échantillon aléatoire (`sample_rows`), 
    le nombre de dernières lignes à inclure (`last_rows`), et un nombre de lignes dans le DataFrame (`nrows_value`).
2. La fonction utilise le module `moduleOS` pour créer le répertoire de destination CSV si nécessaire.
3. Elle crée plusieurs fichiers CSV selon les spécifications 
    (exploration, premières lignes, échantillons aléatoires, dernières lignes) en utilisant la méthode `to_csv` de pandas.
4. Les noms de fichiers sont générés en fonction des paramètres passés à la fonction, 
    et chaque opération de création de fichier est suivie d'une impression indiquant le succès de l'opération et le chemin du fichier généré.
'''

# Importation du module moduleOS pour gérer les opérations sur le système de fichiers
import moduleOS
# Importation du module os pour des opérations liées au système d'exploitation
import os

# Fonction pour créer différents fichiers CSV à partir d'un DataFrame
def create_csv_files(df, csv_directory, file_name, first_rows, sample_rows, last_rows, nrows_value):
    # Importation du module moduleOS pour créer le répertoire CSV si nécessaire
    moduleOS.create_directory(csv_directory)

    # Si first_rows est spécifié, créer un fichier CSV avec les x premières lignes
    if first_rows > 0:
        csv_file_path_explore = os.path.join(csv_directory, f'{file_name}_explore.csv')
        df.head(nrows_value).to_csv(csv_file_path_explore, index=False, encoding='UTF-8')
        print(f"Exporté en CSV : {csv_file_path_explore}")

    # Si first_rows est spécifié, créer un fichier CSV avec les x premières lignes
    if first_rows > 0:
        csv_file_path_head = os.path.join(csv_directory, f'{file_name}_head.csv')
        df.head(first_rows).to_csv(csv_file_path_head, index=False, encoding='UTF-8')
        print(f"Exporté en CSV : {csv_file_path_head}")

    # Si sample_rows est spécifié, créer un fichier CSV avec un échantillon aléatoire de 50% des données
    if sample_rows > 0:
        csv_file_path_sample = os.path.join(csv_directory, f'{file_name}_sample.csv')
        df.sample(frac=0.50).to_csv(csv_file_path_sample, index=False, encoding='UTF-8')
        print(f"Exporté en CSV : {csv_file_path_sample}")

    # Si sample_rows est spécifié, créer un fichier CSV avec un échantillon aléatoire de 10% des données
    if sample_rows > 0:
        csv_file_path_big_sample = os.path.join(csv_directory, f'{file_name}_big_sample.csv')
        df.sample(frac=0.10).to_csv(csv_file_path_big_sample, index=False, encoding='UTF-8')
        print(f"Exporté en CSV : {csv_file_path_big_sample}")

    # Si last_rows est spécifié, créer un fichier CSV avec les x dernières lignes
    if last_rows > 0:
        csv_file_path_tail = os.path.join(csv_directory, f'{file_name}_tail.csv')
        df.tail(last_rows).to_csv(csv_file_path_tail, index=False, encoding='UTF-8')
        print(f"Exporté en CSV : {csv_file_path_tail}")

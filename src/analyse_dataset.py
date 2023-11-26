'''
Explications :
1. Le code commence par importer les modules nécessaires pour le traitement des fichiers, la manipulation de DataFrames, le téléchargement, etc.
2. Un dictionnaire (`files_dict`) est défini, spécifiant les noms des fichiers, leurs emplacements, les séparateurs, 
    et le nombre de lignes à générer dans les fichiers CSV et HTML.
3. Un préfixe pour les noms de fichiers HTML et CSV est défini (`file_prefix`).
4. Un chronomètre est démarré pour mesurer le temps de génération du rapport.
5. Le code parcourt le dictionnaire de fichiers, télécharge ou lit le contenu, crée des DataFrames, 
    génère des fichiers CSV, HTML, et obtient des informations sur les DataFrames.
6. Les modules tels que `moduleOS`, `moduleCSV`, `moduleDownload`, `moduleDataframe`, et `moduleAnalyseHTML` 
    sont utilisés pour effectuer différentes opérations sur les fichiers et les données.
'''

# Importation des modules nécessaires
import moduleOS
import moduleCSV
import moduleDownload
import moduleDataframe
import moduleAnalyseHTML
import time

# Dictionnaire avec les noms des fichiers, leurs emplacements, leur type de séparateur et le nombre de lignes à générer dans les fichiers csv et html
files_dict = {
    'title.akas.tsv': ('./src/data/sources', '\t', 1000, 20, 20, 20),
    'complementaire_tmdb_full.csv': ('./src/data/sources', ',', 1000, 20, 20, 20),
    'title.ratings.tsv': ('./src/data/sources', '\t', 1000, 20, 20, 20),
    'title.principals.tsv': ('./src/data/sources', '\t', 1000, 20, 20, 20),
    'title.episode.tsv': ('./src/data/sources', '\t', 1000, 20, 23, 20),
    'title.crew.tsv': ('./src/data/sources', '\t', 1000, 20, 20, 20),
    'title.basics.tsv': ('./src/data/sources', '\t', 1000, 20, 20, 20),
    'name.basics.tsv': ('./src/data/sources', '\t', 1000, 20, 20, 20),
}

# Préfixe pour les noms de fichiers HTML et CSV
file_prefix = 'A_'

# Début du chronomètre pour mesurer le temps de génération du rapport
start_time = time.time()

# Parcours du dictionnaire de fichiers
for file_name, (path, separator, nrows_value, first_rows, sample_rows, last_rows) in files_dict.items():
    # Téléchargement ou lecture du contenu du fichier
    content = moduleDownload.download_or_read_file(file_name, path, separator, nrows_value)

    # Création du dossier des fichiers .csv
    csv_directory = './data/analyse/'
    moduleOS.create_csv_directory(csv_directory)

    if content is not None:
        # Création d'un DataFrame à partir du contenu du fichier
        df = moduleDataframe.create_dataframe(content, separator, nrows_value)
        
        if df is not None:
            # Création des noms des fichiers avec le préfixe
            csv_file_name = f'{file_prefix}{file_name}.csv'
            html_file_name = f'{file_prefix}{file_name}.html'
            html_file_name_with_prefix = html_file_name

            # Création des fichiers CSV
            moduleCSV.create_csv_files(df, csv_directory, csv_file_name, first_rows, sample_rows, last_rows, nrows_value)

            # Déclaration de local_file_path pour définir le dossier de sauvegarde
            local_file_path = f'./data/analyse/{html_file_name}'

            # Création des fichiers HTML
            moduleAnalyseHTML.create_html_file(df, html_file_name, nrows_value, start_time, files_dict, local_file_path, file_prefix='A_')

            # Obtention des informations du DataFrame
            moduleDataframe.get_dataframe_info(df)

            # Téléchargement du fichier depuis une URL ou lecture depuis un chemin local
            moduleDownload.download_or_read_file(file_name, path, separator, nrows_value)

            # Création d'un DataFrame à partir du contenu du fichier
            moduleDataframe.create_dataframe(content, separator, nrows_value)
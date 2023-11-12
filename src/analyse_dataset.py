# Importation des modules nécessaires
import moduleOS
import moduleCSV
import moduleDownload
import moduleDataframe
import moduleAnalyseHTML
import time

# Dictionnaire avec les noms des fichiers, leurs emplacements, leur type de séparateur et le nombre de lignes à générer dans les fichiers csv et html
files_dict = {
    'title.akas.tsv': ('./data/sources', '\t', 1000, 10, 11, 12),
    'complementaire_tmdb_full.csv': ('./data/sources', ',', 1000, 13, 14, 15),
    'title.ratings.tsv': ('./data/sources', '\t', 500, 16, 17, 18),
    'title.principals.tsv': ('./data/sources', '\t', 800, 19, 20, 21),
    'title.episode.tsv': ('./data/sources', '\t', 300, 22, 23, 24),
    'title.crew.tsv': ('./data/sources', '\t', 700, 25, 26, 27),
    'title.basics.tsv': ('./data/sources', '\t', 1200, 28, 29, 30),
    'name.basics.tsv': ('./data/sources', '\t', 900, 31, 32, 33),
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
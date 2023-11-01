import moduleOS
import moduleCSV
import moduleDownload
import moduleOS
import moduleDataframe
import moduleHTML
import moduleFTP
import time

# Informations de connexion au FTP
from ftplib import FTP
ftp = FTP('ftp.yaminokoe.net')
ftp.login(user='The_A-Team@brya2535.odns.fr', passwd='cestpourleprojet.')

# Dictionnaire avec les noms des fichiers, leurs emplacements, leur type de séparateur et le nombre de lignes
files_dict = {
    'title.akas.tsv': ('C:\Temp\Dataframes', '\t', 1000, 10, 11, 12),
    'complementaire_tmdb_full.csv': ('C:\Temp/Dataframes', ',', 1000, 13, 14, 15),
    'title.ratings.tsv': ('C:\Temp/Dataframes', '\t', 500, 16, 17, 18),
    'title.principals.tsv': ('C:\Temp/Dataframes', '\t', 800, 19, 20, 21),
    'title.episode.tsv': ('C:\Temp/Dataframes', '\t', 300, 22, 23, 24),
    'title.crew.tsv': ('C:\Temp/Dataframes', '\t', 700, 25, 26, 27),
    'title.basics.tsv': ('C:\Temp/Dataframes', '\t', 1200, 28, 29, 30),
    'name.basics.tsv': ('C:\Temp/Dataframes', '\t', 900, 31, 32, 33),
}

# Début du chronomètre
import time
start_time = time.time()

# Parcours du dictionnaire de fichiers
for file_name, (path, separator, nrows_value, first_rows, sample_rows, last_rows) in files_dict.items():
    content = moduleDownload.download_or_read_file(file_name, path, separator, nrows_value)
    
    # Utilisez la fonction pour créer le répertoire des fichiers .csv
    csv_directory = './data/analyse/csv'
    moduleOS.create_csv_directory(csv_directory)
    
    if content is not None:
        df = moduleDataframe.create_dataframe(content, separator, nrows_value)  
        if df is not None:
            moduleCSV.create_csv_files(df, csv_directory, file_name, first_rows, sample_rows, last_rows, nrows_value) # Fonction pour créer des fichiers CSV

            moduleHTML.create_html_file(df, file_name, nrows_value, start_time, files_dict, ftp) # Fonction pour créer un fichier HTML à partir du DataFrame
            local_file_path = f'./data/analyse/{file_name}.html'
            remote_file_path = 'analyse/' + file_name + '.html'
            moduleFTP.upload_file_to_ftp(local_file_path, remote_file_path, ftp)

            # Fonction pour obtenir les informations du DataFrame
            moduleDataframe.get_dataframe_info(df)

            # Fonction pour télécharger un fichier depuis une URL ou lire depuis un chemin local
            moduleDownload.download_or_read_file(file_name, path, separator, nrows_value)

            # Fonction pour créer un DataFrame à partir du contenu du fichier
            moduleDataframe.create_dataframe(content, separator, nrows_value)

            # Fonction pour transférer un fichier vers le serveur FTP
            moduleFTP.upload_file_to_ftp(local_file_path, remote_file_path, ftp)

            # Fonction pour créer un répertoire
            #moduleOS.create_directory(directory_path)

            #moduleOS.create_csv_directory(directory_path)

ftp.quit()


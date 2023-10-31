# Informations de connexion au FTP
from ftplib import FTP
ftp = FTP('ftp.yaminokoe.net')
ftp.login(user='The_A-Team@brya2535.odns.fr', passwd='cestpourleprojet.')

# Fonction pour obtenir les informations du DataFrame
def get_dataframe_info(df):
    import sys
    import pandas as pd  # Importez pandas ici
    from io import StringIO

    original_stdout = sys.stdout
    sys.stdout = StringIO()

    df.info()  # Affiche les informations du DataFrame

    info_output = sys.stdout.getvalue()  # Récupère la sortie capturée
    sys.stdout = original_stdout  # Rétablit la sortie standard

    if info_output.strip() == '':
        return "Aucune information disponible"
    return info_output

# Fonction pour télécharger un fichier depuis une URL ou lire depuis un chemin local
def download_or_read_file(file_name, path, separator, nrows_value):
    import requests  # Importez requests ici
    import pandas as pd  # Importez pandas ici
    from io import StringIO

    if path.startswith('http'):
        # Le chemin est une URL, téléchargez le fichier depuis le site web
        file_url = path + file_name
        response = requests.get(file_url)
        content = response.content.decode('utf-8')
    else:
        # Le chemin est local, lisez le fichier à partir du chemin local
        local_file_path = f'{path}/{file_name}'
        with open(local_file_path, 'r', encoding='UTF-8') as file:
            content = file.read()
    return content

# Fonction pour créer un DataFrame à partir du contenu du fichier
def create_dataframe(content, separator, nrows_value):
    import pandas as pd  # Importez pandas ici
    from io import StringIO    
    try:
        # Création d'un DataFrame avec les premières lignes en fonction du séparateur
        df = pd.read_csv(StringIO(content), sep=separator, nrows=nrows_value, low_memory=False, encoding='UTF-8')
        return df
    except pd.errors.ParserError as e:
        print(f"Erreur lors de la lecture du fichier: {e}")
        return None

# Fonction pour créer un fichier HTML à partir du DataFrame
def create_html_file(df, file_name, nrows_value, start_time):
    import psutil
    import os
    info_output = get_dataframe_info(df)

    if info_output is not None:
        info_output = info_output.replace('\n', '<br>')
    else:
        info_output = "Aucune information disponible"

    # Chemin absolu du répertoire du script Python
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Chemin absolu du fichier CSS en utilisant le répertoire du script
    css_file_path = os.path.join(script_directory, "style.css")

    # Lecture du contenu du fichier CSS
    css_content = ""
    with open(css_file_path, 'r') as css_file:
        css_content = css_file.read()

    first_rows = files_dict[file_name][3]  # x premières lignes
    sample_rows = files_dict[file_name][4]  # x lignes au hasard
    last_rows = files_dict[file_name][5]  # x dernières lignes

    # Ajout du style CSS directement dans le fichier HTML
    html_content = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <title>{file_name}</title>
        <style>
        {css_content}  # Intégrer le contenu CSS lu depuis le fichier
        </style>
    </head>
    <body>
        <h2>{file_name}</h2>
        <p>L'analyse porte sur les <b>{nrows_value}</b> premières lignes du dataframe</p>
        <!-- Informations sur les ressources -->
        <div>
            <h3>Informations sur les ressources :</h3>
            <p>Temps de génération : {round(time.time() - start_time)} secondes</p>
            <p>Utilisation CPU : {psutil.cpu_percent(interval=None, percpu=True)} %</p>
            <p>Utilisation mémoire : {round((psutil.virtual_memory().used) / (1024 * 1024))} Go</p>
            <p>Processeur : {psutil.cpu_freq().current} MHz</p>
        </div>  
        <!-- Informations sur le dataframe -->
        <div>
            <h3>Informations sur le DataFrame ( df.info() ):</h3> 
            <table>
                {info_output}
            </table>
        </div>  
        <div>            
            <h3>Noms des colonnes ( df.columns ) :</h3> 
            <table>
                <tr><td>{', '.join(df.columns)}</td></tr>
            </table>
        </div>  
        <div>            
            <h3>Types de données des colonnes ( df.dtypes ):</h3> 
            <table>
                {df.dtypes.to_frame().to_html(classes='table table-bordered', header=False)}
            </table>
        </div>  
        <div>            
            <h3>Statistiques descriptives pour les colonnes numériques ( df.describe() ):</h3> 
            <table>
                {df.describe().to_html(classes='table table-bordered', header=False)}
            </table>
        </div>  
        <div>            
            <h3>Valeurs manquantes dans le Dataframe ( df.isnull().sum() ) :</h3>
            <table>
                {df.isnull().sum().to_frame().to_html(classes='table table-bordered', header=False)}
            </table>
        </div>  
        <div>
            <h3>{first_rows} premières lignes :</h3>
            <table> 
                {df.head(first_rows).to_html(index=False, escape=False, classes='table table-bordered')}
            </table>
            <h3>{sample_rows} lignes au hasard :</h3>
            <table> 
                {df.sample(sample_rows).to_html(index=False, escape=False, classes='table table-bordered')}
            </table>
            <h3>{last_rows} dernières lignes :</h3>
            <table> 
                {df.tail(last_rows).to_html(index=False, escape=False, classes='table table-bordered')}
            </table>
        </div>
    </body>
    </html>
    """

    # Chemin local du fichier HTML
    local_file_path = f'./data/analyse/{file_name}.html'

    # Écriture du contenu HTML dans le fichier
    with open(local_file_path, 'w', encoding='UTF-8') as f:
        f.write(html_content)
    
    print(f"Exporté en HTML : {local_file_path}")
    
    # Transfert du fichier HTML vers le serveur FTP
    remote_file_path = 'analyse/' + file_name + '.html'
    upload_file_to_ftp(local_file_path, remote_file_path, ftp)

# Fonction pour transférer un fichier vers le serveur FTP
def upload_file_to_ftp(local_file_path, remote_file_path, ftp):
    with open(local_file_path, 'rb') as local_file:
        ftp.storbinary('STOR ' + remote_file_path, local_file)

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
    content = download_or_read_file(file_name, path, separator, nrows_value)
    if content is not None:
        df = create_dataframe(content, separator, nrows_value)
        if df is not None:
            create_html_file(df, file_name, nrows_value, start_time)  # Appel à la fonction pour créer le fichier HTML
            local_file_path = f'./data/analyse/{file_name}.html'
            remote_file_path = 'analyse/' + file_name + '.html'
            upload_file_to_ftp(local_file_path, remote_file_path, ftp)

# Fermeture de la connexion
ftp.quit()

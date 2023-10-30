import requests
import pandas as pd
from io import StringIO
from ftplib import FTP
import psutil
import time
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import datetime

# URL du répertoire distant
url = 'http://yaminokoe.net/imdb/'

# Propriétaire du fichier
people = 'Yann'

# Nombre de lignes à afficher
nrows_value = 10 # Utiliser -1 pour lire toutes les lignes

# Informations de connexion au FTP
ftp = FTP('ftp.yaminokoe.net')
ftp.login(user='The_A-Team@brya2535.odns.fr', passwd='cestpourleprojet.')


# Fonction pour obtenir les informations du DataFrame
def get_dataframe_info():
    import sys
    from io import StringIO

    original_stdout = sys.stdout
    sys.stdout = StringIO()

    df_original.info()  # Affiche les informations du DataFrame

    info_output = sys.stdout.getvalue()  # Récupère la sortie capturée
    sys.stdout = original_stdout  # Rétablit la sortie standard

    if info_output.strip() == '':
        return "Aucune information disponible"
    return info_output

# Début du chronomètre
start_time = time.time()

# Démarrer la surveillance des ressources avec psutil
psutil.cpu_percent(interval=None, percpu=True)
psutil.virtual_memory()

# Dictionnaire avec les noms des fichiers et leur type de séparateur
files_dict = {
	'name.basics.tsv': '\t'
}

# Parcours du dictionnaire de fichiers
for file_name, separator in files_dict.items():
    # Téléchargement du fichier depuis le répertoire distant
    file_url = url + file_name
    response = requests.get(file_url)
    content = response.text

    try:
        # Saisie d'un descriptif et d'un commentaire
        describe = input("Veuillez saisir la description : ")
        comment = input("Veuillez saisir un commentaire : ")

        # Création d'un DataFrame avec les x premières lignes en fonction du séparateur
        df_original = pd.read_csv(StringIO(content), sep=separator, nrows=nrows_value, low_memory=False, encoding='utf-8')

        df_copie = df_original.copy()

        # Trouvez le nombre maximal d'éléments dans une cellule
        max_elements_primaryProfession = df_copie['primaryProfession'].str.count(',') + 1
        max_elements_primaryProfession = int(max_elements_primaryProfession.max())

        max_elements_knownForTitles = df_copie['knownForTitles'].str.count(',') + 1
        max_elements_knownForTitles = int(max_elements_knownForTitles.max())        

        # Division de la colonne "primaryProfession" en plusieurs colonnes distinctes
        for i in range(max_elements_primaryProfession):
            df_copie[f'primaryProfession_{i+1}'] = df_copie['primaryProfession'].str.split(',', expand=True, n=i+1)[i]

        # Division de la colonne "knownForTitles" en plusieurs colonnes distinctes
        for i in range(max_elements_knownForTitles):
            df_copie[f'knownForTitles_{i+1}'] = df_copie['knownForTitles'].str.split(',', expand=True, n=i+1)[i]

        # Supprimer les colonnes "primaryProfession" et "knownForTitles"
        df_copie.drop(['primaryProfession', 'knownForTitles'], axis=1, inplace=True)

        # Utilisation de explode() pour créer une ligne distincte pour chaque profession et titre connu
        # df_copie = df_copie.explode('primaryProfession')
        # df_copie = df_copie.explode('knownForTitles')

        # Réinitialiser les index
        df_copie.reset_index(drop=True, inplace=True)

        # Nombre de lignes des DataFrames
        rows_original = df_original.shape[0]
        rows_copie = df_copie.shape[0]

        now = datetime.datetime.now()
        formatted_date = now.strftime("%Y%m%d-%H%M")

        # Formattage du nom de fichier html
        output_file_name = f'./data/preparation/{file_name}_{people}_{formatted_date}_{describe}.html'

        # Exportez le DataFrame en HTML
        output_path = f'./data/preparation/{file_name}.html'

        # Générer le graphique
        fig, ax = plt.subplots()
        ax.bar(['Original', 'Copie'], [rows_original, rows_copie], label='Lignes')
        ax.set_xlabel('DataFrames')
        ax.set_ylabel('Nombre de lignes')
        ax.set_title('Comparaison du nombre de lignes')
        plt.legend()

        # Sauvegarder le graphique dans un fichier image (au format PNG)
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        # Convertir l'image en base64
        image_base64 = base64.b64encode(buffer.read()).decode()

        # Ajout du style CSS directement dans le fichier HTML
        html_content = f"""
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                font-family: "Arial", sans-serif;
                }}
                /* Style pour un tableau HTML */
                table {{
                width: 100%;
                table-layout: auto; /* Redimensionnement automatique des colonnes */
                border-collapse: collapse;
                margin: 20px 0;
                font-size: 16px;
                }}

                table, th, td {{
                border: 1px solid #ccc;
                }}

                /* Style pour l'en-tête du tableau */
                th {{
                background-color: #f2f2f2;
                font-weight: bold;
                }}

                /* Style pour les lignes impaires du tableau */
                tr:nth-child(odd) {{
                background-color: #f9f9f9;
                }}

                /* Style pour les cellules du tableau */
                td {{
                padding: 10px;
                text-align: left;
                }}

                /* Style pour les liens dans le tableau */
                a {{
                text-decoration: none;
                color: #007bff;
                }}
            </style>
        </head>
        <body>
            <!-- Informations sur les ressources -->
            <div>
                <h3>Informations sur les ressources :</h3>
                <p>Temps de génération : {round(time.time() - start_time)} secondes</p>
                <p>Utilisation CPU : {psutil.cpu_percent(interval=None, percpu=True)} %</p>
                <p>Utilisation mémoire : {round((psutil.virtual_memory().used) / (1024 * 1024))} Go</p>
                <p>Processeur : {psutil.cpu_freq().current} MHz</p>
            </div>

            <!-- Insertion du graphique dans la page -->
            <img src="data:image/png;base64,{image_base64}" alt="Graphique de comparaison des lignes">'

            <!-- Commentaire -->
            <div>
                <h3>Commentaires :</h3>            
                <p>{comment}</p>
            </div>
            <!-- Informations sur les datasets -->
            <div>            
                <h3>Tableau avec les {nrows_value} premières lignes du dataset original:</h3>
                <p>
                    <table>
                    {df_original.to_html()}
                    </table>
                </p>
                <h3>Tableau avec les {nrows_value} premières lignes du dataset modifié:</h3>
                <p>
                    <table>
                    {df_copie.to_html()}
                    </table>
                </p>
        </body>
        </html>
        """

        # Exportez le DataFrame en CSV
        csv_output_file_name = f'./data/preparation/{file_name}_{people}_{formatted_date}_{describe}.csv'
        df_copie.to_csv(csv_output_file_name, encoding='UTF-8', index=False)
        print(f"Exporté en CSV : {csv_output_file_name}")

        # Chemin local du fichier CSV
        local_csv_file_path = csv_output_file_name

        # Chemin distant sur le serveur FTP pour le fichier CSV
        remote_csv_file_path = 'preparation/' + csv_output_file_name.split('/')[-1]

        # Transfert du fichier CSV vers le serveur FTP
        with open(local_csv_file_path, 'rb') as local_csv_file:
            ftp.storbinary('STOR ' + remote_csv_file_path, local_csv_file)

        with open(output_file_name, 'w', encoding='UTF-8') as f:
            f.write(html_content)

        print(f"Exporté en HTML : {output_file_name}")
    except pd.errors.ParserError as e:
        print(f"Erreur lors de la lecture de {file_name}: {e}")

    # Chemin local du fichier HTML
    local_file_path = output_path

    # Chemin distant sur le serveur FTP
    remote_file_path = 'preparation/' + output_file_name.split('/')[-1]

    # Transfert du fichier HTML vers le serveur FTP
    with open(output_file_name, 'rb') as local_file:
        ftp.storbinary('STOR ' + remote_file_path, local_file)

# Fermeture de la connexion
ftp.quit()
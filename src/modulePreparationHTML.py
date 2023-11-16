'''
Explications :
1. La fonction `create_html_file` prend un DataFrame (`df`), 
    le nom du fichier (`file_name`), 
    le nombre de lignes à analyser (`nrows_value`), 
    le temps de début de la génération (`start_time`), 
    un dictionnaire de fichiers (`files_dict`), 
    le chemin local pour enregistrer le fichier HTML (`local_file_path`), 
    et un préfixe (`file_prefix`).
2. Elle utilise différentes bibliothèques telles que `psutil` pour obtenir des informations système, 
    `os` pour les opérations sur le système
'''

import moduleDataframe  # Importation du module pour obtenir des informations sur le DataFrame
import time
import os
import psutil
import moduleFTP  # Importation du module FTP (peut être utilisé pour le transfert vers un serveur FTP)

# Fonction pour créer un fichier HTML à partir du DataFrame
def create_html_file(df, file_name, nrows_value, start_time, files_dict, local_file_path, file_prefix=''):
    # Obtention des informations sur le DataFrame
    info_output = moduleDataframe.get_dataframe_info(df)

    # Si des informations sont disponibles, remplacer les sauts de ligne par des balises <br>
    if info_output is not None:
        info_output = info_output.replace('\n', '<br>')
    else:
        info_output = "Aucune information disponible"

    # Suppression du préfixe du nom du fichier et de l'extension .html
    file_name = file_name.replace(file_prefix, '').replace('.html', '')

    # Chemin absolu du répertoire du script Python
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Chemin absolu du fichier CSS en utilisant le répertoire du script
    css_file_path = os.path.join(script_directory, "style.css")

    # Lecture du contenu du fichier CSS
    css_content = ""
    with open(css_file_path, 'r') as css_file:
        css_content = css_file.read()

    # Récupération des valeurs spécifiées dans le dictionnaire de fichiers
    first_rows = files_dict[file_name][3]  # x premières lignes
    sample_rows = files_dict[file_name][4]  # x lignes au hasard
    last_rows = files_dict[file_name][5]  # x dernières lignes

    # Structure du fichier HTML
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
                {df.sample(frac=0.10).to_html(index=False, escape=False, classes='table table-bordered')}
            </table>
            <h3>{last_rows} dernières lignes :</h3>
            <table> 
                {df.tail(last_rows).to_html(index=False, escape=False, classes='table table-bordered')}
            </table>
        </div>
    </body>
    </html>
    """

    # Écriture du contenu HTML dans le fichier
    with open(local_file_path, 'w', encoding='UTF-8') as f:
        f.write(html_content)
    
    # Affichage du chemin du fichier HTML exporté
    print(f"Exporté en HTML : {local_file_path}")

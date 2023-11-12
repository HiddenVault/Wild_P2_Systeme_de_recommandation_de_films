# Fonction pour télécharger un fichier depuis une URL ou lire un fichier localement
def download_or_read_file(file_name, path, separator, nrows_value):
    # Importation du module requests pour effectuer des requêtes HTTP
    import requests
    # Importation de la classe StringIO du module io pour traiter les chaînes de caractères comme des fichiers
    from io import StringIO

    # Vérification si le chemin commence par 'http' (URL)
    if path.startswith('http'):
        # Si le chemin est une URL, téléchargez le fichier depuis le site web
        file_url = path + file_name
        # Effectuer une requête HTTP pour obtenir le contenu du fichier
        response = requests.get(file_url)
        # Décoder le contenu de la réponse en utilisant l'encodage UTF-8 
        # Utile si le fichier est hébergé sur un serveur utilisant l'encodage 8859-1 par exemple
        content = response.content.decode('utf-8')
    else:
        # Si le chemin est en local, on lit le fichier à partir du chemin local
        local_file_path = f'{path}/{file_name}'
        # Ouverture du fichier en mode lecture avec l'encodage UTF-8
        with open(local_file_path, 'r', encoding='UTF-8') as file:
            # Lire le contenu du fichier
            content = file.read()
    
    # Retourner le contenu du fichier
    return content

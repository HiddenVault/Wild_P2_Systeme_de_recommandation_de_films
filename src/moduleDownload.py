def download_or_read_file(file_name, path, separator, nrows_value):
    import requests  # Importez requests ici
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
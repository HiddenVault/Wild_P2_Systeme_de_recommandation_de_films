def create_directory(directory_path):
    import os
    os.makedirs(directory_path, exist_ok=True)

def create_csv_directory(directory_path):
    import os
    """
    Crée un répertoire pour stocker les fichiers .csv s'il n'existe pas.
    Args:
        directory_path (str): Le chemin du répertoire.
    """
    os.makedirs(directory_path, exist_ok=True)
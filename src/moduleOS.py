'''
Explications :
1. La fonction `create_directory` prend en paramètre le chemin du répertoire à créer (`directory_path`).
2. La fonction utilise la fonction `makedirs` du module `os` pour créer le répertoire spécifié. 
    L'argument `exist_ok=True` permet d'ignorer les erreurs si le répertoire existe déjà.
3. La fonction `create_csv_directory` fait la même chose que `create_directory`.
'''
# Fonction pour créer un répertoire
def create_directory(directory_path):
    # Importation du module os pour effectuer des opérations sur le système de fichiers
    import os
    # Utilisation de la fonction makedirs de os pour créer le répertoire
    # exist_ok=True permet de ne pas générer d'erreur si le répertoire existe déjà
    os.makedirs(directory_path, exist_ok=True)

# Fonction pour créer un répertoire pour stocker des fichiers CSV
def create_csv_directory(directory_path):
    # Importation du module os pour effectuer des opérations sur le système de fichiers
    import os
    """
    Crée un répertoire pour stocker les fichiers .csv s'il n'existe pas.
    Args:
        directory_path (str): Le chemin du répertoire.
    """
    # Utilisation de la fonction makedirs de os pour créer le répertoire
    # exist_ok=True permet de ne pas générer d'erreur si le répertoire existe déjà
    os.makedirs(directory_path, exist_ok=True)

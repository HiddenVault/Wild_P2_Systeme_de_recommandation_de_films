'''
Explications :
1. get_dataframe_info(df):
   - La fonction `get_dataframe_info` prend un DataFrame (`df`) en entrée.
   - Elle utilise la méthode `info()` de pandas pour obtenir des informations détaillées sur le DataFrame, 
        telles que les types de données, les valeurs non nulles, la consommation de mémoire, etc.
   - Les informations sont capturées en redirigeant la sortie standard vers un objet `StringIO`, puis en restaurant la sortie standard d'origine.
   - Si aucune information n'est disponible, la fonction retourne un message indiquant cela.
2. create_dataframe(content, separator, nrows_value):
   - La fonction `create_dataframe` prend en entrée une chaîne de caractères CSV (`content`), 
        un séparateur de colonnes (`separator`), et le nombre de lignes à lire (`nrows_value`).
   - Elle utilise la bibliothèque pandas pour créer un DataFrame à partir de la chaîne de caractères CSV.
   - En cas d'erreur lors de la lecture du fichier CSV, la fonction imprime l'erreur et retourne `None`.
   - Si la lecture réussit, elle retourne le DataFrame créé.
'''
# Importation du module sys pour accéder à des fonctionnalités spécifiques du système
import sys
# Importation de la bibliothèque pandas sous l'alias 'pd'
import pandas as pd
# Importation de la classe StringIO du module io pour traiter les chaînes de caractères comme des fichiers
from io import StringIO

# Fonction pour obtenir des informations sur un DataFrame
def get_dataframe_info(df):
    # Sauvegarde de la sortie standard actuelle
    original_stdout = sys.stdout
    # Redirection de la sortie standard vers un objet StringIO pour capturer les informations
    sys.stdout = StringIO()
    # Appel à la méthode info() du DataFrame pour obtenir des informations sur sa structure
    df.info()
    # Récupération de la sortie capturée dans la variable info_output
    info_output = sys.stdout.getvalue()
    # Restauration de la sortie standard d'origine
    sys.stdout = original_stdout
    # Si aucune information n'a été capturée, renvoyer un message indiquant l'absence d'informations
    if info_output.strip() == '':
        return "Aucune information disponible"
    # Sinon, renvoyer les informations capturées
    return info_output

# Fonction pour créer un DataFrame à partir d'un contenu CSV
def create_dataframe(content, separator, nrows_value):
    try:
        # Si nrows_value est -1, lire l'intégralité du contenu CSV, sinon lire seulement le nombre de lignes spécifiées dans nrows_value
        if nrows_value == -1:
            df = pd.read_csv(StringIO(content), sep=separator, low_memory=False, encoding='UTF-8')
        else:
            df = pd.read_csv(StringIO(content), sep=separator, nrows=nrows_value, low_memory=False, encoding='UTF-8')
        # Renvoyer le DataFrame créé
        return df
    # Gestion des erreurs liées à la lecture du fichier CSV
    except pd.errors.ParserError as e:
        # Affichage d'un message d'erreur en cas d'échec de la lecture
        print(f"Erreur lors de la lecture du fichier: {e}")
        # Renvoyer None pour indiquer un échec de la création du DataFrame
        return None

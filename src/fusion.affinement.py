'''
Explications :
1. Le code commence par importer la bibliothèque pandas sous l'alias 'pd'.
2. Il spécifie le chemin du fichier CSV à lire (`link`) 
    et ouvre le fichier en tant que DataFrame (`df`) en utilisant `pd.read_csv()`.
3. Les colonnes pour chaque catégorie sont sélectionnées 
    dans des listes distinctes (`selected_columns_ge`, `selected_columns_ti`, etc.).
4. Des préfixes correspondants sont définis pour chaque catégorie (`prefix_ge`, `prefix_ti`, etc.).
5. Les colonnes du DataFrame sont renommées en ajoutant les préfixes appropriés en fonction de leur catégorie.
6. Enfin, le DataFrame modifié est enregistré en tant que fichier CSV sous un nouveau nom (`F2_merged_data.csv`) avec l'encodage 'UTF-8'.
'''

# Importer la bibliothèque pandas sous l'alias 'pd'
import pandas as pd

# Spécifier le chemin du fichier CSV à lire
link = "./data/preparation/F_merged_data.csv"

# Ouvrir le fichier CSV en tant que DataFrame en spécifiant le séparateur (',') et l'encodage ('UTF-8')
# Utiliser low_memory=False pour éviter les avertissements liés à la mémoire lors de la lecture de grands fichiers
df = pd.read_csv(link, sep=',', encoding='UTF-8', low_memory=False)

# Sélectionner les colonnes pour chaque catégorie et ajouter les préfixes correspondants
selected_columns_ge = ['Action', 'Adult', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy', 'Film-Noir', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Sport', 'Thriller', 'War', 'Western']
selected_columns_ti = ['titleType', 'primaryTitle', 'startYear', 'runtimeMinutes', 'poster_path', 'tagline', 'overview']
selected_columns_pe = ['primaryName', 'nconst_tp', 'nconst_nb', 'directors', 'writers']
selected_columns_pk = ['category', 'actor', 'actress', 'animation_department', 'art_department', 'art_director', 'assistant', 'assistant_director', 'camera_department', 'casting_department', 'casting_director', 'cinematographer', 'composer', 'costume_department', 'costume_designer', 'director', 'editor', 'editorial_department', 'electrical_department', 'executive', 'legal', 'location_management', 'make_up_department', 'manager', 'miscellaneous', 'music_artist', 'music_department', 'podcaster', 'producer', 'production_department', 'production_designer', 'production_manager', 'publicist', 'script_department', 'set_decorator', 'sound_department', 'soundtrack', 'special_effects', 'stunts', 'talent_agent', 'transportation_department', 'visual_effects', 'writer']
selected_columns_ra = ['popularity', 'title', 'averageRating', 'numVotes']

# Préfixes à ajouter aux noms de colonnes correspondants à chaque catégorie
prefix_ge = 'GE_'
prefix_ti = 'TI_'
prefix_pe = 'PE_'
prefix_pk = 'PK_'
prefix_ra = 'RA_'

# Renommer les colonnes en ajoutant le préfixe correspondant en fonction de la catégorie de la colonne
df.rename(columns=lambda x: prefix_ge + x if x in selected_columns_ge else
                          prefix_ti + x if x in selected_columns_ti else
                          prefix_pe + x if x in selected_columns_pe else
                          prefix_pk + x if x in selected_columns_pk else
                          prefix_ra + x if x in selected_columns_ra else x, inplace=True)

# Enregistrer le DataFrame final en tant que fichier CSV
df.to_csv('./data/preparation/F2_merged_data.csv', index=False, encoding='UTF-8')

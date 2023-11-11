import pandas as pd

link = "./data/preparation/F_merged_data.csv"

# Ouvrir un dataset en spécifiant le séparateur
df = pd.read_csv(link, sep=',', encoding='UTF-8', low_memory=False)

# Sélectionner les colonnes pour chaque catégorie et ajouter les préfixes
selected_columns_ge = ['Action', 'Adult', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy', 'Film-Noir', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Sport', 'Thriller', 'War', 'Western']
selected_columns_ti = ['titleType', 'primaryTitle', 'startYear', 'runtimeMinutes', 'poster_path', 'tagline', 'overview']
selected_columns_pe = ['primaryName', 'nconst_tp', 'nconst_nb', 'directors', 'writers']
selected_columns_pk = ['category', 'actor', 'actress', 'animation_department', 'art_department', 'art_director', 'assistant', 'assistant_director', 'camera_department', 'casting_department', 'casting_director', 'cinematographer', 'composer', 'costume_department', 'costume_designer', 'director', 'editor', 'editorial_department', 'electrical_department', 'executive', 'legal', 'location_management', 'make_up_department', 'manager', 'miscellaneous', 'music_artist', 'music_department', 'podcaster', 'producer', 'production_department', 'production_designer', 'production_manager', 'publicist', 'script_department', 'set_decorator', 'sound_department', 'soundtrack', 'special_effects', 'stunts', 'talent_agent', 'transportation_department', 'visual_effects', 'writer']
selected_columns_ra = ['popularity', 'title', 'averageRating', 'numVotes']

# Préfixe à ajouter aux noms de colonnes
prefix_ge = 'GE_'
prefix_ti = 'TI_'
prefix_pe = 'PE_'
prefix_pk = 'PK_'
prefix_ra = 'RA_'

# Renommer les colonnes en ajoutant le préfixe
df.rename(columns=lambda x: prefix_ge + x if x in selected_columns_ge else
                          prefix_ti + x if x in selected_columns_ti else
                          prefix_pe + x if x in selected_columns_pe else
                          prefix_pk + x if x in selected_columns_pk else
                          prefix_ra + x if x in selected_columns_ra else x, inplace=True)

# Enregistrer le DataFrame final en tant que fichier CSV
df.to_csv('./data/preparation/F2_merged_data.csv', index=False, encoding='UTF-8')


'''
Explications :
Le script permet de déterminer le nombre optimal de clusters pour un dataframe en utilisant :
    - K-Means, 
    - la méthode du coude,
    - le score de la silhouette. 
1. Chargement du dataframe à partir d'un fichier CSV.
2. Sélection des colonnes numériques du DataFrame pour le clustering.
3. Boucle pour stocker l'inertie et le score de la silhouette dans des listes.
4. Détermination du nombre optimal de clusters (méthode du coude)
5. Tracé du graphique avec deux axes (inertie & score)
6. Création d'une légende combinant les légendes des deux graphiques pour les deux graphiques avec Line2D
7. Affichage du graphique
'''


import warnings
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score  # Pour gérer le score de silhouette
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D  # permet la création des lignes personnalisées dans les graphiques

# Les avertissements de type FutureWarning sont ignorés
with warnings.catch_warnings():
    warnings.simplefilter(action='ignore', category=FutureWarning)

    df = pd.read_csv('http://hiddenvault.fr/P2_Systeme_de_recommandation_de_films/ML_F2_merged_data_v3.csv', sep=',', encoding='UTF-8', low_memory=False)

    # Sélection des colonnes numériques du DataFrame
    numeric_columns = df.select_dtypes(include=['float64', 'int64'])

    # Initialisation des listes pour stocker les résultats du clustering pour les différentes valeurs de k
    list_k = [] 
    list_inertie = []  # Liste pour stocker l'inertie du modèle K-Means
    list_score = []  # Liste pour stocker le score de silhouette

    # On boucle sur les différentes valeurs de k pour le modèle K-Means
    for k in range(2, 30):
        # Initialisation du modèle K-Means avec un certain nombre de clusters (k)
        modelKM = KMeans(n_clusters=k)  
        # On adapter le modèle aux données
        modelKM.fit(numeric_columns)  

        # Ajoutdes des résultats aux listes
        list_k.append(k)
        # Inertie du modèle K-Means
        list_inertie.append(modelKM.inertia_) 
        # Score de silhouette
        list_score.append(silhouette_score(numeric_columns, modelKM.labels_))  

# Fonction pour trouver le nombre optimal de clusters en utilisant la méthode du coude
def find_optimal_k(list_k, list_inertie):
    deltas = [list_inertie[i] - list_inertie[i - 1] for i in range(1, len(list_inertie))]
    acceleration = [deltas[i] - deltas[i - 1] for i in range(1, len(deltas))]
    
    # Indice du coude (là où l'accélération est maximale)
    optimal_k_index = acceleration.index(max(acceleration)) + 1
    
    return list_k[optimal_k_index]

# Fonction pour trouver le nombre optimal de clusters (optimal_k)
optimal_k = find_optimal_k(list_k, list_inertie)

# Création d'un graphique avec deux axes partageant l'axe x
fig, ax1 = plt.subplots(figsize=(10, 6))

# Méthode du Coude pour déterminer le nombre optimal de clusters
line1 = ax1.plot(list_k, list_inertie, 'b-', label='Inertie')  # Tracer l'inertie en fonction de k
line2 = ax1.axvline(x=optimal_k, color='k', linestyle='--', label='Optimal k')  # Ligne verticale pour indiquer le nombre optimal de clusters
ax1.text(optimal_k + 0.1, max(list_inertie) - 5000, f'Optimal k = {optimal_k}', color='k')  # Texte indiquant le nombre optimal de clusters
plt.xlabel('Nombre de Clusters (k)')
plt.ylabel('Inertie')

# Création d'un deuxième axe y en partageant le même axe x que le premier
ax2 = ax1.twinx()
line3 = ax2.plot(list_k, list_score, 'r-', label='Silhouette Score')  # Traçage de la courbe de score en fonction de k
plt.ylabel('Score')

# Fusion des labels descriptifs en une seule liste pour la légende
combined_lines = [Line2D([0], [0], color='b', label='Inertie'),
                  Line2D([0], [0], color='k', linestyle='--', label='Optimal k'),
                  Line2D([0], [0], color='r', label='Silhouette Score')]

combined_labels = [label.get_label() for label in combined_lines]

# Ajout de la légende avec les labels combinés sur le premier axe
ax1.legend(combined_lines, combined_labels, loc='upper right')

# Affichage du graphique
plt.show()

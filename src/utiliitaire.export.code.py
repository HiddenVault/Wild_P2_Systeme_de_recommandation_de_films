'''
Explications  :
1. Le script commence par définir le chemin du dossier contenant 
    les fichiers (`dossier_scripts`) et 
    la liste des noms de fichiers à traiter (`noms_de_fichiers`).
2. Il ouvre un fichier de sortie (`exported_scripts.txt`) en mode écriture, 
    pour stocker les informations extraites des scripts.
3. Ensuite, pour chaque nom de fichier dans la liste, il construit le chemin complet en utilisant `os.path.join` .
4. Dans un bloc `try-except`, le script tente d'ouvrir chaque fichier, lit son contenu, 
    puis écrit le nom du script suivi de son contenu dans le fichier de sortie.
5. Si un fichier n'est pas trouvé (lève une exception `FileNotFoundError`), 
    le script affiche un message indiquant que le fichier n'a pas été trouvé dans le dossier spécifié.
6. Le script affiche "Exportation terminée" une fois que toutes les opérations sont effectuées avec succès.
'''

import os

# Dossier contenant les fichiers
dossier_scripts = "./src"

# Liste des noms de fichiers
noms_de_fichiers = ["preparation.title.basics.csv.py","moduleCSV.py"]

# Ouvrir un fichier de sortie en mode écriture
with open("exported_scripts.txt", "w") as fichier_export:

    # Parcours de la liste des noms de fichiers
    for nom_fichier in noms_de_fichiers:
        chemin_complet = os.path.join(dossier_scripts, nom_fichier)

        try:
            # Ouvrerture du fichier en mode lecture
            with open(chemin_complet, "r") as fichier_source:
                # Lecture du contenu du fichier
                contenu = fichier_source.read()

            # Écriture du nom du script dans le fichier de sortie
            fichier_export.write(f"Nom du script : {nom_fichier}\n")
            
            # Écriture du contenu du script dans le fichier de sortie
            fichier_export.write("Contenu du script :\n")
            fichier_export.write(contenu)
            fichier_export.write("\n\n")

        except FileNotFoundError:
            print(f"Le fichier {nom_fichier} n'a pas été trouvé dans le dossier {dossier_scripts}.")

print("Exportation terminée.")

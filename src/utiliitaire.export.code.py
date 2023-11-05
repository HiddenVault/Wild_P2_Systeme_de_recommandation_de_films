import os

# Dossier contenant les fichiers
dossier_scripts = "E:/Users/jefferson/Documents/Formation/Data Analyst/Projet/Projet 2 - Recommandation de films/draft"

# Liste des noms de fichiers
noms_de_fichiers = ["preparation.title.basics.csv.py","moduleCSV.py"]


# Ouvrir un fichier de sortie en mode écriture
with open("exported_scripts.txt", "w") as fichier_export:

    # Parcourir la liste des noms de fichiers
    for nom_fichier in noms_de_fichiers:
        chemin_complet = os.path.join(dossier_scripts, nom_fichier)

        try:
            # Ouvrir le fichier en mode lecture
            with open(chemin_complet, "r") as fichier_source:
                # Lire le contenu du fichier
                contenu = fichier_source.read()

            # Écrire le nom du script dans le fichier de sortie
            fichier_export.write(f"Nom du script : {nom_fichier}\n")
            
            # Écrire le contenu du script dans le fichier de sortie
            fichier_export.write("Contenu du script :\n")
            fichier_export.write(contenu)
            fichier_export.write("\n\n")

        except FileNotFoundError:
            print(f"Le fichier {nom_fichier} n'a pas été trouvé dans le dossier {dossier_scripts}.")

print("Exportation terminée.")


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

'''
Explications  :
1. Le script définit un dictionnaire (`files_to_process`) contenant des informations sur les scripts à traiter, 
    notamment s'ils doivent être traités, le mode d'exécution, et leur numéro d'ordre.
2. Les scripts sont triés en fonction de leur ordre d'exécution.
3. Ensuite, le script parcourt les scripts triés et exécute chaque script selon ses propriétés. 
    On peut utiliser `subprocess.run` ou `subprocess.Popen` pour lancer les scripts Python.
4. Le script affiche des messages sur le début et la fin de l'exécution de chaque script.
'''

import subprocess

# Dictionnaire définissant les scripts à traiter avec leurs propriétés associées
files_to_process = {
    "./src/preparation.complementaire_tmdb_full.csv.py": {"process": True, "execution_mode": "run", "order": 1},
    "./src/preparation.name.basics.csv.py": {"process": True, "execution_mode": "run", "order": 2},
    "./src/preparation.title.akas.csv.py": {"process": True, "execution_mode": "run", "order": 3},
    "./src/preparation.title.basics.csv.py": {"process": True, "execution_mode": "run", "order": 4},
    "./src/preparation.title.crew.csv.py": {"process": True, "execution_mode": "run", "order": 5},
    "./src/preparation.title.episode.csv.py": {"process": True, "execution_mode": "run", "order": 6},
    "./src/preparation.titles.principals.csv.py": {"process": True, "execution_mode": "run", "order": 7},
    "./src/preparation.title.ratings.csv.py": {"process": True, "execution_mode": "run", "order": 8},
    "./src/fusion.dataframes.py": {"process": True, "execution_mode": "run", "order": 9}
}

# Triage des scripts en fonction de leur numéro d'ordre.
sorted_scripts = sorted(files_to_process.items(), key=lambda x: x[1]["order"])

# Parcours des scripts triés et exécution en fonction de leurs propriétés.
for script_name, script_info in sorted_scripts:
    if script_info["process"]:
        try:
            # Affiche un message indiquant le début de l'exécution du script.
            print(f"Début de l'exécution du script {script_name} en mode '{script_info['execution_mode']}'.")
            
            # Vérifie le mode d'exécution et exécute le script en conséquence.
            if script_info["execution_mode"] == "run":
                # Exécution du script en utilisant subprocess.run.
                subprocess.run(["python", script_name])
            elif script_info["execution_mode"] == "Popen":
                # Exécution du script en utilisant subprocess.Popen.
                subprocess.Popen(["python", script_name])
            
            # Affiche un message indiquant la fin de l'exécution du script.
            print(f"Fin de l'exécution du script {script_name}.")
        
        except subprocess.CalledProcessError as e:
            # Gestion des erreurs lors de l'exécution des scripts.
            print(f"Erreur lors de l'exécution de {script_name}: {e}")
    
    else:
        # Si le script ne doit pas être traité, affiche un message correspondant.
        print(f"Le script {script_name} ne doit pas être traité.")

import subprocess

files_to_process = {
    "./draft/preparation.complementaire_tmdb_full.csv.py": {"process": True, "execution_mode": "run", "order": 1},
    "./draft/preparation.name.basics.csv.py": {"process": True, "execution_mode": "run", "order": 2},
    "./draft/preparation.title.akas.csv.py": {"process": True, "execution_mode": "run", "order": 3},
    "./draft/preparation.title.basics.csv.py": {"process": True, "execution_mode": "run", "order": 4},
    "./draft/preparation.title.crew.csv.py": {"process": True, "execution_mode": "run", "order": 5},
    "./draft/preparation.title.episode.csv.py": {"process": True, "execution_mode": "run", "order": 6},
    "./draft/preparation.titles.principals.csv.py": {"process": True, "execution_mode": "run", "order": 7},
    "./draft/preparation.title.ratings.csv.py": {"process": True, "execution_mode": "run", "order": 8},
    "./draft/fusion.dataframes.py": {"process": True, "execution_mode": "run", "order": 9}
}

# Triage des scripts en fonction de leur numéro d'ordre.
sorted_scripts = sorted(files_to_process.items(), key=lambda x: x[1]["order"])

# Parcourez les scripts triés et exécutez-les en fonction de leurs propriétés.
for script_name, script_info in sorted_scripts:
    if script_info["process"]:
        try:
            print(f"Début de l'exécution du script {script_name} en mode '{script_info['execution_mode']}'.")
            if script_info["execution_mode"] == "run":
                # Exécution du script en utilisant subprocess.run.
                subprocess.run(["python", script_name])
            elif script_info["execution_mode"] == "Popen":
                # Exécution du script en utilisant subprocess.Popen.
                subprocess.Popen(["python", script_name])
            print(f"Fin de l'exécution du script {script_name}.")
        except subprocess.CalledProcessError as e:
            print(f"Erreur lors de l'exécution de {script_name}: {e}")
    else:
        print(f"Le script {script_name} ne doit pas être traité.")

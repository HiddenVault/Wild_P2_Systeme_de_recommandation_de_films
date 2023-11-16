'''
Explications  :
1. La fonction `upload_file_to_ftp` prend en paramètre le chemin local du fichier à transférer (`local_file_path`), 
    le chemin distant où le fichier sera stocké sur le serveur FTP (`remote_file_path`), et un objet FTP préalablement configuré (`ftp`).
2. La fonction utilise la commande FTP `STOR` pour transférer le fichier vers le serveur FTP. 
   La méthode `storbinary` est utilisée pour effectuer cette opération. 
   Le mode 'rb' est utilisé lors de l'ouverture du fichier local pour s'assurer que le transfert est effectué en mode binaire.
3. Cette fonction est utile lorsque l'on a un fichier local que l'on souhaite le transférer vers un serveur FTP distant. 
   Elle facilite le processus de mise à jour de fichiers sur le serveur distant à partir d'une machine locale.
'''

# Fonction pour transférer un fichier vers le serveur FTP
def upload_file_to_ftp(local_file_path, remote_file_path, ftp):
    # Ouvrir le fichier local en mode lecture binaire ('rb')
    with open(local_file_path, 'rb') as local_file:
        # Utiliser la méthode storbinary() de l'objet FTP pour transférer le fichier
        # 'STOR' est une commande FTP qui signifie "Store a file on the remote machine."
        # Elle est suivie du chemin distant et du fichier local à stocker
        ftp.storbinary('STOR ' + remote_file_path, local_file)

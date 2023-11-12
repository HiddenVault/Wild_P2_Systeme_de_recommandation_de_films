# Fonction pour transférer un fichier vers le serveur FTP
def upload_file_to_ftp(local_file_path, remote_file_path, ftp):
    # Ouvrir le fichier local en mode lecture binaire ('rb')
    with open(local_file_path, 'rb') as local_file:
        # Utiliser la méthode storbinary() de l'objet FTP pour transférer le fichier
        # 'STOR' est une commande FTP qui signifie "Store a file on the remote machine."
        # Elle est suivie du chemin distant et du fichier local à stocker
        ftp.storbinary('STOR ' + remote_file_path, local_file)

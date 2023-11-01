# Fonction pour transférer un fichier vers le serveur FTP
def upload_file_to_ftp(local_file_path, remote_file_path, ftp):
    with open(local_file_path, 'rb') as local_file:
        ftp.storbinary('STOR ' + remote_file_path, local_file)
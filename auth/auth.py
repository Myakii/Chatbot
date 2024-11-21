import os
import pickle
import google.auth
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

# Si modifie les autorisations, supprime le fichier token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def authenticate_google_account():
    """Authentification via OAuth 2.0 pour accéder à Google Drive."""
    creds = None
    # Le fichier token.pickle stocke l'accès de l'utilisateur et les informations de rafraîchissement.
    # Il est créé automatiquement lors du processus d'authentification initial.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # Si il n'y a pas de (valid) credentials, demande à l'utilisateur de se connecter.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)

        # Sauvegarde les informations d'authentification pour les futures utilisations
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('drive', 'v3', credentials=creds)

def download_file_from_drive(file_id, destination):
    """Télécharge un fichier de Google Drive."""
    service = authenticate_google_account()
    request = service.files().get_media(fileId=file_id)
    with open(destination, 'wb') as f:
        downloader = MediaIoBaseDownload(f, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(f'Download {int(status.progress() * 100)}%.')

import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# Définir les scopes nécessaires pour accéder à Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def authenticate_google_drive():
    """Authentifier l'utilisateur et retourner le service Google Drive."""
    creds = None
    # Le fichier token.pickle contient les informations d'identification de l'utilisateur. Création automatique
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # Si les informations d'identification ne sont pas valides ou absentes, demandez à l'utilisateur de se connecter.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Sauvegarder les informations d'identification dans token.pickle pour une utilisation future
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Construire le service Google Drive
    service = build('drive', 'v3', credentials=creds)
    return service


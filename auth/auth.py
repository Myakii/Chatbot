from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
import pickle
from google.auth.transport.requests import Request

# Les informations d'authentification (ID client et secret) se trouvent dans credentials.json
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def authenticate_google_drive():
    """Authentifie l'utilisateur et retourne un service Google Drive."""
    
    creds = None
    # Le fichier token.pickle contient les jetons d'accès et de rafraîchissement pour l'utilisateur.
    # Il est créé automatiquement lors de l'authentification initiale.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # Si les informations d'identification sont invalides ou inexistantes, l'utilisateur doit se reconnecter.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Demande une nouvelle authentification via OAuth2
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Sauvegarde les informations d'identification pour la prochaine exécution.
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    # Retourne le service Google Drive authentifié
    service = build('drive', 'v3', credentials=creds)
    return service

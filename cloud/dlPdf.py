import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError

# Définir les scopes d'autorisation (Accès à Google Drive)
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def authenticate_google_drive():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds

def download_file_from_drive(file_id, file_name):
    try:
        creds = authenticate_google_drive()
        service = build('drive', 'v3', credentials=creds)

        # Téléchargement du fichier
        request = service.files().get_media(fileId=file_id)
        fh = open(file_name, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}%.")
        print(f"File {file_name} downloaded successfully.")

    except HttpError as error:
        print(f'An error occurred: {error}')

if __name__ == '__main__':
    # Remplace 'file_id_here' par l'ID réel de ton fichier sur Google Drive
    download_file_from_drive('file_id_here', 'Races_de_chiens_pour_appartement.pdf')

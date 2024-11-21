# import os
# import requests
# import PyPDF2
# from auth.auth import download_file_from_drive

# # Lire le fichier PDF
# def read_pdf(file_path):
#     with open(file_path, 'rb') as file:
#         reader = PyPDF2.PdfReader(file)
#         text = ''
#         for page in range(len(reader.pages)):
#             text += reader.pages[page].extract_text()
#     return text

# # Fonction pour interroger Ollama avec un prompt
# def ask_ollama(prompt):
#     url = "http://localhost:11434/api/generate"  # Assure-toi que Ollama est démarré
#     headers = {"Content-Type": "application/json"}
#     payload = {"model": "llama2", "prompt": prompt}

#     response = requests.post(url, json=payload, headers=headers)
#     return response.json().get('choices')[0].get('text')

# # Extraire le contenu du PDF
# pdf_content = read_pdf(file_path)

# # Crée un prompt basé sur la question et le contenu du PDF
# question = "Comment vivre en appartement avec un chien?"
# prompt = f"{question}\nVoici le contenu du fichier PDF sur la question :\n{pdf_content}"

# # Interroger Ollama
# response = ask_ollama(prompt)
# print("Réponse d'Ollama : ", response)

import os
import io
import PyPDF2
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from auth.auth import download_file_from_drive

# Variables globales
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
TOKEN_FILE = 'token.json'  # Token de session
CREDENTIALS_FILE = 'credentials.json'  # Fichier client OAuth 2.0
DRIVE_API = None

# ID du fichier Google Drive (assure-toi de le remplacer par l'ID réel du PDF)
file_id = '15eS8loNmhSomZisKxET1fPOUUl5OAVsh?usp=drive_link'
file_path = 'vivre_en_appartement_avec_chien.pdf'

# Télécharger le fichier PDF de Google Drive
download_file_from_drive(file_id, file_path)

def download_file_from_drive():
    """Authentifie l'utilisateur avec OAuth 2.0 et récupère l'API Drive."""
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=8080)
        
        # Sauvegarder les nouveaux credentials
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    
    global DRIVE_API
    DRIVE_API = build('drive', 'v3', credentials=creds)

def search_pdf_in_drive(query):
    """Recherche un fichier PDF dans Google Drive basé sur la requête utilisateur."""
    results = DRIVE_API.files().list(q=f"name contains '{query}' and mimeType='application/pdf'",
                                      fields="files(id, name)").execute()
    files = results.get('files', [])
    if not files:
        return None
    return files[0]  # Retourne le premier fichier trouvé

def download_pdf(file_id, file_name):
    """Télécharge le fichier PDF à partir de Google Drive."""
    request = DRIVE_API.files().get_media(fileId=file_id)
    fh = io.FileIO(file_name, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    print(f"Fichier {file_name} téléchargé.")

def extract_text_from_pdf(file_path):
    """Extrait le texte d'un PDF donné."""
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

def send_text_to_ollama(text):
    """Envoie le texte à Ollama pour analyse et renvoie la réponse."""
    # Remplace par la logique d'intégration Ollama
    # Par exemple : appel HTTP à Ollama API
    # Implémente ici la logique pour poser la question à Ollama et obtenir une réponse
    response = ollama_query(text)  # Logique d'appel à Ollama (exemple)
    return response

def list_files_from_drive(service):
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)"
    ).execute()
    items = results.get('files', [])

    if not items:
        print("Aucun fichier trouvé.")
    else:
        print("Fichiers dans le Drive :")
        for item in items:
            print(f"Nom : {item['name']}, ID : {item['id']}")


def main():
    """Exécution principale."""
    download_file_from_drive()  # Authentifie l'utilisateur
    query = "vivre en appartement avec un chien"  # Exemple de question de l'utilisateur
    file = search_pdf_in_drive(query)  # Recherche un fichier correspondant
    if file:
        print(f"Fichier trouvé: {file['name']}")
        download_pdf(file['id'], file['name'])  # Télécharge le PDF
        text = extract_text_from_pdf(file['name'])  # Extrait le texte du PDF
        print(f"Texte extrait du fichier: {text[:200]}...")  # Affiche une partie du texte extrait
        response = send_text_to_ollama(text)  # Envoie à Ollama pour réponse
        print(f"Réponse d'Ollama: {response}")
    else:
        print("Aucun fichier trouvé.")

if __name__ == '__main__':
    main()

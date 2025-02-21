from fuzzywuzzy import fuzz
import os
import PyPDF2
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Variables globales
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
TOKEN_FILE = 'token.json'
CREDENTIALS_FILE = 'credentials.json'
DRIVE_API = None

def authenticate_drive():
    """Authentifie l'utilisateur et initialise l'API Google Drive."""
    global DRIVE_API
    creds = None
    if not os.path.exists(CREDENTIALS_FILE):
        print("Fichier credentials.json manquant. Assure-toi d'avoir les bonnes informations d'authentification.")
        exit()

    if os.path.exists(TOKEN_FILE):
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        except Exception as e:
            print("Erreur avec le token existant :", e)
            creds = None  

    if not creds or not creds.valid: 
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
        creds = flow.run_local_server(port=8080)
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    DRIVE_API = build('drive', 'v3', credentials=creds)

def search_pdf_in_drive(query):
    """Recherche un fichier PDF dans Google Drive, en explorant aussi les dossiers si nécessaire."""
    keywords = query.lower().split()  

    # 1️⃣ Cherche les fichiers PDF directement
    results = DRIVE_API.files().list(
        q="mimeType='application/pdf'",
        fields="files(id, name, parents)"
    ).execute()
    
    files = results.get('files', [])
    
    for file in files:
        file_name = file['name'].lower()
        if all(keyword in file_name for keyword in keywords):
            return file  

    # 2️⃣ Si aucun fichier trouvé, cherche dans les dossiers
    folder_results = DRIVE_API.files().list(
        q="mimeType='application/vnd.google-apps.folder'",
        fields="files(id, name)"
    ).execute()
    
    folders = folder_results.get('files', [])
    
    for folder in folders:
        folder_id = folder['id']
        folder_name = folder['name'].lower()
        
        # Vérifie si le dossier correspond aux mots-clés
        if all(keyword in folder_name for keyword in keywords):
            sub_results = DRIVE_API.files().list(
                q=f"'{folder_id}' in parents and mimeType='application/pdf'",
                fields="files(id, name)"
            ).execute()
            
            sub_files = sub_results.get('files', [])
            if sub_files:
                return sub_files[0] 

    return None 

def download_pdf(file_id, file_name):
    """Télécharge le fichier PDF à partir de Google Drive."""
    request = DRIVE_API.files().get_media(fileId=file_id)
    with open(file_name, 'wb') as f:
        downloader = MediaIoBaseDownload(f, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"Téléchargement : {int(status.progress() * 100)}%")
    print(f"Fichier {file_name} téléchargé.")

def extract_text_from_pdf(file_path):
    """Extrait le texte d'un PDF donné."""
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or "" 
    return text

def fuzzy_search_text(text, query):
    """Recherche floue pour trouver des phrases ou des termes pertinents dans le texte."""
    sentences = text.split(".")  
    best_match = ""
    highest_score = 0
    for sentence in sentences:
        score = fuzz.partial_ratio(query.lower(), sentence.lower()) 
        if score > highest_score:
            highest_score = score
            best_match = sentence.strip()
    return best_match, highest_score

def main():
    authenticate_drive()
    query = input("Entrez le nom ou mot-clé du PDF à rechercher : ")
    file = search_pdf_in_drive(query)
    if file:
        print(f"Fichier sélectionné : {file['name']}")
        download_pdf(file['id'], file['name'])
        text = extract_text_from_pdf(file['name'])
        print("\n--- Contenu extrait du PDF ---\n")
        print(text)
        
        while True:
            question = input("Posez une question sur le contenu du PDF (ou tapez 'exit' pour quitter) : ")
            if question.lower() == 'exit':
                break
            
            best_match, score = fuzzy_search_text(text, question)
            if best_match:
                print(f"\n--- Réponse ---")
                print(f"Meilleure correspondance : {best_match}")
                print(f"Score de correspondance : {score}%\n")
            else:
                print("Aucune correspondance trouvée dans le texte.")
    else:
        print("Aucun fichier correspondant trouvé ou aucune sélection valide.")

if __name__ == '__main__':
    main()

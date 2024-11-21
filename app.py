import os
import io
import PyPDF2
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import requests

# Variables globales
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
TOKEN_FILE = 'token.json'  # Token de session
CREDENTIALS_FILE = 'credentials.json'  # Fichier client OAuth 2.0
DRIVE_API = None

def authenticate_to_drive():
    """Authentifie l'utilisateur avec OAuth 2.0 et initialise l'API Google Drive."""
    global DRIVE_API
    creds = None

    # Chargement des credentials existants
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    # Si les credentials sont invalides ou inexistants, exécute le flux OAuth
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=8080)
        
        # Sauvegarder les nouveaux credentials
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    
    DRIVE_API = build('drive', 'v3', credentials=creds)
    print("Authentification réussie.")

def search_pdf_in_drive(query):
    """Recherche un fichier PDF dans Google Drive basé sur une requête."""
    if not DRIVE_API:
        raise RuntimeError("L'API Drive n'est pas initialisée. Veuillez exécuter `authenticate_to_drive`.")
    
    results = DRIVE_API.files().list(
        q=f"name contains '{query}' and mimeType='application/pdf'",
        fields="files(id, name)"
    ).execute()
    files = results.get('files', [])
    if not files:
        print("Aucun fichier trouvé.")
        return None
    return files[0]  # Retourne le premier fichier trouvé

def download_file_from_drive(file_id, file_path):
    """Télécharge un fichier PDF depuis Google Drive."""
    if not DRIVE_API:
        raise RuntimeError("L'API Drive n'est pas initialisée. Veuillez exécuter `authenticate_to_drive`.")
    
    request = DRIVE_API.files().get_media(fileId=file_id)
    with open(file_path, 'wb') as f:
        downloader = MediaIoBaseDownload(f, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"Téléchargement en cours : {int(status.progress() * 100)}%")
    print(f"Fichier téléchargé avec succès : {file_path}")

def extract_text_from_pdf(file_path):
    """Extrait le texte d'un fichier PDF."""
    try:
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier PDF : {e}")
        return ""

def save_text_to_file(text, txt_file_path):
    """Sauvegarde le texte extrait dans un fichier .txt."""
    try:
        with open(txt_file_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Texte extrait sauvegardé dans : {txt_file_path}")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde du fichier texte : {e}")

def ask_ollama(prompt):
    """Interroge Ollama avec un prompt spécifique."""
    url = "http://localhost:11434/api/generate"  # Assure-toi que Ollama est démarré
    headers = {"Content-Type": "application/json"}
    payload = {"model": "llama2", "prompt": prompt}

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json().get('choices')[0].get('text')
    except requests.RequestException as e:
        print(f"Erreur lors de l'interrogation d'Ollama : {e}")
        return "Erreur lors de la génération de la réponse."

def main():
    """Exécution principale."""
    # Authentification à Google Drive
    authenticate_to_drive()

    # Recherche du fichier PDF
    query = "vivre en appartement avec un chien"
    file_info = search_pdf_in_drive(query)

    if not file_info:
        print("Aucun fichier correspondant n'a été trouvé.")
        return

    print(f"Fichier trouvé : {file_info['name']} (ID : {file_info['id']})")
    
    # Téléchargement du fichier
    file_path = file_info['name']
    download_file_from_drive(file_info['id'], file_path)

    # Extraction du texte du PDF
    pdf_text = extract_text_from_pdf(file_path)
    if not pdf_text:
        print("Aucun texte n'a pu être extrait du fichier PDF.")
        return

    # Sauvegarder le texte en tant que fichier .txt
    txt_file_path = os.path.splitext(file_path)[0] + '.txt'
    save_text_to_file(pdf_text, txt_file_path)

    # Interrogation d'Ollama
    question = "Comment vivre en appartement avec un chien ?"
    prompt = f"{question}\nVoici le contenu du fichier PDF :\n{pdf_text[:3000]}"  # Limite à 3000 caractères pour éviter les dépassements
    response = ask_ollama(prompt)

    print("Réponse d'Ollama :", response)

if __name__ == '__main__':
    main()

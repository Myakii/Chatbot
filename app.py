from auth.auth import authenticate_google_drive
from utils.download import download_file
from utils.text_extraction import extract_text_from_pdf
from models.rag_model import initialize_model, generate_response

def main():
    # Authentifie l'utilisateur et obtient le service Google Drive
    service = authenticate_google_drive()
    
    # Exemple de téléchargement d'un fichier depuis Google Drive
    file_id = '1V7yXvWqD5eB6V6Lg8wP7tPm5RQ6k1zTx'  # Remplace par un ID de fichier réel
    download_file(file_id, service)

    # Extraire le texte du fichier PDF téléchargé
    text = extract_text_from_pdf('downloaded_file.pdf')
    
    # Initialiser et utiliser le modèle RAG pour générer une réponse basée sur le texte extrait
    model = initialize_model()
    prompt = f"Peux-tu me résumer ce texte ? {text}"
    response = generate_response(prompt, model)
    
    # Afficher la réponse générée
    print(response)

if __name__ == '__main__':
    main()

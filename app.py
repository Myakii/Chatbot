import os
import requests
import PyPDF2
from auth.auth import download_file_from_drive

# ID du fichier Google Drive (assure-toi de le remplacer par l'ID réel du PDF)
file_id = 'votre_fichier_id_google_drive'
file_path = 'Races_de_chiens_pour_appartement.pdf'

# Télécharger le fichier PDF de Google Drive
download_file_from_drive(file_id, file_path)

# Lire le fichier PDF
def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in range(len(reader.pages)):
            text += reader.pages[page].extract_text()
    return text

# Fonction pour interroger Ollama avec un prompt
def ask_ollama(prompt):
    url = "http://localhost:11434/api/generate"  # Assure-toi que Ollama est démarré
    headers = {"Content-Type": "application/json"}
    payload = {"model": "llama2", "prompt": prompt}

    response = requests.post(url, json=payload, headers=headers)
    return response.json().get('choices')[0].get('text')

# Extraire le contenu du PDF
pdf_content = read_pdf(file_path)

# Crée un prompt basé sur la question et le contenu du PDF
question = "Comment vivre en appartement avec un chien?"
prompt = f"{question}\nVoici le contenu du fichier PDF sur la question :\n{pdf_content}"

# Interroger Ollama
response = ask_ollama(prompt)
print("Réponse d'Ollama : ", response)

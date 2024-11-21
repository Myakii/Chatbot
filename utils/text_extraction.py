from PyPDF2 import PdfReader

def extract_text_from_pdf(file_path):
    """Extrait le texte d'un fichier PDF."""
    
    with open(file_path, 'rb') as file:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

import pdfplumber

def extract_text_from_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

pdf_text = extract_text_from_pdf('Races_de_chiens_pour_appartement.pdf')
print(pdf_text[:1000])  # Affiche les 1000 premiers caractères du texte extrait

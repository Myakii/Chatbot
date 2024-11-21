import re

def chatbot_response(query, pdf_text):
    # Recherche des mots-clés dans le texte extrait du PDF
    if re.search(r'chien.*appartement', query, re.IGNORECASE):
        return pdf_text  # Retourne tout le texte extrait, tu peux affiner selon la question
    
    return "Je n'ai pas trouvé de réponse dans le document."

# Exemple d'utilisation
query = "comment vivre avec un chien en appartement"
response = chatbot_response(query, pdf_text)
print(response[:500])  # Affiche les 500 premiers caractères de la réponse

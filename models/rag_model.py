# Ce fichier va contenir la logique pour utiliser ton modèle LLM
from transformers import pipeline

# Par exemple, tu peux utiliser Hugging Face pour charger un modèle
def initialize_model():
    # Initialiser ton modèle RAG (si tu utilises un modèle LLM Hugging Face)
    model = pipeline("text-generation", model="gpt2")
    return model

def generate_response(prompt, model):
    # Utilise ton modèle pour générer une réponse
    response = model(prompt, max_length=100, num_return_sequences=1)
    return response[0]['generated_text']

# Chatbot avec Google Drive

## Description
Ce projet permet de récupérer des documents depuis Google Drive et d'utiliser un modèle de langage pour générer des réponses à partir de ces documents en utilisant la technique RAG (Retrieval-Augmented Generation).

## Pré-requis
- Python 3.7 ou supérieur
- Créer un projet sur [Google Cloud Console](https://console.cloud.google.com/) et activer l'API Google Drive.
- Télécharger le fichier `credentials.json` et le placer dans le répertoire principal du projet.

## Installation
1. Cloner ce dépôt.
2. Installer les dépendances : `pip install -r requirements.txt`.
3. Exécuter le script avec `python app.py`.

## Fonctionnement
L'application télécharge un fichier depuis Google Drive, en extrait le texte et génère une réponse à l'aide d'un modèle de langage.


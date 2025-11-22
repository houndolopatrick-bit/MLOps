import streamlit as st
from PIL import Image
import requests

st.set_page_config(
    page_title="Cat vs Dog Classifier",
    page_icon=":cat: :dog:",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.title("Cat vs Dog Classifier :cat: :dog:")

st.markdown(
    """
    <style>
    .main {
        background-color: #f5f5f5;
        padding: 2rem;
        border-radius: 1rem;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }
    .sidebar .sidebar-content {
        background-color: #fff;
        border-right: 1px solid #ddd;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
"""unsafe_allow_html=True est un paramètre utilisé dans Streamlit, une bibliothèque Python pour créer des interfaces web interactives. 
Ce paramètre est utilisé avec la fonction st.markdown() ou st.write() pour autoriser du code HTML brut dans l’application.
"""

upload = st.file_uploader("Upload an image of a cat or dog", type=['png', 'jpg', 'jpeg'])
"""La fonction requests.post() en Python sert à envoyer une requête HTTP POST à un serveur web. C’est une méthode de la bibliothèque requests, très utilisée pour interagir avec des APIs.

📬 Que fait requests.post() exactement ?
Elle envoie des données (texte, JSON, fichiers, etc.) à une URL donnée, généralement pour :
- Créer une ressource (ex : un nouvel utilisateur)
- Envoyer un fichier
- Lancer une prédiction (dans le cas d’un modèle ML)
- Soumettre un formulaire
req.json()
- Récupère la réponse du serveur sous forme de dictionnaire Python
- Cela suppose que le serveur FastAPI renvoie une réponse au format JSON, comme :

"""
if upload: # permet d'appliquer un bloc d'instructions à condition que la variable existe
    files = {"file": upload.getvalue()}

    with st.spinner("Analyzing the image..."):
        req = requests.post("http://127.0.0.1:8000/predict", files=files)
        resultat = req.json()
        prob_cat = resultat["cat_proba"] * 100
        prob_dog = resultat["dog_proba"] * 100

    st.image(Image.open(upload), caption="Uploaded Image", use_column_width=True)

    st.subheader("Prediction Results")
    if prob_cat > prob_dog:
        st.markdown(
            f"""
            <div style='padding: 2rem; background-color: #f8d7da; border-left: 5px solid #dc3545;'>
            <h2 style='color: #721c24;'>Cat</h2>
            <p>I am <strong>{prob_cat:.2f}%</strong> certain this is a cat.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div style='padding: 2rem; background-color: #d4edda; border-left: 5px solid #28a745;'>
            <h2 style='color: #155724;'>Dog</h2>
            <p>I am <strong>{prob_dog:.2f}%</strong> certain this is a dog.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
"""Oui, exactement ! La méthode requests.post() envoie une requête au serveur et attend une réponse dans le même appel. 
C’est un aller-retour complet entre ton programme et l’API.

🔁 Ce qui se passe étape par étape
- Tu envoies une requête POST :
- Avec une URL (ex. http://localhost:8000/predict)
- Et des données (ex. un fichier, un JSON, un formulaire)
- Le serveur reçoit la requête, la traite (ex. il lit le fichier, fait une prédiction, etc.)
- Le serveur renvoie une réponse :
- Souvent au format JSON
- Avec un code HTTP (200, 400, 500…)
- Ton programme reçoit cette réponse :
- Tu peux lire le contenu avec .json(), .text, .status_code, etc.
"""

"""- GET : pour lire des données
- POST : pour envoyer des données
- Les deux renvoient une réponse que tu peux lire avec .json(), .text, .status_code, etc.
import requests

params = {"nom": "Alice", "ville": "Cotonou"}
response = requests.get("https://api.exemple.com/recherche", params=params)
Elle sert à insérer des clés valeurs, q?= valeur à travers un json que l'on nomme params dans get()
""" 

# Un endpoint est une URL spécifique dans une API qui accepte des requêtes et retourne des réponses. 
# Chaque endpoint correspond à une fonctionnalité précise

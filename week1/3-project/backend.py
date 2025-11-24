from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd


# Créer l'application FastAPI
app = FastAPI()

def load():
    model_path = r"week1/3-project/model.pkl" # J'ai du changer le `\ par / pour me conformer à Render baser sous Linux §§§§
    model = joblib.load(model_path)
    return model
# Prendre l'habitude d'utiliser les row string dans mes appplication de chemin (path)
# Chargement du modèle lors de la configuration de l'application

model = load()

# __ First route__
@app.get("/")
def bonjour():
    return {"info" : "Bienvenue pour la prédiction de l'attrition des clients"}

# __ Second route__

# Définir la structure des données attendues
class CustomerData(BaseModel):
    gender: str
    SeniorCitizen: int
    Partner: str
    Dependents: str
    tenure: int
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    # ajoute toutes les autres variables nécessaires


# Définir une route pour la prédiction
@app.post("/predict") 
async def predict_churn(data: CustomerData):
    # Convertir les données en DataFrame
    df = pd.DataFrame([data.model_dump()])
     # Mêmes transformations que pendant l'entraînement !
    # -------------------------------------------
    df = df.replace({'Yes': 1, 'No': 0})
    df['gender'] = df['gender'].map({'Male': 1, 'Female': 0})

    # One-hot encoding pour les colonnes catégorielles
    df = pd.get_dummies(df,columns = ["MultipleLines", "InternetService", "OnlineSecurity"],  drop_first=True, dtype = int)

    # -------------------------------------------
    # Alignement des colonnes avec le modèle (important si ton modèle a été entraîné sur un ensemble plus large)
    # -------------------------------------------
    model_columns = model.feature_names_in_


    # feature_names_in_ est un attribut des modèles scikit-learn qui indique la liste exacte des colonnes (features) utilisées lors de l’entraînement du modèle.
    # C’est extrêmement utile — et souvent indispensable — lorsqu’on fait du déploiement, car il permet de
    # vérifier que les données envoyées au modèle au moment de la prédiction correspondent exactement aux données utilisées à l’entraînement.

    df = df.reindex(columns=model_columns, fill_value = 0)
     # La méthode reindex() de pandas sert à réarranger, ajouter ou supprimer des lignes/colonnes dans un DataFrame en fonction d’un nouvel index ou d’une nouvelle liste de colonnes.
    # fill_value = 0, c'est se paramètre  qui a planté mon fastapi

    # En clair : reindex force un DataFrame à correspondre à une liste d’index/colonnes donnée.
    # “Garde exactement ces colonnes, dans cet ordre.
    # Si une colonne manque, ajoute-la et remplis-la avec 0.
    # Si une colonne en trop existe, supprime-la.”


    """dump en programmation signifie 'sérialiser', c'est-à-dire convertir des données complexes(structur"s) en
     un format simple et transportable"""
    # Faire la prédiction
    prediction = model.predict(df)
    proba_prediction = model.predict_proba(df)

    # Retourner le résultat
    return  {"churn_prediction": int(prediction[0]), "proba_prediction" : float(proba_prediction[0][1])} # ici je n'avais mis que int(proba_prediction[0])
    # je ne peux pas transformer une liste en entier 
    # La probabilité c'est un nombre à virgule pas un int, comment je peux mettre int

#  Quand tu appuies sur le bouton, st.button() renvoie True pendant une exécution, puis repasse à False
"""- Started server process [22072] → Uvicorn a lancé un processus avec l’ID 22072.
- Waiting for application startup. → FastAPI exécute les éventuelles fonctions de démarrage (startup events).
- Application startup complete. → Ton application est maintenant opération
"""

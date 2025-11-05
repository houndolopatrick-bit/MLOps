from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd


# Créer l'application FastAPI
app = FastAPI()

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
def predict_churn(data: CustomerData):
    # Convertir les données en DataFrame
    df = pd.DataFrame([data.dict()])

    # Faire la prédiction
    prediction = model.predict(df)

    # Retourner le résultat
    return {"churn_prediction": int(prediction[0])}

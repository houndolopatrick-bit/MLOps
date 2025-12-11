from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from datetime import date,  datetime
import numpy as np
from sklearn.preprocessing import MinMaxScaler


# Créer l'application FastAPI
app = FastAPI()

def load():
    model_path = r"model.pkl" # J'ai du changer le `\ par / pour me conformer à Render baser sous Linux §§§§
    model = joblib.load(model_path)
    return model
# Prendre l'habitude d'utiliser les row string dans mes appplication de chemin (path)
# Chargement du modèle lors de la configuration de l'application

model = load()
scaler = joblib.load("scaler.pkl")

# définir la longeur de la fenêtre avec look_back
def create_sequences(data, window_size):
    X= []
    # Séquence d'entreéé X : les données de t à t + look_back - 1
    X.append(data[0: window_size, :])
    return np.array(X)
# Définissons le pas de la fenêtre : 6

window_size= 6


# __ First route__

@app.get("/")
# Pourquoi cette fonction ne s'applique pas (tout simplement parce que tu n'utilises pas cette route)
def bonjour():
    return {"info" : "Bienvenue pour la prédiction des ventes de vos magasins "}

# __ Second route__

# Définir la structure des données attendues


class Observation(BaseModel):
   date : str  # les formats comme json ne comprenne que strings, nombres, bool , liste et dico. Il ne peuvent pas gérer date, datetime
   store_nbr : int 
   family : str
   onpromotion : int
    # ajoute toutes les autres variables nécessaires

# Définir une route pour la prédiction
@app.post("/predict")   
def predict_churn(data: Observation):  # Structure de observation 

    # 1. Convertir la liste en DataFrame
    df_original = pd.DataFrame([data.model_dump()])
    N = 5

    # 1. Utiliser le même principe d'index répétitif, mais en utilisant N
    index_repete_fixe = np.repeat(df_original.index.values, 5)

    # 2. Appliquer .loc[]
    df = df_original.loc[index_repete_fixe].reset_index(drop=True)
                      
    df['date'] = pd.to_datetime(df['date'], format ="%Y-%m-%d") # sépareer par des / est différent de - au niveau de format
     # Mêmes transformations que pendant l'entraînement !
    
    df["month"] = df["date"].dt.month
    df["year"] = df["date"].dt.year
    df["day"] = df["date"].dt.day

    
    
    # Encodage du mois et des jours pour tenir compte de leur périodicité dans le modèle 
    df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
    df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
    df['day_sin'] = np.sin(2 * np.pi * df['day'] / 30)
    df['day_cos'] = np.cos(2 * np.pi * df['day'] / 30)
    # Suppression des colonnes inutiles
    df.drop(columns = ['date', 'family', 'month', 'day','store_nbr'], inplace = True) 
    # sans le inplace, je ne modifie rien


    # En clair : reindex force un DataFrame à correspondre à une liste d’index/colonnes donnée.
    # “Garde exactement ces colonnes, dans cet ordre.
    # Si une colonne manque, ajoute-la et remplis-la avec 0.
    # Si une colonne en trop existe, supprime-la.”

    df = df.reindex( columns = ['onpromotion', 'year', 'month_sin', 'month_cos', 'day_sin', 'day_cos'])
    df_np = df.to_numpy()
    """dump en programmation signifie 'sérialiser', c'est-à-dire convertir des données complexes(structur"s) en
     un format simple et transportable"""
    df2_np = create_sequences(df_np, window_size)
    np.shape(df2_np)
    # Faire la prédiction

    prediction_scaled_sales = model.predict(df2_np)

    # Revenons au vraie valeurs de notre variable scaler
    dummy_test_data = np.zeros((len(prediction_scaled_sales), 6)) # 6 pour mon nombre de features
    dummy_test_data[:, 0] = prediction_scaled_sales.flatten()
    predict_sales = scaler.inverse_transform(dummy_test_data)[:, 0]

    # Retourner le résultat
    return  {"prediction" : float(predict_sales[0])} # ici je n'avais mis que int(proba_prediction[0])
    # je ne peux pas transformer une liste en entier 
    # La probabilité c'est un nombre à virgule pas un int, comment je peux mettre int

# Le simple fait de charger un modèle me donne accès à ses caractéristiques comme n_features_in_

# 422 : le serveaur a compris la requête, mais ne peut  pas la traiter à cause de données invalides
# commande pour lancer fastapi : uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Mon erreur était tout simplement dû au fait que j'ai entraîné mon modèle avec 06 données 
# historiques(observation) et il se fait il en réclame de même pour la prédiction or je ne dispose
# que des données d'une observation
"""Dans le contexte des modèles de données que vous utilisez (probablement Pydantic, car vous mentionnez model_dump), une instance de la classe data est un objet Python concret créé à partir de la définition formelle du modèle de données (data).

🏗️ Comprendre la Relation
Pour clarifier, faisons la distinction entre la Classe et l'Instance :

1. La Classe (data) : Le Moule 🍮
La classe data (ou tout autre nom que vous lui avez donné, par exemple DataItem ou PredictionRequest) est le schéma ou le moule qui définit la structure des données.

Elle spécifie quels champs doivent exister (par exemple, sales_scaled, month_sin, year), et quel est le type de données attendu pour chaque champ (par exemple, float, int).

Exemple (Définition Pydantic) :

Python

class Data(BaseModel):
    sales_scaled: float
    year: int
    month_sin: float
2. L'Instance (data_instance) : L'Objet Rempli 🧱
L'instance est un objet réel créé à partir de cette classe, contenant des valeurs spécifiques et validées.

C'est la matérialisation du schéma.

Exemple :

Python

# L'instance de la classe Data, contenant des données réelles
data_instance = Data(sales_scaled=0.337937, year=2013, month_sin=0.5)

# Ici, 'data_instance' est l'instance de la classe 'Data'.
# C'est sur cet objet que vous appelleriez '.model_dump()'
🎯 Rôle de l'Instance dans FastAPI/Pydantic
Dans votre flux de travail de Machine Learning/API :

Lorsque FastAPI reçoit une requête JSON (les données que l'utilisateur envoie).

Il prend ce JSON, le valide contre le schéma de la Classe data.

Si la validation réussit, FastAPI crée une instance de la classe data (l'objet validé) et la passe à votre fonction d'API.

C'est cette instance qui garantit que vos données 
sont au format, au type et dans les limites attendues avant d'être traitées par votre modèle."""
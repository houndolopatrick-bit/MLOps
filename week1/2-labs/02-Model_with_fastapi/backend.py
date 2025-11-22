# ------------------------------------------------------- 
# Requirements
# ------------------------------------------------------- 
from fastapi import FastAPI, UploadFile
from tensorflow.keras.models import load_model
import numpy as np
import io
from PIL import Image
import joblib
from pydantic import BaseModel

# ------------------------------------------------------- 
# App
# ------------------------------------------------------- 
app = FastAPI()

# ------------------------------------------------------- 
# Utils
# ------------------------------------------------------- 
def preprocess(img):
    img = img.resize((150, 150))
    img = np.asarray(img)
    img = np.expand_dims(img, axis=0)
    return img

def load():
    model_path = "./notebook/best_model.keras"
    # model = joblib.load(model_path)
    model = load_model(model_path)
    return model

# ------------------------------------------------------- 
# Load the model on app setup
# ------------------------------------------------------- 
model = load()

# ------------------------------------------------------- 
# First route
# ------------------------------------------------------- 
@app.get("/")
def api_info():
    return {"info": "Welcome carapuce"}

# ------------------------------------------------------- 
# Second route
# ------------------------------------------------------- 
class Params(BaseModel):
    age: int
    weight: float
    height: float


@app.post("/predict")
async def predict(file: UploadFile):
    image_data = await file.read()
    img = Image.open(io.BytesIO(image_data))
    img_processed = preprocess(img)

    predictions = model.predict(img_processed)
    print(predictions)
    proba = float(predictions[0][0])
    return {
        "cat_proba": 1 - proba,
        "dog_proba": proba,
        "predict_class": "dog" if proba > 0.5 else "cat"
    }
<<<<<<< HEAD

# @app.post("/predict")
# async def predict(params: Params):
# #async def predict(file: UploadFile):
# #    image_data = await file.read()
#     #img = Image.open(io.BytesIO(image_data))
#     #img_processed = preprocess(img)
#     predictions = model.predict(params)
#     print(predictions)
#     proba = float(predictions[0][0])
#     return {"churn": predictions}
#     return {
#         "cat_proba": 1 - proba,
#         "dog_proba": proba,
#         "predict_class": "dog" if proba > 0.5 else "cat"
#     }
=======
"""from pydantic import BaseModel

class Params(BaseModel):
    age: int
    weight: float
    height: float
    - BaseModel : classe de base fournie par Pydantic. Elle permet de créer des modèles avec validation automatique.
- Params : nom de ta classe, ici utilisée pour regrouper des paramètres.
- age: int : champ obligatoire, doit être un entier
- weight: float : champ obligatoire, doit être un nombre décimal
- height: float : idem
Avantage de BaseModel de Pydantic
La validation automatique consiste à vérifier que les données reçues (par exemple via une requête HTTP) sont du bon type, complets, et conformes à ce que ton programme attend
La sérialisation consiste à convertir un objet Python (comme une instance de Params) en un format transportable, comme du JSON, pour l’envoyer à un client ou à une autre API.
Exemple : 
params = Params(age=30, weight=70.5, height=175)
json_data = params.json()

"""
>>>>>>> f662e81 (WIP: travail en cours)

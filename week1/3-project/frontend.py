import streamlit as st
import requests

# ------------------------------------------------------- 
# General setting
# ------------------------------------------------------- 
st.set_page_config(page_title='Churn prediction', layout='wide', page_icon ="🚀" )
st.title("Churn predictor")
st.markdown("Bienvenue à SpaceLand, où tout est possible. Il suffit d'y croire fort")
st.write("Sans plus tarder prédison l'attrition des clients. Remplissez les champs sur votre gauche et explorons les possibilités de l'acquisition de cette nouvelle compétence ")

with st.sidebar.header('Set Parameters'):
    gender = st.sidebar.radio('Quel est votre genre ?', options = ["Female", "Male"])
    Partner = st.sidebar.radio('Avez-vous un partenaire (conjoint) ?', options = ["Yes", "No"])
    OnlineSecurity= st.sidebar.radio('OnlineSecurity', options = ["Yes", "No"])
    SeniorCitizen = st.sidebar.slider('SeniorCitizen', 0, 1) # valeur minimale et après valeur maximale
    Dependents = st.sidebar.radio('Dependents', options = ["Yes", "No"])
    tenure = st.sidebar.number_input("Tenure", min_value= 0, max_value = 72, value =25)
    PhoneService = st.sidebar.radio('PhoneService', options = ["Yes", "No"])
    MultipleLines =st.sidebar.radio("MultipleLines", options = ["No", "Yes", "No phone service"] ) 
    InternetService = st.sidebar.radio("InternetService", options = ["No", "DSL", "Fiber Optic"] )
    MonthlyCharges = st.sidebar.number_input("MonthlyCharges", value = 0)

# Mes data
data = {"gender" : gender, "Partner": Partner, "OnlineSecurity" : OnlineSecurity, "SeniorCitizen": SeniorCitizen,
    "Dependents" : Dependents, "tenure" : tenure, "PhoneService" : PhoneService, "MultipleLines" : MultipleLines,
    "InternetService" : InternetService, "MonthlyCharges" : MonthlyCharges} 

# URL prediction
url = "https://mlops-3-vcca.onrender.com/predict"

# Scop des variables Dans Python classique, une variable définie après un événement n’existe pas avant.
# Dans Streamlit, les événements déclenchent une ré-exécution complète, donc toute variable définie dans
#  un bloc dépendant d’un widget n’existe qu’après le clic, même si on lit le script du haut vers le bas.

if st.button("Send"):
   reponse  = requests.post(url,json = data) 
   reponse = reponse.json()
   st.write(f"La probabilité de quitter cette entreprise est de {reponse["proba_prediction"]}./n" )


# Interception de l'erreur
try:
        response = requests.post(url, json=data)
        # Oui exactement, status_code est un attribut d’un objet Response dans les bibliothèques HTTP comme
        #  requests en Python (ou FastAPI côté serveur, mais côté client c’est un attribut de la réponse).

        if response.status_code == 200:
            st.success("Prediction reçue !") # Fonction Streamlit qui affiche un message de succès avec un encadré vert.
            # Très utile pour indiquer à l’utilisateur que l’action a été réalisée correctement.
             # le résultat de notre api est un dictionnaire qu'il est important de convertir en json
            st.write(response)
        else:
            st.error(f"Erreur API : {response.status_code}") # Fonction Streamlit qui affiche un message d’erreur avec un encadré rouge.
            # Très pratique pour alerter l’utilisateur d’un problème.
            st.write(response.json())

except Exception as e:
        st.error("Impossible de contacter l'API.")
        st.write(e)










   # !!!! J'avais mis url et req en dehors de if et cela à générer une erreur , pourquoi ?


#  Lors de la prédiction, tu dois envoyer au modèle exactement les colonnes qu’il a apprises :
# même nom

# même ordre

# mêmes colonnes one-hot

# aucune colonne manquante

# Sinon scikit-learn plante.

# ➡️ reindex sert à cela : garantir la compatibilité entre tes données et ton modèle.


# Un scaler est un outil de prétraitement en machine learning qui sert à mettre les variables numériques à la même échelle
# - En pratique, certaines variables peuvent avoir des valeurs très grandes (ex. revenu annuel en milliers) et d’autres très petites (ex. âge en dizaines).
# - Si tu utilises un modèle sensible aux différences d’échelle (comme la régression logistique, les SVM, ou les réseaux de neurones), les variables avec des grandes valeurs peuvent dominer l’apprentissage.
# - Le scaler corrige ça en transformant les données pour que toutes les variables soient comparables.
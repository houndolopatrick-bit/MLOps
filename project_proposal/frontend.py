import streamlit as st
from datetime import date, datetime
import streamlit as st
import requests  # Nécessaire pour la requête d'API
import pandas as pd
from time import sleep

# ------------------------------------------------------- 
# General setting
# ------------------------------------------------------- 
st.set_page_config(page_title="Prédiction des ventes d'une entreprise", layout='wide', page_icon ="🚀" )


# --- 1. Initialisation de la Session (Mémoire) ---
# Si 'observations' n'existe pas dans la mémoire de l'application, on le crée.

# Toute application à besoin d'un titre
st.title("Prédiction de vente ")
st.markdown("Bienvenue à vous sur  cette interface de prévision")
st.write("Sans plus tarder prédisons les ventes futures de notre entreprises." \
"Remplissez les champs sur votre gauche et explorons les possibilités de l'acquisition de cette nouvelle compétence ")

with st.sidebar:
    st.header('Sélectionner les caractéristiques de la barre de navigation')
    date = st.sidebar.date_input(label = 'Quel est la date de prévision ?', value = date.today() , min_value =date(2013,1,1), format = "YYYY/MM/DD") # Format d'affichage pour l'utilisateur
    # Les fichiers json ne connaissant pas les format de type date, je dois les convertir en string 
    date_str = datetime.strftime(date, format = "%Y-%m-%d")
    store_nbr = st.sidebar.number_input('Quelle est le numéro du magasin ', min_value = 1, max_value = 54)
    family = st.sidebar.selectbox('Types de famille de vente', options = ['AUTOMOTIVE', 'BABY CARE', 'BEAUTY', 'BEVERAGES', 'BOOKS',
       'BREAD/BAKERY', 'CELEBRATION', 'CLEANING', 'DAIRY', 'DELI', 'EGGS',
       'FROZEN FOODS', 'GROCERY I', 'GROCERY II', 'HARDWARE',
       'HOME AND KITCHEN I', 'HOME AND KITCHEN II', 'HOME APPLIANCES',
       'HOME CARE', 'LADIESWEAR', 'LAWN AND GARDEN', 'LINGERIE',
       'LIQUOR,WINE,BEER', 'MAGAZINES', 'MEATS', 'PERSONAL CARE',
       'PET SUPPLIES', 'PLAYERS AND ELECTRONICS', 'POULTRY',
       'PREPARED FOODS', 'PRODUCE', 'SCHOOL AND OFFICE SUPPLIES',
       'SEAFOOD'])
    onpromotion = st.sidebar.number_input("Promotion", min_value= 0, value =25)
#Pour mettre en place une liste déroulante (un menu de sélection) dans Streamlit, vous devez utiliser le widget st.selectbox.
# # Ce widget est idéal pour permettre à l'utilisateur de choisir une seule option parmi une liste définie.
# Mes datas


st.info("Veuillez entrer les paramètres relatifs à 06 observations puis appuyer sur le boutton **Envoyer** qui **s'affichera**")

data = {"date" : date_str , "store_nbr": store_nbr, "family": family, "onpromotion" : onpromotion} 
# Rechercher pourquoi je dois mettre entre parenthèses (), les valeurs de mes clés 

# Il y a 02 manières de définir un dataframe, une liste de dictionne, un dataframe avec une liste pour chaque clé
# Affichage du statut

# Affichage de l'observation en cours de saisie
st.subheader("Observation Actuelle (Ligne à Ajouter)")
st.dataframe(pd.DataFrame([data]))
st.success("Séquence complète. Prêt pour la prédiction !")

# --- 5. Logique du Bouton de Prédiction (Appel API) ---

    # Le bouton de prédiction n'apparaît que lorsque les 6 sont là.
    # URL prediction 
    # Usage  de la route predict
url = "https://mlops-p1fj.onrender.com/predict"


    # Interception de l'erreur
try:
    
    # Oui exactement, status_code est un attribut d’un objet Response dans les bibliothèques HTTP comme
    #  requests en Python (ou FastAPI côté serveur, mais côté client c’est un attribut de la réponse).
    
    if st.button("Envoyer"):
        # Envoie des données à mon url uvicorn de fastapi

        response  = requests.post(url, json = data) 
        if response.status_code == 200:
            st.write("Le modèle traite vos données en temps réel.")
            progress_bar = st.progress(0, text="Progression du traitement...")

            for percent_complete in range(100):
                sleep(0.05)
                progress_bar.progress(percent_complete + 1, text=f"Progression : {percent_complete + 1}%")
            st.write("Patientez un court instant....")

            reponse = response.json()
            st.success("Données bien reçue!") # Fonction Streamlit qui affiche un message de succès avec un encadré vert.
            # Très utile pour indiquer à l’utilisateur que l’action a été réalisée correctement.
            # le résultat de notre api est un dictionnaire qu'il est important de convertir en json
            st.write(f"Vos ventes seront de {reponse['prediction']: .3f} le {date_str}.")
            
        else:      
            st.error(f"Erreur API : {response.status_code}") 
            # Fonction Streamlit qui affiche un message d’erreur avec un encadré rouge.
            # Très pratique pour alerter l’utilisateur d’un problème.

except Exception as e:
        st.error("Impossible de contacter l'API.")
        st.write(e)

    # Scop des variables Dans Python classique, une variable définie après un événement n’existe pas avant.
    # Dans Streamlit, les événements déclenchent une ré-exécution complète, donc toute variable définie dans
    #  un bloc dépendant d’un widget n’existe qu’après le clic, même si on lit le script du haut vers le bas.

st.text_input('Veuillez faire part de vos critiques pour pouvoir améliorer notre algorithme de prévision')
st.text('A bientôt ')

    #Pour intégrer du Markdown (formatage de texte comme le gras, les listes ou les liens) à l'intérieur 
    # d'un message affiché avec st.info, st.success, st.warning ou st.error dans Streamlit, vous n'avez rien de spécial à faire.
    #Streamlit prend en charge le Markdown dans tous ses messages d'alerte par défaut !

    # $$\Large \text{st.rerun()}$$Cette nouvelle fonction fait exactement la même chose : elle force l'application Streamlit à redémarrer son exécution du début, ce qui est nécessaire dans ce cas précis pour mettre à jour le compteur d'observations et le tableau après un ajout.
# Pour faire un retour à indentation Shift + Tab
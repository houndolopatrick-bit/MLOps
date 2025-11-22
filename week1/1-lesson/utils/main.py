from typing import Union
from fastapi import FastAPI

""" Création de l'instance FastApi"""
app = FastAPI()
"""__Différence entre get et post
Get : Obtenir ou récupérer des données
Post : Créer ou Envoyer des données
Le / indique la racine de votre interface ou sa page d'accueil"""

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

""" 
supposons qu'un utilisateur fasse : GET http://monsite.com/menu
Fast APi fait
Reçoit la requête
Trouve la route /menu
Exécute la fonction sous le décorateur
Prend le retour de la fonction
Le transforme en JSON
Renvoie la réponse au client
___ Les crochets définissent une partie variable de l'URL
__ Le / sépare les segments de l'URL
__?param = value : Il s'agit de définit un  paramètre optionnelle dans l'URL
__ Rappelle toi que les décorateurs permettent d'appliquer une fonction à condition que quelque chose soit fait
"""
"""Structure complète d'une URL
- Structure
HTTPS/// # sécurisé
http:// # Non sécurisé
ftp // # Transfert de fichier
-Hôte (host) domaine ou Ip
monapi.com
localhost
127.0.0.1
- Chemin(Path) - Route principale
/users
/posts
/api/v1/products
- Paramètres de chemin - variables dans l'url
/users/{user_id}
posts/{post_id}
-Paramètres de requêtes (Query param-tres)
/ : sépare les segments de chemin
? : Début des query
& : Sépare les query
= : Assigne une valeur à un paramètre
__Différence  entre les paramètres de chemin et de requête__
Les paramètres de  chemin se situe dans l'URL directement 
https: //monapi.com/users/123/posts/456 : ici 123 représent le user_id et post_id = 456 sont les paramètres
Les paramètres de requête figure après le ?
Une grande différence est le fait que les paramètres de chemin sont obligatoire et ceux de requête sont optionnelles



"""
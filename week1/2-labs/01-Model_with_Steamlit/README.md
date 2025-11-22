# week1-lab1

### Create conda environment
Firstly, we will create a conda environment called *lab1_env*
```
python -m venv lab1_env
```
Secondly, we will login to the *lab1_env* environement
```
source ./lab1_env/bin/activate
```
### Install prerequisite libraries
Pip install libraries
```
pip install -r requirements.txt
```

###  Launch the app
```
python -m streamlit run app.py
```
🔹 1. Le rôle de python -m

L’option -m de Python veut dire :

« Exécute le module nommé qui se trouve dans les paquets installés, comme si c’était un script. »

Autrement dit, python -m streamlit dit à Python :

« Trouve le module streamlit installé dans l’environnement courant et exécute son code principal. »
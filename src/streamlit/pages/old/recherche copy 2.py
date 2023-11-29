import streamlit as st
import pandas as pd

df = pd.read_csv('./pages/dataset_personnes.csv')

df = df[['Statut', 'Âge', 'Enfants', 'Profession', 'Salaire Annuel (€)']]

liste_metiers = list(df['Profession'].unique())

df = pd.get_dummies(df)

X = df.drop('Salaire Annuel (€)', axis=1)
y = df['Salaire Annuel (€)']

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size = 0.70)

from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X_train, y_train)

def prediction(age, enfants, statut, profession):
  Xp = pd.DataFrame({'Âge' : [age],
                   'Enfants' : [enfants],
                   'Statut' : [statut],
                   'Profession' : [profession]})

  cols = X.columns

  Xp_dummies = pd.get_dummies(Xp)

  for c in cols:
    if c not in Xp_dummies.columns:
        Xp_dummies[c] = 0

  Xp_dummies = Xp_dummies[cols]

  import numpy as np
  Xp_dummies = Xp_dummies.astype(np.uint8)

  return model.predict(Xp_dummies)[0]


age = st.slider('Age', 0, 100, 50)
enfants = st.slider('Enfant(s)', 0, 10, 1)

options = ["Marié", "Non Marié"]

# Création du select box
statut = st.selectbox("Choisissez une valeur :", options, index=1)

#liste_metiers



#metier = st.text_input('Entrez un métier', value = 'Avocat')

recherche = st.text_input("Rechercher un métier :")\
        .lower()\
        .replace('é', 'e')

if recherche:
    metiers_trouves = [metier for metier \
                    in liste_metiers \
                    if recherche \
                    in metier\
                        .lower()\
                        .replace('é', 'e')]
    #st.write(films_trouves)

    metier = st.selectbox("Choisissez une valeur :", metiers_trouves)







try :
    predi = prediction(age, enfants, statut, metier)
    predi
except : 
   'en attente'


















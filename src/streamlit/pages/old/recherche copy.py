import streamlit as st

liste_films = ["Fight Club",
               "Inception",
               "The Matrix",
               "Interstellar",
               "Intermédiaire",
               "Intermediaire sans accent",
               "Street Fighter"]


recherche = st.text_input("Rechercher un film :")\
        .lower()\
        .replace('é', 'e')

if recherche:
    films_trouves = [film for film \
                    in liste_films \
                    if recherche \
                    in film\
                        .lower()\
                        .replace('é', 'e')]
    #st.write(films_trouves)

    statut = st.selectbox("Choisissez une valeur :", films_trouves)


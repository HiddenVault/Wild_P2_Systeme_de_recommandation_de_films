import streamlit as st

liste_films = ["Fight Club",
               "Inception",
               "The Matrix",
               "Interstellar",
               "Intermédiaire",
               "Street Fighter"]


recherche = st.text_input("Rechercher un film :").lower()

if recherche:
    films_trouves = [film for film in liste_films \
                    if recherche in film.lower()]
    
    st.write(films_trouves)


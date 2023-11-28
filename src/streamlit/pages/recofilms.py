import streamlit as st

def lire_css(fichier):
    with open(fichier, 'r', encoding='utf-8') as f:
        return f.read()

# Lire le fichier HTML
contenu_html = lire_css('./pages/st.css')

# Afficher le contenu HTML dans Streamlit
st.markdown(contenu_html, unsafe_allow_html=True)

st.title('Hello Wilders, welcome to my application!')

data = ''
url = 'http://www.google.fr'

st.button("Click me")
st.checkbox("I agree")
st.toggle("Enable")
st.radio("Pick one", ["cats", "dogs"])
st.selectbox("Pick one", ["cats", "dogs"])
st.multiselect("Buy", ["milk", "apples", "potatoes"])
st.slider("Pick a number", 0, 100)
st.select_slider("Pick a size", ["S", "M", "L"])
st.text_input("First name")
st.number_input("Pick a number", 0, 10)
st.text_area("Text to translate")
st.date_input("Your birthday")
st.time_input("Meeting time")

tab1, tab2 = st.tabs(["Tab 1", "Tab2"])
tab1.write("this is tab 1")
tab2.write("this is tab 2")

import streamlit as st

st.markdown('<h1 style="color:red;">Voilà mon titre</h1><h2 style="color:green;">Mon H2</h2><br><br><p>mon paragraphe</p>', unsafe_allow_html=True)


st.markdown("""
    <h1 style="color:red;">Voilà mon titre</h1>
<h2 style="color:red;">Mon H2</h1>
<br><br>
<p>mon paragraphe</p>
    """, unsafe_allow_html=True)

# HTML avec la classe CSS appliquée
st.markdown('<div class="custom-css">Texte avec CSS personnalisé</div>', unsafe_allow_html=True)
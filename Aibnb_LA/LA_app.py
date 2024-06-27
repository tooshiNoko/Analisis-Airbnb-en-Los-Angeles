import altair as alt
import pandas as pd
import streamlit as st

# Show the page title and description.
st.title("🏠 Los Angeles - Airbnb dataset")
st.write(
    """
  Esta aplicación permite explorar los datos de los alojamientos de Airbnb en Los Angeles.
  Utilizamos el conjunto de datos de [Inside Airbnb](http://insideairbnb.com/get-the-data.html).
    """
)

import streamlit as st

st.set_page_config(page_title="Airbnb Los Angeles", page_icon="🏠", layout="wide")

# Crear una barra lateral para la navegación
st.sidebar.title("Navegación")
page = st.sidebar.radio("Ir a", ["Inicio", "Análisis de Datos"])

# Navegar a la página seleccionada
if page == "Inicio":
    from pages import home
    home.show()
elif page == "Análisis de Datos":
    from pages import analysis
    analysis.show()
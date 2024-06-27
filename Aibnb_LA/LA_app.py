import streamlit as st
import pandas as pd
import folium
import geopandas as gpd
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium


# Configuración de la página
st.set_page_config(page_title="LA Airbnb Analysis", layout="wide")

# Show the page title and description.
st.title("🏠 Los Angeles - Airbnb dataset")
st.write(
    """
  Esta aplicación permite explorar los datos de los alojamientos de Airbnb en Los Angeles.
  Utilizamos el conjunto de datos de [Inside Airbnb](http://insideairbnb.com/get-the-data.html).
    """
)

# Función para cargar los datos desde una URL comprimida
@st.cache
def load_data_from_url():
    # URL del archivo comprimido CSV
    URL = r"https://data.insideairbnb.com/united-states/ca/los-angeles/2024-03-11/data/listings.csv.gz"
    # Leer el archivo CSV comprimido
    LAgz = pd.read_csv(URL, compression='gzip')
    # Seleccionar solo las columnas necesarias de LAgz
    LAgz_selected = LAgz[['id', 'bathrooms', 'amenities', 'bedrooms', 'beds', "accommodates", "first_review", "review_scores_rating"]]
    return LAgz_selected

# Función para cargar el archivo listings.csv localmente
@st.cache
def load_data_local():
    # Cargar el archivo listings.csv desde la carpeta 'data'
    LA = pd.read_csv('data/listings.csv')
    # Reemplazar cambios de línea por espacios en columnas de tipo objeto
    for col in LA.select_dtypes(include=['object']).columns:
        LA[col] = LA[col].str.replace("\n", " ", regex=False)
    return LA

# Cargar los datos una vez al inicio de la aplicación
LA = load_data_local()
LAgz_selected = load_data_from_url()

# Realizar el merge basado en la columna 'id'
LA_merged = pd.merge(LA, LAgz_selected, on='id', how='left')


# Configuración de la página de Streamlit
st.set_page_config(
    page_title="LA Airbnb Data Analysis",
    layout="wide"
)

# Definir las funciones para cada página
def show_home():
    st.title("Home")
    st.header("Bienvenido al Análisis de Airbnb en Los Ángeles")
    st.write("Utilice el menú lateral para navegar a través de diferentes secciones y obtener información específica.")
    #st.image('data/los_angeles.jpg', caption='Los Ángeles')

    with st.expander('Origen de los Datos'):
        st.markdown("""
                    Los datos utilizados en este proyecto han sido proporcionados por InsideAirbnb. Este dataset tiene múltiples columnas que detallan las propiedades de Airbnb en Los Ángeles.
                    """)
    
    with st.expander("Historia de Los Ángeles"):
        st.write("Los Ángeles es una ciudad conocida por su clima soleado, sus playas y su industria del entretenimiento, especialmente el cine y la televisión.")

    with st.expander("Ruta de los Vecindarios"):
        st.write("Los vecindarios en Los Ángeles ofrecen una diversidad única, desde áreas urbanas hasta zonas más residenciales.")
        #st.image('data/la_neighborhoods.jpg', caption='Barrios de Los Ángeles')

def show_analysis():
    st.title("Analysis")
    st.header("Choose an analysis to view:")

    analysis_option = st.selectbox(
        "Select an analysis:",
        ["Distribution by neighborhood", "Room type distribution", "Price distribution", "Interactive Map"]
    )

    if analysis_option == "Distribution by neighborhood":
        show_neighborhood_distribution()
    elif analysis_option == "Room type distribution":
        show_room_type_distribution()
    elif analysis_option == "Price distribution":
        show_price_distribution()

def show_interactive_map():
    st.title("Interactive Map")
    show_interactive_map()

# Función para mostrar la distribución por barrio
def show_neighborhood_distribution():
    st.header("Distribution by neighborhood")
    # Aquí irá el código para graficar la distribución por barrio con filtros

# Función para mostrar la distribución por tipo de habitación
def show_room_type_distribution():
    st.header("Room type distribution")
    # Aquí irá el código para graficar la distribución por tipo de habitación con filtros

# Función para mostrar la distribución de precios
def show_price_distribution():
    st.header("Price distribution")
    # Aquí irá el código para graficar la distribución de precios con filtros

# Función para mostrar el mapa interactivo
def show_interactive_map():
    
    st.header("Análisis de Datos de Airbnb en Los Ángeles")
    st.write('Aquí ponemos los graficos con los mapas')
    
    # Ejemplo de integración de un mapa usando Folium y Streamlit-Folium
    
    '''
    m = folium.Map(location=[34.0522, -118.2437], zoom_start=11)

    marker_cluster = MarkerCluster().add_to(m)
    for idx, row in listings.iterrows():
        folium.Marker(location=[row['latitude'], row['longitude']], popup=row['name']).add_to(marker_cluster)

    folium.LayerControl().add_to(m)

    st_folium(m, width=700, height=500)

  '''
# Definir el contenido de la barra lateral (sidebar)
st.sidebar.title("Navigation")
page_options = ["Home", "Analysis", "Interactive Map"]
page_selection = st.sidebar.radio("Go to", page_options)

# Mostrar la página seleccionada
if page_selection == "Home":
    show_home()
elif page_selection == "Analysis":
    show_analysis()
else:
    show_interactive_map()
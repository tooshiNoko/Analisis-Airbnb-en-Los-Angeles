import streamlit as st
import pandas as pd
import folium
from folium.plugins import FastMarkerCluster
import geopandas as gpd
from branca.colormap import LinearColormap
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
# Función para cargar el archivo listings.csv localmente
@st.cache_data
def load_data():
    return pd.read_csv('LA-Airbnb\data\LA_clean.csv')

# Cargar los datos
LA = load_data()



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
    
    with st.expander("Dasbhoard Los Angeles"):
        show_dashboard()

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

def show_dashboard():
    st.title("Dashboard Los Angeles Airbnb Data Analysis")
    st.write("A continuación se muestra el dashboard de Power BI:")
    
    # URL del dashboard de Power BI
    power_bi_url = "https://app.powerbi.com/view?r=eyJrIjoiNWQ2ZDBiNmYtMmY1NC00YTkyLWE3MTQtYmIwMmY3YzZjYWE2IiwidCI6IjhhZWJkZGI2LTM0MTgtNDNhMS1hMjU1LWI5NjQxODZlY2M2NCIsImMiOjl9"
    
    # Mostrar el iframe del dashboard de Power BI
    st.components.v1.iframe(power_bi_url, height=600)


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
    columns_to_load = ['latitude', 'longitude', 'name', 'host_name', 'price', 'bedrooms','neighbourhood_group', 'neighbourhood','price_level','antiguedad_ex','accommodates','has_pet', 'review_scores_rating','room_type']
    listings = pd.read_csv('LA-Airbnb\data\LA_clean.csv', usecols=columns_to_load)
    # Dividir la pantalla en dos columnas
    map_column, filter_column = st.columns([3, 1])
    
    with filter_column:
            st.write("Filtrar por:")
            # Ejemplo de inicialización de filtros para incluir todas las opciones por defecto
            selected_price = st.slider('Selecciona un precio', min_value=int(listings['price'].min()), max_value=int(listings['price'].max()), value=[int(listings['price'].min()), int(listings['price'].max())])
            selected_bedrooms = st.slider('Seleccion Nº de habitaciones', min_value=0, max_value=int(listings['bedrooms'].max())+1, value=[0, int(listings['bedrooms'].max())+1])
            neighbourhood_group = st.multiselect('Zonas', listings['neighbourhood_group'].unique(), default=listings['neighbourhood_group'].unique())
            neighbourhood_options = ['Todos'] + sorted(listings['neighbourhood'].unique())
            neighbourhood = st.multiselect('Barrios', options=neighbourhood_options, default=['Todos'])
            price_level = st.selectbox('Nivel de precios', ['Todos'] + list(listings['price_level'].unique()))
            antiguedad_ex = st.slider('Antigüedad', 0, int(listings['antiguedad_ex'].max())+1, value=[0, int(listings['antiguedad_ex'].max())+1])
            accommodates = st.slider('Nº de Huéspedes', 1, listings['accommodates'].max()+1, value=[1, listings['accommodates'].max()+1])
            has_pet = st.radio('Admite mascota', ['Todos', 'Sí', 'No'])
            review_scores_rating = st.slider('Puntuación', 0, 100, value=[0, 100])
            room_type = st.selectbox('Tipo de alojamiento', ['Todos'] + list(listings['room_type'].unique()))

    # Filtrar datos con condiciones para cada filtro
    filtered_listings = listings[
        (listings['price'].between(selected_price[0], selected_price[1])) &
        (listings['bedrooms'].between(selected_bedrooms[0], selected_bedrooms[1]-1)) &
        (listings['neighbourhood_group'].isin(neighbourhood_group) if neighbourhood_group else True) &
        (listings['neighbourhood'].isin(neighbourhood) if 'Todos' not in neighbourhood else True) &
        (listings['price_level'] == price_level if price_level != 'Todos' else True) &
        (listings['antiguedad_ex'].between(antiguedad_ex[0], antiguedad_ex[1]-1)) &
        (listings['accommodates'].between(accommodates[0], accommodates[1]-1)) &
        (listings['has_pet'] == (has_pet == 'Sí') if has_pet != 'Todos' else True) &
        (listings['review_scores_rating'].between(review_scores_rating[0], review_scores_rating[1])) &
        (listings['room_type'] == room_type if room_type != 'Todos' else True)
    ]

    with map_column:
        m = folium.Map(location=[34.0522, -118.2437], zoom_start=11)
        locations = filtered_listings[['latitude', 'longitude']].values.tolist()
        popup_texts = [f"Name: {row['name']}<br>Host: {row['host_name']}<br>Price: {row['price']}<br>Bedrooms: {row['bedrooms']}" for _, row in filtered_listings.iterrows()]
        marker_cluster = FastMarkerCluster(data=locations, popups=popup_texts, name='Airbnb Listings')
        marker_cluster.add_to(m)
        folium.LayerControl().add_to(m)
        st_folium(m, width=700, height=500)

    
# Definir el contenido de la barra lateral (sidebar)
st.sidebar.title("Navigation")
page_options = ["Home", "Analysis", "Interactive Map"]
page_selection = st.sidebar.radio("Go to", page_options)

# Mostrar la página seleccionada
if page_selection == "Home":
    show_home()
elif page_selection == "Analysis":
    show_analysis()
elif page_selection == "Interactive Map":
    show_interactive_map()
elif page_selection == "Dashboard":
    show_dashboard()    
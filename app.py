import streamlit as st
from streamlit_option_menu import option_menu
from utils.config_state import init_config_state
import utils.config_state 
import json
import os

# Configuración inicial
st.set_page_config(page_title="LuxBeauty Lab", layout="wide")

def cargar_configuracion_visual():
    CONFIG_VISUAL_FILE = "config_visual.json"
    if os.path.exists(CONFIG_VISUAL_FILE):
        with open(CONFIG_VISUAL_FILE, "r") as f:
            return json.load(f)
    else:
        return {
            "color_primario": "#4CAF50",
        }

if "config_visual" not in st.session_state:
    st.session_state["config_visual"] = cargar_configuracion_visual()

init_config_state()

nombre_tienda = st.session_state["config_general"]["nombre"]
color_principal = st.session_state["config_visual"]["color_primario"]
formato_fecha = st.session_state["config_sistema"]["formato_fecha"]
telefono_tienda = st.session_state["config_general"]["telefono"]
direccion = st.session_state["config_general"]["direccion"]


# Estilos CSS
st.markdown("""
    <style>
        /* Fondo azul sidebar */
        section[data-testid="stSidebar"] {
            background-color: %s;
        }}; 
            padding-top: 0;
            padding-bottom: 0;
        }

        /* Quitar padding general que pone Streamlit */
        div[data-testid="stSidebar"] > div:first-child {
            padding-top: 0 !important;
            padding-bottom: 0 !important;
        }

        /* Estilo para el título en sidebar */
        .sidebar-title {
    color: white;
    font-size: 28px;         /* Un poco más grande */
    font-weight: 900;        /* Más grueso */
    margin-top: 8px;
    margin-bottom: 6px;
    letter-spacing: 1px;     /* Espaciado entre letras */
    text-transform: uppercase; /* Mayúsculas para dar fuerza */
}
        /* Estilo para el contacto */
        .sidebar-contact {
            color: white;
            font-size: 14px;
            font-weight: 400;
            opacity: 0.8;
            margin-bottom: 10px;
        }
    </style>
"""  % color_principal, unsafe_allow_html=True)

# Contenido HTML aplicado con estilo
st.sidebar.markdown(
    f"""
    <div class="sidebar-title">{nombre_tienda}</div>
    <div class="sidebar-contact">📞 {telefono_tienda}</div>
    <div class="sidebar-contact">📍 {direccion}</div>
    """,
    unsafe_allow_html=True
)

# Menú lateral
#st.sidebar.markdown("LUXBEAUTY LAB")
st.sidebar.markdown("---")

# Agregar al menú
with st.sidebar:
    menu = option_menu(
        None,
        [
            "Gestión de clientes",
            "Gestión de servicios",
            "Gestión de inventarios",
            "Reportes",
            "Facturación",
            "Cuadre de caja",
            "Configuración"
        ],
        icons=["people", "scissors", "box", "bar-chart", "receipt", "cash-coin", "question-circle", "shield-lock", "gear"],
        default_index=0,
        menu_icon="cast",
        styles={
            "container": {"padding": "0!important", "background-color": color_principal},
            "icon": {"color": "white", "font-size": "18px"},
            "nav-link": {"font-size": "16px", "color": "white", "text-align": "left", "margin": "0px"},
            "nav-link-selected": {"background-color": "rgba(255, 255, 255, 0.1)"},
        }
    )

    # Menú lateral
    #st.sidebar.markdown("LUXBEAUTY LAB")
    st.sidebar.markdown("---")


#Importación dinámica según selección
if menu == "Gestión de clientes":
    import secciones.clientes as clientes
    clientes.pantalla_clientes()

elif menu == "Gestión de servicios":
    import secciones.gestion_servicios as servicios
    servicios.pantalla_servicios()

elif menu == "Gestión de inventarios":
    import secciones.gestion_inventario as inventario
    inventario.pantalla_inventario()

elif menu == "Reportes":
    import secciones.reportes as reportes
    reportes.pantalla_reportes()

#elif menu == "Facturación":
#    import secciones.facturacion as facturacion
#    facturacion.pantalla_facturacion()

elif menu == "Cuadre de caja":
   import secciones.cuadre_caja as caja
   caja.pantalla_cuadre_caja()

#elif menu == "Solicitar Soporte":
#    import secciones.soporte as soporte
#    soporte.pantalla_soporte()

#elif menu == "Seguridad y Accesos":
 #   import secciones.seguridad as seguridad
#    seguridad.pantalla_seguridad()

elif menu == "Configuración":
    import secciones.configuracion as configuracion
    configuracion.pantalla_configuracion()

import streamlit as st
from streamlit_option_menu import option_menu


# Configuración inicial
st.set_page_config(page_title="LuxBeauty Lab", layout="wide")

st.markdown("""
    <style>
        /* Fondo azul sidebar */
        section[data-testid="stSidebar"] {
            background-color: #1f77b4;
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
            font-size: 25px;
            font-weight: bold;
            margin-top: 8px;
            margin-bottom: 8px;
        }
    </style>
""", unsafe_allow_html=True)

# Mostrar título con clase CSS en sidebar
st.sidebar.markdown('<div class="sidebar-title">LUXBEAUTY LAB</div>', unsafe_allow_html=True)

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
            "Solicitar Soporte",
            "Seguridad y Accesos",
            "Configuración"
        ],
        icons=["people", "scissors", "box", "bar-chart", "receipt", "cash-coin", "question-circle", "shield-lock", "gear"],
        default_index=0,
        menu_icon="cast",
        styles={
            "container": {"padding": "0!important", "background-color": "#1f77b4"},
            "icon": {"color": "white", "font-size": "18px"},
            "nav-link": {"font-size": "16px", "color": "white", "text-align": "left", "margin": "0px"},
            "nav-link-selected": {"background-color": "#145A8A"},
        }
    )

#Importación dinámica según selección
if menu == "Gestión de clientes":
    import secciones.clientes as clientes
    clientes.pantalla_clientes()

#elif menu == "Gestión de servicios":
#    import secciones.servicios as servicios
#    servicios.pantalla_servicios()
#
#elif menu == "Gestión de inventarios":
#    import secciones.inventario as inventario
#    inventario.pantalla_inventario()
#
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

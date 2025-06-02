import streamlit as st
import json
import os

CONFIG_VISUAL_FILE = "config_visual.json"

def guardar_configuracion_visual(color_primario, color_secundario, color_fondo):
    config = {
        "color_primario": color_primario,
    }
    with open(CONFIG_VISUAL_FILE, "w") as f:
        json.dump(config, f, indent=4)


def init_config_state():
    if "config_general" not in st.session_state:
        st.session_state["config_general"] = {
            "nombre": "LuxBeauty Lab",
            "telefono": "3173603298",
            "direccion": "Calle Belleza 101",
            "leyenda": "Gracias por tu compra. ¡Vuelve pronto!"
        }

    if "config_visual" not in st.session_state:
        st.session_state["config_visual"] = {
            "color_primario": "#C71585",
        }

    if "config_sistema" not in st.session_state:
        st.session_state["config_sistema"] = {
            "formato_fecha": "%d/%m/%Y",
            "prefijo_factura": "LUX-",
            "consecutivo_inicial": 1001
        }

def update_config_general(nombre, telefono, direccion, leyenda):
    st.session_state["config_general"] = {
        "nombre": nombre,
        "telefono": telefono,
        "direccion": direccion,
        "leyenda": leyenda
    }

def update_config_visual(color_primario, color_secundario, color_fondo):
    st.session_state["config_visual"] = {
        "color_primario": color_primario,
    }

def update_config_sistema(formato_fecha, prefijo, consecutivo):
    st.session_state["config_sistema"] = {
        "formato_fecha": formato_fecha,
        "prefijo_factura": prefijo,
        "consecutivo_inicial": consecutivo
    }

# 👇 Llama a la inicialización antes de acceder a session_state
init_config_state()
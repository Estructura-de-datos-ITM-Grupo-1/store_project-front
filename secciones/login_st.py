import streamlit as st

# -----Diccionario simulado de usuarios: {usuario: contraseña}-----
USUARIOS = {
    "admin": "admin123",
    "usuario1": "clave123",
}

def mostrar_login():
    st.title("Iniciar sesión")

    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    login_button = st.button("Ingresar")

    if login_button:
        if username in USUARIOS and USUARIOS[username] == password:
            st.session_state["logeado"] = True
            st.session_state["usuario"] = username
            st.success(f"Bienvenido, {username} 🎉")
        else:
            st.error("Usuario o contraseña incorrectos")

def mostrar_app_principal():
    st.title("Bienvenido a la aplicación")
    st.write(f"Has iniciado sesión como: **{st.session_state['usuario']}**")

    if st.button("Cerrar sesión"):
        st.session_state["logeado"] = False
        st.session_state["usuario"] = ""

# -----Inicializa los valores si no existen-----
if "logeado" not in st.session_state:
    st.session_state["logeado"] = False
if "usuario" not in st.session_state:
    st.session_state["usuario"] = ""

# -----Muestra contenido según el estado de sesión-----
if st.session_state["logeado"]:
    mostrar_app_principal()
else:
    mostrar_login()

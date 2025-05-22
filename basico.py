import streamlit as st

def main():
    st.set_page_config(page_title="LuxBeauty Login", layout="wide")

    col1, col2 = st.columns(2)  # Split the page into two columns

    with col1:
        st.markdown(
            """
            <style>
            .left-panel {
                background-color: #1570EF;
                color: white;
                padding: 80px;
                text-align: center; /* Center text */
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('<div class="left-panel"><h1>LUXBEAUTY<br>LAB</h1><p>Bienvenido al sitio web donde se gestionan y optimizan procesos laborales.</p></div>', unsafe_allow_html=True)

    with col2:
        st.title("Inicio de sesión")
        email = st.text_input("Correo Electrónico", "alvaro-prueba@store-lux.com")
        password = st.text_input("Contraseña", type="password")
        st.button("Ingresar")
        st.button("Solicitar Soporte")

if __name__ == "__main__":
    main()
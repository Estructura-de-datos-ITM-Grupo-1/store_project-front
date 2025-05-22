import streamlit as st
st.set_page_config(page_title="LuxBeauty Login", layout="wide")

st.markdown("""
    <style>
    .main {
        background-color: white;
    }
    .login-container {
        display: flex;
        height: 100vh;
    }
    .left-panel {
        background-color: #1570EF;
        color: white;
        width: 50%;
        padding: 80px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        font-family: 'Segoe UI', sans-serif;
    }
    .left-panel h1 {
        font-size: 32px;
        font-weight: bold;
        text-transform: uppercase;
    }
    .left-panel p {
        font-size: 22px;
        font-weight: 400;
        margin-top: 30px;
    }
    .right-panel {
        width: 50%;
        padding: 80px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        font-family: 'Segoe UI', sans-serif;
    }
    .input {
        margin-bottom: 20px;
    }
    .login-button, .support-button {
        width: 100%;
        padding: 10px;
        background-color: #1570EF;
        color: white;
        border: none;
        border-radius: 5px;
        font-size: 16px;
    }
    .support-button {
        background-color: white;
        color: #1570EF;
        border: 2px solid #1570EF;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)


st.markdown("""
<div class="login-container">
    <div class="left-panel">
        <h1>LUXBEAUTY LAB</h1>
        <p>Bienvenido al sitio web<br> donde se gestionan y<br> optimizan procesos laborales.</p>
    </div>
    <div class="right-panel">
        <h2>Inicio de sesión</h2>
        <div class="input">
            <label>Correo Electrónico</label><br>
            <input type="email" placeholder="balamia@gmail.com" style="width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 5px;">
        </div>
        <div class="input">
            <label>Contraseña</label><br>
            <input type="password" placeholder="Enter your password" style="width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 5px;">
        </div>
        <button class="login-button">Ingresar</button>
        <button class="support-button">Solicitar Soporte</button>
    </div>
</div>
""", unsafe_allow_html=True)

#def main():
#    st.title("Hola, Señor Álvaro 👋")
#    st.write("¡Bienvenido a tu primera app con Streamlit!")

#if __name__ == "__main__":
#    main()

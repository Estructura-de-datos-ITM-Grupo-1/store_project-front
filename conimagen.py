import streamlit as st
import base64

def get_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def main():
    st.set_page_config(page_title="LuxBeauty Login", layout="wide")

    img_base64 = get_base64("fondo.jpg")

    
    st.markdown(f"""
        <style>
        .main {{
            background-color: white;
        }}
        .login-container {{
            display: flex;
            height: 100vh;
        }}
        .left-panel {{
            background-color: #1570EF;
            color: white;
            width: 50%;
            padding: 80px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            font-family: 'Segoe UI', sans-serif;
        }}
        .left-panel h1 {{
            font-size: 50px;
            font-weight: bold;
            text-transform: uppercase;
            margin-bottom: 40px;
           
        }}
        .left-panel p {{
            font-size: 22px;
            font-weight: 400;
            margin-top: 30px;
            line-height: 1.5;
        }}
        .right-panel {{
            width: 50%;
            padding: 80px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            font-family: 'Segoe UI', sans-serif;
            position: relative;
            background-image: url("data:image/jpeg;base64,{img_base64}");
            background-repeat: no-repeat;
            background-size: 60%;
            background-position: 120% center;
            background-blend-mode: lighten;
            background-color: rgba(255, 255, 255, 0.5);
        }}
        .right-panel h2 {{
            font-size: 24px;
            margin-bottom: 30px;
            position: relative;
            z-index: 2;
        }}
        .input {{
            margin-bottom: 20px;
            position: relative;
            z-index: 2;
        }}
        .input label {{
            font-size: 16px;
            margin-bottom: 8px;
            display: block;
        }}
        .login-button {{
            width: 100%;
            padding: 12px;
            background-color: #1570EF;
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            transition: all 0.3s;
            margin-bottom: 15px;
            position: relative;
            z-index: 2;
        }}
        .login-button:hover {{
            background-color: #0e5bc4;
        }}
        .support-container {{
            display: flex;
            justify-content: flex-end;
            position: relative;
            z-index: 2;
        }}
        .support-button {{
            padding: 8px 20px;
            background-color: white;
            color: #1570EF;
            border: 2px solid #1570EF;
            border-radius: 5px;
            font-size: 14px;
            cursor: pointer;
            transition: all 0.3s;
        }}
        .support-button:hover {{
            background-color: #f0f7ff;
        }}
        input[type="email"], input[type="password"] {{
            width: 100%;
            padding: 12px;
            border: 1px solid #ccc;
            border-radius: 5px;
            font-size: 16px;
            box-sizing: border-box;
        }}
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="login-container">
        <div class="left-panel">
            <h1>LUXBEAUTY<br>LAB</h1>
            <p>Bienvenido al sitio web donde se gestionan y optimizan procesos laborales.</p>
        </div>
        <div class="right-panel">
            <h2>Inicio de sesión</h2>
            <div class="input">
                <label>Correo Electrónico</label>
                <input type="email" placeholder="alvaro-prueba@store-lux.com">
            </div>
            <div class="input">
                <label>Contraseña</label>
                <input type="password" placeholder="Enter your password">
            </div>
            <button class="login-button">Ingresar</button>
            <div class="support-container">
                <button class="support-button">Solicitar Soporte</button>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

import streamlit as st
import pandas as pd
import jwt
import time

def pantalla_servicios():
    # --- Simulación de autenticación JWT ---
    def generar_token_prueba(rol="admin"):
        payload = {
            "user_id": 1,
            "role": rol,
            "exp": time.time() + 3600
        }
        clave_secreta = "clave-secreta-del-backend"
        return jwt.encode(payload, clave_secreta, algorithm="HS256")

    if "token" not in st.session_state:
        st.session_state.token = generar_token_prueba("admin")  # o "user"

    CLAVE_SECRETA = "clave-secreta-del-backend"

    def obtener_rol_desde_token(token):
        try:
            decoded = jwt.decode(token, CLAVE_SECRETA, algorithms=["HS256"])
            return decoded.get("role", "user")
        except jwt.ExpiredSignatureError:
            st.error("Sesión expirada. Vuelve a iniciar sesión.")
        except jwt.InvalidTokenError:
            st.error("Token inválido.")
        return None

    rol_usuario = obtener_rol_desde_token(st.session_state.token)

    # --- Configuración de la app ---
    
    if st.sidebar.button("🔒 Cerrar sesión"):
        st.session_state.clear()

    # --- Título principal ---
    st.title("Gestion de Servicios")

    # --- Inicialización de datos ---
    if "servicios" not in st.session_state:
        st.session_state.servicios = []

    if "historial" not in st.session_state:
        st.session_state.historial = []

    if "servicios_temporales" not in st.session_state:
        st.session_state.servicios_temporales = []

    # --- Tabs principales ---
    tab1, tab2, tab3 = st.tabs([
        "⚙️Panel de gestión principal",
        "📋Servicios registrados",
        "🗂️Historial de modificaciones"
    ])

    # === TAB 1 ===
    with tab1:
        st.subheader("🔍 Buscar servicios por código o descripción")

        termino_busqueda = st.text_input("Escribe parte del código o descripción del servicio")

        if termino_busqueda:
            termino = termino_busqueda.lower()

            resultados = [
                s for s in st.session_state.servicios
                if termino in s["Código"].lower() or termino in s["Descripción"].lower()
            ]

            if resultados:
                st.success(f"Se encontraron {len(resultados)} servicio(s):")
                for serv in resultados:
                    st.markdown(f"**Código:** {serv['Código']}")
                    st.markdown(f"**Descripción:** {serv['Descripción']}")
                    st.markdown(f"**Precio:** ${serv['Precio']:.2f}")
                    st.markdown("---")
            else:
                st.warning("No se encontraron coincidencias.")

        st.divider()

        st.subheader("🆕 Agregar servicio")

        if rol_usuario == "admin":
            with st.expander("➕ Agregar nuevo servicio"):
                with st.form("form_servicio"):
                    codigo = st.text_input("Código del servicio (único)", key="codigo")
                    descripcion = st.text_area("Descripción del servicio", key="descripcion")
                    precio = st.number_input("Precio ($)", min_value=0.0, step=0.1, key="precio")
                    submit = st.form_submit_button("Registrar")

                if submit:
                    if not codigo or not descripcion:
                        st.warning("Por favor, completa todos los campos.")
                    elif any(serv["Código"] == codigo for serv in st.session_state.servicios):
                        st.error("El código ingresado ya existe. Usa uno único.")
                    else:
                        nuevo_servicio = {
                            "Código": codigo,
                            "Descripción": descripcion,
                            "Precio": precio
                        }
                        st.session_state.servicios.append(nuevo_servicio)
                        st.success("Servicio registrado exitosamente.")
        else:
            st.info("No tienes permisos para agregar servicios.")

        if rol_usuario == "cajero" or "admin":
            with st.expander("➕ Facturar servicio temporal (uso imprevisto)"):
                with st.form("form_temporal"):
                    desc_temp = st.text_area("Descripción", key="descripcion_temp")
                    precio_temp = st.number_input("Precio ($)", min_value=0.0, step=0.1, key="precio_temp")

                    submit_temp = st.form_submit_button("Facturar temporal")

                if submit_temp:
                    if not desc_temp:
                        st.warning("Por favor, completa todos los campos del servicio temporal.")
                    else:
                        nuevo_temp = {
                            "Descripción": desc_temp,
                            "Precio": precio_temp
                        }
                        st.session_state.servicios_temporales.append(nuevo_temp)
                        st.success("Servicio temporal facturado.")

        st.divider()

        st.subheader("📝 Modificar un servicio")

        if rol_usuario == "admin":
            if st.session_state.servicios:
                cod_editar = st.text_input("Ingresa el código del servicio a editar")

                servicio = next((s for s in st.session_state.servicios if s["Código"] == cod_editar), None)

                if servicio:
                    nueva_desc = st.text_area("Nueva descripción", value=servicio["Descripción"])
                    nuevo_precio = st.number_input("Nuevo precio", value=servicio["Precio"], step=0.1)

                    if st.button("Actualizar servicio"):
                        descripcion_anterior = servicio["Descripción"]
                        precio_anterior = servicio["Precio"]

                        servicio["Descripción"] = nueva_desc
                        servicio["Precio"] = nuevo_precio

                        st.session_state.historial.append({
                            "Código": cod_editar,
                            "Descripción anterior": descripcion_anterior,
                            "Descripción nueva": nueva_desc,
                            "Precio anterior": precio_anterior,
                            "Precio nuevo": nuevo_precio,
                            "Fecha y hora": time.strftime("%Y-%m-%d %H:%M:%S")
                        })

                        st.success("Servicio actualizado.")
                elif cod_editar:
                    st.error("Código no encontrado.")
            else:
                st.info("Aún no hay servicios.")
        else:
            st.info("No tienes permisos para modificar servicios.")

    # === TAB 2 ===
    with tab2:
        st.subheader("📋 Servicios registrados")

        if st.session_state.servicios:
            df_servicios = pd.DataFrame(st.session_state.servicios)
            st.dataframe(df_servicios)
        else:
            st.info("Aún no hay servicios registrados.")

    # === TAB 3 ===
    with tab3:
        st.subheader("🕒 Historial de modificaciones")

        if st.session_state.historial:
            df_historial = pd.DataFrame(st.session_state.historial)
            st.dataframe(df_historial)
        else:
            st.info("Aún no hay modificaciones registradas.")

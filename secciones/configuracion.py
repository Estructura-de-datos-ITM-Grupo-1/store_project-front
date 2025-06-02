import streamlit as st
from backend_logic import configuracion as cb
from backend_logic import usuarios as backend
from utils.config_state import init_config_state
from utils.config_state import update_config_general, update_config_visual, update_config_sistema


# Inicializa session_state si no existe
init_config_state()

# Aplica el color de fondo directamente aquí
st.markdown(
    f"""
    <style>
        .main {{
            background-color: {st.session_state["config_visual"]["color_fondo"]};
        }}
    </style>
    """,
    unsafe_allow_html=True
)

def pantalla_configuracion():
    st.title("⚙️ Configuración del Sistema")
    st.markdown("""
        Este módulo permite personalizar y configurar aspectos claves del sistema, tales como usuarios,
        apariencia visual, configuración de la numeración consecutiva de facturas y accesos basados en roles específicos.
        Su finalidad es facilitar una administración ordenada, segura y personalizada del sistema de gestión para la tienda de maquillaje.
    """)

    tabs = st.tabs([
        "📋 Parámetros Generales",
        "👤 Administración de Usuarios",
        "⚙️ Gestión de Roles",
        "🎨 Configuración Visual",
        "🛠️ Configuración del Sistema"
    ])

    # --- Pestaña 1: Parámetros Generales ---
    with tabs[0]:
        st.subheader("📋 Parámetros Generales")

        config = cb.obtener_configuracion()
        nombre = st.text_input("Nombre de la tienda", value=st.session_state["config_general"]["nombre"])
        telefono = st.text_input("Número de contacto", value=config["telefono"])
        direccion = st.text_input("Dirección", value=config["direccion"])
        leyenda = st.text_area("Leyenda final de factura", value=config["leyenda_factura"])

        if st.button("Guardar configuración", key="guardar_config_general"):
            cb.guardar_configuracion(nombre, telefono, direccion, leyenda)

            st.session_state["config_general"] = {
                "nombre": nombre,
                "telefono": telefono,
                "direccion": direccion,
                "leyenda_factura": leyenda
            }

            st.success("✅ Configuración guardada correctamente")

    # --- Pestaña 2: Administración de Usuarios ---
    with tabs[1]:
        st.subheader("👥 Administración de Usuarios")

        with st.expander("➕ Registrar nuevo usuario", expanded=False):
            nombre = st.text_input("Nombre completo", key="nombre_usuario")
            correo = st.text_input("Correo electrónico (opcional)", key="correo_usuario")
            usuario = st.text_input("Nombre de usuario", key="user_usuario")
            contraseña = st.text_input("Contraseña", type="password", key="clave_usuario")

            if st.button("Guardar usuario", key="guardar_usuario"):
                ok = backend.crear_usuario(nombre, correo, usuario, contraseña)
                if ok:
                    st.success("✅ Usuario guardado correctamente")
                else:
                    st.error("❌ Error al guardar")

        st.divider()
        st.subheader("📄 Lista de Usuarios")
        usuarios = backend.obtener_usuarios()

        if usuarios:
            for i, u in enumerate(usuarios):
                cols = st.columns([3, 3, 2, 2, 1])
                cols[0].write(f"👤 **{u['nombre']}**")
                cols[1].write(f"📧 {u['correo'] or 'No registrado'}")
                cols[2].write(f"👥 Usuario: `{u['usuario']}`")
                estado = "🟢 Activo" if u["activo"] else "🔴 Inactivo"
                cols[3].write(estado)
                if u["activo"]:
                    if cols[4].button("Inactivar", key=f"inactivar_{i}"):
                        backend.cambiar_estado_usuario(i, False)
                else:
                    if cols[4].button("Activar", key=f"activar_{i}"):
                        backend.cambiar_estado_usuario(i, True)
        else:
            st.info("ℹ️ No hay usuarios registrados aún.")

    # --- Pestaña 3: Gestión de Roles y Permisos ---
    with tabs[2]:
        st.title("⚙️ Gestión de Roles y Permisos")

        st.markdown("Define los roles y los permisos asociados para controlar el acceso y funcionalidades dentro del sistema.")
        roles = list(cb.ROLES.keys())
        rol_tabs = st.tabs(roles)

        for i, rol in enumerate(roles):
            with rol_tabs[i]:
                detalles = cb.ROLES[rol]
                st.subheader(f"🔐 Rol: {rol}")
                st.markdown(f"**Descripción:** {detalles['descripcion']}")
                st.markdown("**Permisos:**")
                for permiso in detalles['permisos']:
                    st.markdown(f"- {permiso}")

        st.markdown("---")
        st.subheader("Asignar usuarios a roles")
        usuarios = cb.obtener_usuarios()
        rol_seleccionado = st.selectbox("Selecciona un rol para asignar usuarios", roles)
        usuarios_seleccionados = st.multiselect(f"Usuarios para el rol {rol_seleccionado}", usuarios, key=f"usuarios_{rol_seleccionado}")

        if st.button("Guardar asignación", key="guardar_asignacion_roles"):
            exito = cb.guardar_asignacion_usuarios(rol_seleccionado, usuarios_seleccionados)
            if exito:
                st.success(f"Usuarios {', '.join(usuarios_seleccionados)} asignados al rol {rol_seleccionado}")
            else:
                st.error("Error al guardar la asignación. Intenta nuevamente.")

    # --- Pestaña 4: Configuración Visual ---
    with tabs[3]:
        st.subheader("🎨 Configuración Visual y Personalización")
        st.markdown("Personaliza el sistema con la imagen y colores de tu tienda.")

        st.markdown("#### 🖼️ Logo de la tienda")
        st.image("https://via.placeholder.com/300x100.png?text=LOGO+TIENDA", width=300, caption="Vista previa del logo (imagen de prueba)")
        st.info("Esta es una imagen de prueba. Próximamente se podrá subir un logo personalizado.")

        st.divider()

        st.markdown("#### 🎨 Colores corporativos")
        color_primario = st.color_picker(
            "Color primario del sistema",
            value=st.session_state["config_visual"]["color_primario"],
            key="color_primario_picker"
        )

        if st.button("Guardar diseño visual", key="guardar_diseno_visual"):
            if color_primario != st.session_state["config_visual"]["color_primario"]:
                cb.guardar_configuracion_visual(color_primario)
                update_config_visual(color_primario)
                st.success("✅ Configuración visual guardada correctamente")
            else:
                st.info("ℹ️ No se realizaron cambios en los colores")
    # --- Pestaña 5: Configuración del Sistema ---
    with tabs[4]:
        st.subheader("🛠️ Configuración del Sistema")
        st.markdown("Ajusta parámetros importantes como el formato de fechas y la numeración consecutiva de las facturas.")

        st.markdown("### 🗓️ Formato de Fecha y Hora")
        formatos_fecha = {
            "DD/MM/AAAA": "%d/%m/%Y",
            "MM-DD-AAAA": "%m-%d-%Y",
            "AAAA.MM.DD": "%Y.%m.%d",
            "ISO (AAAA-MM-DD)": "%Y-%m-%d"
        }

        formato_actual = st.session_state["config_sistema"]["formato_fecha"]
        formato_legible = next((k for k, v in formatos_fecha.items() if v == formato_actual), "DD/MM/AAAA")
        formato_seleccionado = st.selectbox("Formato preferido para fechas:", list(formatos_fecha.keys()), index=list(formatos_fecha.keys()).index(formato_legible))

        st.markdown("---")
        st.markdown("### 🧾 Numeración de Facturas")
        prefijo_factura = st.text_input("Prefijo (opcional)", value=st.session_state["config_sistema"]["prefijo_factura"])
        consecutivo_inicial = st.number_input("Número inicial del consecutivo", min_value=1, step=1, value=st.session_state["config_sistema"]["consecutivo_inicial"])
        formato_muestra = f"{prefijo_factura}{consecutivo_inicial:05d}"
        st.info(f"Ejemplo de factura: **{formato_muestra}**")

        if st.button("Guardar configuración del sistema", key="guardar_config_sistema"):
            cb.guardar_configuracion_sistema(formatos_fecha[formato_seleccionado], prefijo_factura, consecutivo_inicial)
            update_config_sistema(formatos_fecha[formato_seleccionado], prefijo_factura, consecutivo_inicial)
            st.success("✅ Configuración del sistema guardada correctamente")

import streamlit as st
from backend_logic import configuracion as cb
from backend_logic import usuarios as backend  # Asegúrate de tener este archivo

def pantalla_configuracion():
    st.title("⚙️ Configuración del Sistema")
    st.markdown("""
        Este módulo permite personalizar y configurar aspectos claves del sistema, tales como usuarios,
        apariencia visual, configuración de la numeración consecutiva de facturas y accesos basados en roles específicos.
        Su finalidad es facilitar una administración ordenada, segura y personalizada del sistema de gestión para la tienda de maquillaje.
    """)

    tabs = st.tabs(["📋 Parámetros Generales", "👤 Administración de Usuarios", "⚙️ Gestión de Roles"])

    # --- Pestaña 1: Parámetros Generales ---
    with tabs[0]:
        st.subheader("📋 Parámetros Generales")

        config = cb.obtener_configuracion()

        nombre = st.text_input("Nombre de la tienda", value=config["nombre_tienda"])
        telefono = st.text_input("Número de contacto", value=config["telefono"])
        direccion = st.text_input("Dirección", value=config["direccion"])
        leyenda = st.text_area("Leyenda final de factura", value=config["leyenda_factura"])

        if st.button("Guardar configuración"):
            cb.guardar_configuracion(nombre, telefono, direccion, leyenda)
            st.success("✅ Configuración guardada correctamente (modo simulado)")

    # --- Pestaña 2: Administración de Usuarios ---
    with tabs[1]:
        st.subheader("👥 Administración de Usuarios")

        with st.expander("➕ Registrar nuevo usuario", expanded=False):
            nombre = st.text_input("Nombre completo", key="nombre_usuario")
            correo = st.text_input("Correo electrónico (opcional)", key="correo_usuario")
            usuario = st.text_input("Nombre de usuario", key="user_usuario")
            contraseña = st.text_input("Contraseña", type="password", key="clave_usuario")

            if st.button("Guardar usuario"):
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
                        st.experimental_rerun()
                else:
                    if cols[4].button("Activar", key=f"activar_{i}"):
                        backend.cambiar_estado_usuario(i, True)
                        st.experimental_rerun()
        else:
            st.info("ℹ️ No hay usuarios registrados aún.")

    # --- Pestaña 3: Gestión de Roles y Permisos ---
    with tabs[2]:
        st.title("⚙️ Gestión de Roles y Permisos")

        st.markdown("""
        Define los roles y los permisos asociados para controlar el acceso y funcionalidades dentro del sistema.
        """)

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

        usuarios_seleccionados = st.multiselect(
            f"Usuarios para el rol {rol_seleccionado}",
            usuarios,
            key=f"usuarios_{rol_seleccionado}"  # evita conflictos
        )

        if st.button("Guardar asignación"):
            exito = cb.guardar_asignacion_usuarios(rol_seleccionado, usuarios_seleccionados)
            if exito:
                st.success(f"Usuarios {', '.join(usuarios_seleccionados)} asignados al rol {rol_seleccionado}")
            else:
                st.error("Error al guardar la asignación. Intenta nuevamente.")

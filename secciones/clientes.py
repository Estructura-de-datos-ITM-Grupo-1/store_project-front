import streamlit as st
import pandas as pd
import backend_logic.reportes as backend_reportes


def sidebar_menu():
    st.sidebar.markdown("## 🌟 Gestión Empresarial", unsafe_allow_html=True)
    st.sidebar.markdown("---")

    menu = {
        "📊 Reportes": "reportes",
        "🗂️ Gestión de Clientes": "clientes",
        "📋 Otra Sección": "otra"
    }

    seleccion = st.sidebar.radio("Navegación", list(menu.keys()))
    return menu[seleccion]


def pantalla_clientes():
    st.title("🗂️ Gestión de Clientes")
    st.markdown('<p class="small-desc">Aquí puedes visualizar, editar o agregar clientes al sistema.</p>', unsafe_allow_html=True)

    df_clientes = backend_reportes.cargar_clientes()

  
    if st.button("🔤 Ordenar clientes A → Z"):
        df_clientes = df_clientes.sort_values("Cliente", ascending=True).reset_index(drop=True)
        st.success("Clientes ordenados alfabéticamente por nombre.")

    st.markdown("⚠️ *Recuerda presionar Enter o hacer clic fuera de una celda después de editarla para que se registre el cambio.*")

    
    if "clientes_editado" not in st.session_state:
        st.session_state.clientes_editado = df_clientes

    st.session_state.clientes_editado = st.data_editor(
        st.session_state.clientes_editado,
        num_rows="dynamic",
        use_container_width=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("💾 Guardar cambios"):
            backend_reportes.guardar_clientes_crud(st.session_state.clientes_editado)
            st.success("✅ Cambios guardados correctamente.")

    with col2:
        excel_data = backend_reportes.convertir_a_excel(st.session_state.clientes_editado)
        st.download_button(
            label="📥 Descargar Excel",
            data=excel_data,
            file_name="clientes_actualizado.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    with col3:
        st.info("✏️ Puedes editar directamente en la tabla.")


def pantalla_otra():
    st.title("📋 Otra Sección")
    st.write("Contenido de ejemplo.")



def main():
    st.set_page_config(page_title="Dashboard Empresarial", layout="wide", page_icon="📊")
    pagina = sidebar_menu()

    if pagina == "clientes":
        pantalla_clientes()
    elif pagina == "reportes":
        st.write("")  
    elif pagina == "otra":
        pantalla_otra()


if __name__ == "__main__":
    main()

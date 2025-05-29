import streamlit as st
import pandas as pd
import backend_logic.reportes as backend_reportes

def pantalla_reportes():
    st.title("📊 Reportes")

    st.markdown('<p class="small-desc">Explora las siguientes secciones para obtener información detallada:</p>', unsafe_allow_html=True)
    
    tabs = st.tabs([
        "📦 Movimientos de Inventario",
        "💅 Servicios Realizados",
        "👥 Clientes Frecuentes",
        "📈 Desempeño Financiero"
    ])

    # ===== REPORTE DE MOVIMIENTOS DE INVENTARIO =====
    with tabs[0]:
        st.subheader("📦 Reporte de Movimientos de Inventario")

        df = backend_reportes.cargar_movimientos_inventario()
        hoy = pd.Timestamp.today().normalize()

        modo_filtro_inv = st.radio("Filtrar por:", ["Tipo de reporte", "Rango de fechas manual"], horizontal=True, key="modo_filtro_inventario")

        if modo_filtro_inv == "Tipo de reporte":
            tipo_reporte = st.selectbox("Tipo de reporte", ["Diario", "Semanal", "Mensual", "Anual"], key="tipo_reporte_inv")

            if tipo_reporte == "Diario":
                fecha_inicio_inv = hoy
                fecha_fin_inv = hoy
            elif tipo_reporte == "Semanal":
                fecha_inicio_inv = hoy - pd.Timedelta(days=7)
                fecha_fin_inv = hoy
            elif tipo_reporte == "Mensual":
                fecha_inicio_inv = hoy - pd.DateOffset(months=1)
                fecha_fin_inv = hoy
            elif tipo_reporte == "Anual":
                fecha_inicio_inv = hoy - pd.DateOffset(years=1)
                fecha_fin_inv = hoy

            st.write(f"Mostrando resultados del **{fecha_inicio_inv.date()}** al **{fecha_fin_inv.date()}**")
        else:
            fecha_inicio_inv = st.date_input("📅 Fecha inicio", df['Fecha'].min().date(), key="fecha_inicio_inv")
            fecha_fin_inv = st.date_input("📅 Fecha fin", df['Fecha'].max().date(), key="fecha_fin_inv")

        fecha_inicio_inv = pd.to_datetime(fecha_inicio_inv)
        fecha_fin_inv = pd.to_datetime(fecha_fin_inv)

        tipos = st.multiselect("📂 Tipo de movimiento", df['Tipo'].unique(), default=df['Tipo'].unique(), key="tipos_inv")
        productos = st.multiselect("💄 Producto", df['Producto'].unique(), default=df['Producto'].unique(), key="productos_inv")
        responsables = st.multiselect("👤 Responsable", df['Responsable'].unique(), default=df['Responsable'].unique(), key="responsables_inv")

        df_filtrado = df[
            (df['Fecha'] >= fecha_inicio_inv) &
            (df['Fecha'] <= fecha_fin_inv) &
            (df['Tipo'].isin(tipos)) &
            (df['Producto'].isin(productos)) &
            (df['Responsable'].isin(responsables))
        ]

        st.dataframe(df_filtrado)

        excel_data = backend_reportes.convertir_a_excel(df_filtrado)
        st.download_button(
            label="📥 Descargar Excel",
            data=excel_data,
            file_name='reporte_movimientos_inventario.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

    # ===== REPORTE DE SERVICIOS REALIZADOS =====
    with tabs[1]:
        st.subheader("💅 Reporte de Servicios Realizados")

        df_srv = backend_reportes.cargar_servicios()
        hoy = pd.Timestamp.today().normalize()

        modo_filtro_srv = st.radio("Filtrar por:", ["Tipo de reporte", "Rango de fechas manual"], horizontal=True, key="modo_filtro_servicios")

        if modo_filtro_srv == "Tipo de reporte":
            tipo_reporte_srv = st.selectbox("Tipo de reporte", ["Diario", "Semanal", "Mensual", "Anual"], key="tipo_reporte_srv")

            if tipo_reporte_srv == "Diario":
                fecha_inicio_srv = hoy
                fecha_fin_srv = hoy
            elif tipo_reporte_srv == "Semanal":
                fecha_inicio_srv = hoy - pd.Timedelta(days=7)
                fecha_fin_srv = hoy
            elif tipo_reporte_srv == "Mensual":
                fecha_inicio_srv = hoy - pd.DateOffset(months=1)
                fecha_fin_srv = hoy
            elif tipo_reporte_srv == "Anual":
                fecha_inicio_srv = hoy - pd.DateOffset(years=1)
                fecha_fin_srv = hoy

            st.write(f"Mostrando resultados del **{fecha_inicio_srv.date()}** al **{fecha_fin_srv.date()}**")
        else:
            fecha_inicio_srv = st.date_input("📅 Fecha inicio", df_srv['Fecha'].min().date(), key="fecha_inicio_srv")
            fecha_fin_srv = st.date_input("📅 Fecha fin", df_srv['Fecha'].max().date(), key="fecha_fin_srv")

        fecha_inicio_srv = pd.to_datetime(fecha_inicio_srv)
        fecha_fin_srv = pd.to_datetime(fecha_fin_srv)

        empleados = st.multiselect("👤 Empleado", options=df_srv['Empleado'].unique(), default=df_srv['Empleado'].unique(), key="empleados_srv")
        servicios = st.multiselect("💅 Servicio", options=df_srv['Servicio'].unique(), default=df_srv['Servicio'].unique(), key="servicios_srv")

        df_srv_filtrado = df_srv[
            (df_srv['Fecha'] >= fecha_inicio_srv) &
            (df_srv['Fecha'] <= fecha_fin_srv) &
            (df_srv['Empleado'].isin(empleados)) &
            (df_srv['Servicio'].isin(servicios))
        ]

        st.dataframe(df_srv_filtrado)

        excel_srv = backend_reportes.convertir_a_excel(df_srv_filtrado)
        st.download_button(
            label="📥 Descargar Excel (Servicios)",
            data=excel_srv,
            file_name='reporte_servicios.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

    # ===== REPORTE DE CLIENTES FRECUENTES =====
    with tabs[2]:
        st.subheader("👥 Reporte de Clientes Frecuentes")

        df = backend_reportes.cargar_clientes()
        hoy = pd.Timestamp.today().normalize()

        modo_filtro = st.radio("Filtrar por:", ["Tipo de reporte", "Rango de fechas manual"], horizontal=True, key="modo_filtro_clientes")

        if modo_filtro == "Tipo de reporte":
            tipo_reporte = st.selectbox("Tipo de reporte", ["Diario", "Semanal", "Mensual", "Anual"], key="tipo_reporte_clientes")
            if tipo_reporte == "Diario":
                fecha_inicio = hoy
                fecha_fin = hoy
            elif tipo_reporte == "Semanal":
                fecha_inicio = hoy - pd.Timedelta(days=7)
                fecha_fin = hoy
            elif tipo_reporte == "Mensual":
                fecha_inicio = hoy - pd.DateOffset(months=1)
                fecha_fin = hoy
            elif tipo_reporte == "Anual":
                fecha_inicio = hoy - pd.DateOffset(years=1)
                fecha_fin = hoy
        else:
            fecha_inicio = st.date_input("📅 Fecha inicio", df['Fecha'].min().date(), key="fecha_inicio_clientes")
            fecha_fin = st.date_input("📅 Fecha fin", df['Fecha'].max().date(), key="fecha_fin_clientes")

        fecha_inicio = pd.to_datetime(fecha_inicio)
        fecha_fin = pd.to_datetime(fecha_fin)

        df_filtrado = df[(df['Fecha'] >= fecha_inicio) & (df['Fecha'] <= fecha_fin)]

        resumen = df_filtrado.groupby('Cliente').agg(
            Compras=('Cliente', 'count'),
            Total_gastado=('Monto', 'sum')
        ).reset_index()

        resumen = resumen.sort_values(by='Compras', ascending=False)

        st.dataframe(resumen)

        excel_data = backend_reportes.convertir_a_excel(resumen)
        st.download_button(
            label="📥 Descargar Excel (Clientes Frecuentes)",
            data=excel_data,
            file_name='reporte_clientes_frecuentes.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

    # ===== REPORTE DE DESEMPEÑO FINANCIERO =====
    with tabs[3]:
        st.subheader("📊 Desempeño Financiero del Negocio")

        modo = st.radio("Visualizar por:", ["Diario", "Semanal", "Mensual", "Anual"], horizontal=True, key="modo_desempeno")

        df = backend_reportes.generar_datos_financieros(modo)

        df = df.sort_values("Fecha")
        df.set_index("Fecha", inplace=True)

        st.dataframe(df)
        st.line_chart(df[["Ingresos", "Egresos"]])

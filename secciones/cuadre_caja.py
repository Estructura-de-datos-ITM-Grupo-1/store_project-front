import streamlit as st
import pandas as pd
import backend_logic.cuadre_caja_logic as backend_cuadre_caja
from datetime import datetime


def pantalla_cuadre_caja():
    st.title("📠 Cuadre Caja")

    st.markdown('<p class="small-desc">Explora las siguientes secciones para obtener información detallada:</p>', unsafe_allow_html=True)
    
    # Definir los tabs correctamente y guardarlos en una variable
    tabs = st.tabs([
        "📊 Ventas",
        "📝	Información General del Cuadre",
        "💰 Egresos",
        "💵 Efectivo en Caja",
        "🔢 Cálculos",
        "📈 Reporte Final"
    ])

    # Acceder correctamente al primer tab (Resumen de Ventas)
    with tabs[0]:  # Ahora accedes correctamente al primer tab
        st.subheader("📊 Detalle de Ventas del Día")
        st.write("Listado completo de artículos y servicios vendidos en la fecha actual.")

        df_ventas = backend_cuadre_caja.cargar_ventas_diarias()
        metodos_pago = ["Efectivo", "Transferencia electrónica", "Tarjeta"]
        metodo_seleccionado = st.selectbox("Filtrar por método de pago", metodos_pago, key="filtro_metodo_pago")

        df_filtrado = df_ventas[df_ventas['Método de Pago'] == metodo_seleccionado]

        # Mostrar datos filtrados
        st.dataframe(df_filtrado[['Descripción', 'Cantidad', 'Precio Unitario', 'Total', 'Método de Pago']])

        # Calcular total de ingresos
        total_ingresos = df_filtrado['Total'].sum()
        st.metric("Total Vendido", f"${total_ingresos:.2f}")

        # Exportación del reporte
        excel_ventas = backend_cuadre_caja.convertir_a_excel(df_filtrado)
        st.download_button(
            label="📥 Descargar Reporte de Ventas",
            data=excel_ventas,
            file_name='resumen_diario_ventas.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    with tabs[1]:
        st.subheader("📋 Información General del Cuadre")
        st.write("Aquí puedes visualizar los detalles del cuadre de caja.")

        # Datos dinámicos
        fecha_actual = datetime.today().strftime('%Y-%m-%d')
        usuario_actual = "Usuario123"
        base_caja = backend_cuadre_caja.obtener_base_caja()

        col1, col2, col3 = st.columns(3)
        col1.metric("📅 Fecha", fecha_actual)
        col2.metric("👤 Responsable", usuario_actual)
        col3.metric("💰 Base de Caja", f"${base_caja:.2f}")

        nueva_base_caja = st.number_input("Modificar Base de Caja:", value=base_caja, step=5000)

        if st.button("Actualizar Base de Caja"):
            backend_cuadre_caja.actualizar_base_caja(nueva_base_caja)
            st.success(f"Base de Caja actualizada a ${nueva_base_caja:.2f}")
            
    with tabs[2]:
        st.subheader("💰 Egresos del Día")
        st.write("Lista de egresos registrados en el día.")

        # Cargar datos reales desde el backend
        df_egresos = backend_cuadre_caja.cargar_egresos_diarios()

         # Mostrar datos en Streamlit
        st.dataframe(df_egresos)

        # Calcular total de egresos
        total_egresos = df_egresos['Monto'].sum()
        st.metric("Total Egresos", f"${total_egresos:.2f}")

    with tabs[3]:  
        st.subheader("💵 Conteo de Efectivo en Caja")
        st.write("Ingresa el monto exacto del efectivo presente en caja.")
    
        efectivo_manual = st.number_input("Efectivo físico en caja:", min_value=0, step=5000)
        st.write(f"💰 **Efectivo declarado:** ${efectivo_manual:.2f}")

    # ===== 5. Cálculos Automáticos =====
    with tabs[4]:
        st.subheader("🔢 Cálculos Automáticos")

        # Obtener datos desde el backend
        total_ingresos = backend_cuadre_caja.obtener_total_ingresos()
        total_egresos = backend_cuadre_caja.obtener_total_egresos()
        utilidad_dia = total_ingresos - total_egresos
        base_caja = backend_cuadre_caja.obtener_base_caja()

        # Comparación de efectivo en sistema vs físico
        diferencia_caja = efectivo_manual - (total_ingresos - total_egresos)
        estado_cuadre = "✅ Cuadre Correcto" if diferencia_caja == 0 else "⚠️ Descuadre Detectado"

        # Dinero que consignar
        dinero_consignar = (total_ingresos - backend_cuadre_caja.obtener_pagos_en_otros_medios()) - base_caja

        # Mostrar métricas
        col1, col2, col3 = st.columns(3)
        col1.metric("📈 Total Ingresos", f"${total_ingresos:.2f}")
        col2.metric("💰 Total Egresos", f"${total_egresos:.2f}")
        col3.metric("📊 Utilidad del Día", f"${utilidad_dia:.2f}")

        st.subheader("🛠 Validación y Cuadre de Caja")
        st.write(f"🔍 **Diferencia en caja:** ${diferencia_caja:.2f} - {estado_cuadre}")
        st.metric("🏦 Dinero que consignar", f"${dinero_consignar:.2f}")

    # ===== 6. Reporte Final =====
    with tabs[5]:
        st.subheader("📈 Reporte Final del Cuadre")

        # Generar DataFrame con la información
        datos_reporte = {
            "Fecha": [datetime.today().strftime('%Y-%m-%d')],
            "Usuario": ["Usuario123"],
            "Total Ingresos": [total_ingresos],
            "Total Egresos": [total_egresos],
            "Utilidad del Día": [utilidad_dia],
            "Efectivo Declarado": [efectivo_manual],
            "Diferencia en Caja": [diferencia_caja],
            "Dinero a Consignar": [dinero_consignar]
        }
        df_reporte = pd.DataFrame(datos_reporte)

        st.dataframe(df_reporte)

        # Exportación a PDF/Excel
        excel_reporte = backend_cuadre_caja.convertir_a_excel(df_reporte)
        st.download_button(
            label="📥 Descargar Reporte en Excel",
            data=excel_reporte,
            file_name='reporte_final.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

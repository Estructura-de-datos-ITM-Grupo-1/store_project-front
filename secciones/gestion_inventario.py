import streamlit as st
from backend_logic import inventario  # Asumo que backend_logic es tu módulo backend

def pantalla_inventario():

    st.title("Gestión de Inventario")

    # --- Tabs para registro y agregar cantidad ---
    tab1, tab2 = st.tabs(["➕ Registro de Producto Nuevo", "➕ Agregar Cantidad Adicional"])

    # --- Registro de Producto Nuevo ---
    with tab1:
        st.header("Registro de Producto Nuevo")
        with st.form("form_registro_producto"):
            nombre = st.text_input("Nombre del Producto")
            descripcion = st.text_area("Descripción del Producto (presentación, detalles)")
            categoria = st.text_input("Categoría")
            marca = st.text_input("Marca")
            referencia = st.text_input("Código Interno (Referencia única)")
            color = st.text_input("Color")
            valor_costo = st.number_input("Valor de Costo", min_value=0.0, format="%.2f")
            valor_venta = st.number_input("Valor de Venta", min_value=0.0, format="%.2f")
            cantidad = st.number_input("Cantidad Ingresada", min_value=0, step=1)

            submitted = st.form_submit_button("Registrar Producto")
            if submitted:
                if not nombre or not referencia or not marca:
                    st.error("Por favor, completa los campos obligatorios: Nombre, Código Interno y Marca.")
                else:
                    ok, mensaje = inventario.crear_producto(
                        nombre=nombre,
                        descripcion=descripcion,
                        categoria=categoria,
                        marca=marca,
                        referencia=referencia,
                        color=color,
                        valor_costo=valor_costo,
                        valor_venta=valor_venta,
                        cantidad=cantidad
                    )
                    if ok:
                        st.success(mensaje)
                    else:
                        st.error(mensaje)

    # --- Agregar Cantidad Adicional ---
    with tab2:
        st.header("Agregar Cantidad Adicional al Inventario")

        productos = inventario.obtener_productos_con_nombre()
        if not productos:
            st.info("No hay productos registrados.")
        else:
            # ref_dict: clave "Nombre (Referencia)" -> referencia
            ref_dict = {f"{nombre} ({ref})": ref for ref, nombre in productos}
            seleccion = st.selectbox("Selecciona producto por Código Interno", list(ref_dict.keys()))
            referencia_seleccionada = ref_dict[seleccion]

            producto = inventario.obtener_producto_por_referencia(referencia_seleccionada)
            if producto:
                st.write("### Datos actuales del producto:")
                st.write(f"**Nombre:** {producto['nombre']}")
                st.write(f"**Cantidad Actual en Inventario:** {producto['cantidad']}")

                cantidad_adicional = st.number_input("Cantidad adicional a agregar", min_value=1, step=1)

                if st.button("Agregar Stock"):
                    ok, mensaje = inventario.agregar_stock(referencia_seleccionada, cantidad_adicional)
                    if ok:
                        st.success(mensaje)
                        st.experimental_rerun()
                    else:
                        st.error(mensaje)
            else:
                st.error("Producto no encontrado.")

    st.markdown("---")

    # --- Actualizar Producto Existente ---
    st.title("✏️ Actualizar Producto Existente")
    productos = inventario.obtener_productos_con_nombre()
    if productos:
        ref_dict = {f"{nombre} ({ref})": ref for ref, nombre in productos}
        seleccion = st.selectbox("Selecciona producto", ["Selecciona..."] + list(ref_dict.keys()))

        if seleccion != "Selecciona...":
            referencia = ref_dict[seleccion]
            st.success(f"Referencia seleccionada: {referencia}")

            with st.form("form_actualizar"):
                nuevo_nombre = st.text_input("Nuevo nombre")
                nueva_categoria = st.text_input("Nueva categoría")
                nueva_marca = st.text_input("Nueva marca")
                nuevo_color = st.text_input("Nuevo color")
                nuevo_precio = st.number_input("Nuevo precio", min_value=0.0, format="%.2f")

                if st.form_submit_button("💾 Actualizar"):
                    exito, mensaje = inventario.actualizar_producto(
                        referencia,
                        nombre=nuevo_nombre,
                        categoria=nueva_categoria,
                        marca=nueva_marca,
                        color=nuevo_color,
                        precio=nuevo_precio
                    )
                    if exito:
                        st.success(mensaje)
                    else:
                        st.error(mensaje)
        else:
            st.warning("Selecciona un producto para actualizar.")
    else:
        st.warning("No hay productos registrados.")

    st.markdown("---")

    # --- Movimiento de Inventario ---
    st.title("🔄 Movimiento de Inventario")
    st.markdown("Automatiza entradas y salidas de productos con actualización en tiempo real.")

    productos = inventario.obtener_productos_con_nombre()
    if not productos:
        st.info("No hay productos registrados.")
        return

    ref_dict = {f"{nombre} ({ref})": ref for ref, nombre in productos}
    seleccion = st.selectbox("📦 Selecciona producto", list(ref_dict.keys()))
    referencia = ref_dict[seleccion]

    tipo = st.radio("Tipo de movimiento", ["Entrada", "Salida"], horizontal=True)
    cantidad_mov = st.number_input("Cantidad", min_value=1, step=1)
    motivo = st.text_input("Motivo del movimiento")

    if st.button("📥 Registrar movimiento"):
        if motivo.strip() == "":
            st.warning("⚠️ Ingresa un motivo.")
        elif tipo == "Salida" and inventario.esta_bloqueado(referencia):
            st.error("❌ Producto con stock cero. No se permite venta hasta actualizar stock.")
        else:
            exito, mensaje = inventario.registrar_movimiento(
                referencia=referencia,
                tipo=tipo.lower(),
                cantidad=cantidad_mov,
                motivo=motivo
            )
            if exito:
                st.success(mensaje)
            else:
                st.error(mensaje)

    st.markdown("---")

    # --- Alertas de Inventario ---
    st.title("🚨 Alertas de Inventario")
    
    bajo_stock = inventario.obtener_productos_bajo_stock()
    alta_demanda = inventario.obtener_productos_alta_demanda()

    if bajo_stock:
        st.subheader("Productos con bajo stock")
        for ref, nombre, cantidad_disp in bajo_stock:
            st.warning(f"⚠️ {nombre} ({ref}) tiene solo {cantidad_disp} unidades disponibles.")
    else:
        st.success("👍 No hay productos con bajo stock.")

    st.markdown("---")

    if alta_demanda:
        st.subheader("Productos con alta demanda (últimos 7 días)")
        for ref, nombre, salidas in alta_demanda:
            st.info(f"📈 {nombre} ({ref}) tuvo {salidas} salidas esta semana.")
    else:
        st.success("👍 No hay productos con alta demanda.")

    # --- Historial de Movimientos ---
    st.title("📜 Historial de Movimientos de Inventario")

    historial = inventario.obtener_historial_movimientos()
    if not historial:
        st.info("No hay movimientos registrados aún.")
        return

    for mov in historial:
        fecha_str = mov['fecha'].strftime("%Y-%m-%d %H:%M:%S")
        producto = next((p for p in inventario.productos if p['referencia'] == mov['referencia']), None)
        nombre = producto['nombre'] if producto else "Producto no encontrado"
        st.write(f"- **{fecha_str}** | Producto: {nombre} ({mov['referencia']}) | Tipo: {mov['tipo'].capitalize()} | Cantidad: {mov['cantidad']} | Motivo: {mov['motivo'].capitalize()}")

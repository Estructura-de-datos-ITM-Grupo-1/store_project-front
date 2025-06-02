import streamlit as st
import pandas as pd
from datetime import datetime
import json
import base64
from pathlib import Path
from typing import Optional, List, Dict, Any
import io 
import zipfile 
from streamlit_autorefresh import st_autorefresh

st.set_page_config(layout="wide", page_title="LUXBEAUTY LAB - Sistema de Facturación")


from models import MedioPago, Cliente, Producto, Servicio, ItemFactura, Factura
from data_manager import DataManager
from utils import format_currency, generate_invoice_number, calculate_invoice_totals, set_invoice_number_config, _invoice_prefix, _invoice_suffix
from invoice_generator import generate_invoice_pdf, prepare_logo

def validate_invoice_data(client, items, payment_method):
    errors = []
    
    if not client:
        errors.append("• Cliente es obligatorio")
    
    if not items:
        errors.append("• Debe agregar al menos un ítem a la factura")
    
    if not payment_method:
        errors.append("• Medio de pago es obligatorio")
    
    
    for item in items:
        if item.producto and item.cantidad > item.producto.stock:
            errors.append(f"• Stock insuficiente para {item.producto.nombre}")
    
    return len(errors) == 0, errors

data_manager = DataManager()
def setup_assets():
    assets_dir = Path("assets")
    assets_dir.mkdir(exist_ok=True) 

    logo_original_path = assets_dir / "logo.jpg"
    logo_prepared_path = assets_dir / "logo_prepared.png" 

    with st.sidebar:
        if not logo_original_path.exists():
            st.warning("⚠️ Logo no encontrado")
            st.info(f"Coloca tu logo en: {logo_original_path}")
                        
            logo_for_pdf_path = None
        else:           
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(str(logo_original_path), width=500)
            logo_for_pdf_path = str(logo_prepared_path) 

        now = datetime.now()
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.title("LUXBEAUTY LAB")
        fecha_hora = now.strftime("%d/%m/%Y - %H:%M:%S")
        st.markdown(f"<p style='font-size: 14px; text-align: center;'>{fecha_hora}</p>", unsafe_allow_html=True) 
        st_autorefresh(interval=1000, key="date_time_refresh_sidebar") 
       
        if logo_original_path.exists():
            prepare_logo(str(logo_original_path), str(logo_prepared_path))

    return logo_for_pdf_path 

def setup_sidebar_navigation(menu_options: List[str]):
    with st.sidebar:
        
        st.markdown("---")      
        selected_option = st.radio(
            "Selecciona una opción:",
            menu_options,
            key="main_navigation"
        )
        st.markdown("---")        
    return selected_option 

def get_table_download_link(df: pd.DataFrame, filename: str, text: str):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href

def get_pdf_download_link_auto(file_path: str):
    if Path(file_path).exists():
        with open(file_path, "rb") as f:
            pdf_bytes = f.read()
        b64 = base64.b64encode(pdf_bytes).decode()
        
        js_code = f"""
            <script>
                var link = document.createElement('a');
                link.href = 'data:application/pdf;base64,{b64}';
                link.download = '{Path(file_path).name}';
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            </script>
        """
        return js_code
    return "" 

def show_invoice_details(invoice_row):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**📋 Número:** {invoice_row.get('numero', 'N/A')}")
        st.markdown(f"**📅 Fecha:** {invoice_row.get('fecha', 'N/A')}")
        st.markdown(f"**👤 Cliente:** {invoice_row.get('cliente_nombre', 'N/A')}")
        st.markdown(f"**🆔 Documento:** {invoice_row.get('cliente_documento', 'N/A')}")
    
    with col2:
        st.markdown(f"**💳 Medio de Pago:** {invoice_row.get('medio_pago', 'N/A')}")
        st.markdown(f"**💰 Total:** ${invoice_row.get('total_factura', invoice_row.get('total', 0)):,.0f}")
        st.markdown(f"**📝 Observaciones:** {invoice_row.get('observaciones', 'Sin observaciones')}")
    
    
    if 'items_json' in invoice_row and invoice_row['items_json']:
        # Detalles de los ítems de la factura
        items = invoice_row['items_json']
        if isinstance(items, list) and len(items) > 0:
            
            items_data = []
            for item in items:
                if isinstance(item, dict):
                    items_data.append({
                        'Tipo': 'Producto' if item.get('producto_nombre') else 'Servicio',
                        'Nombre': item.get('producto_nombre') or item.get('servicio_nombre', 'N/A'),
                        'Cantidad': item.get('cantidad', 0),
                        'Precio Unit.': f"${item.get('precio_unitario', 0):,.0f}",
                        'Descuento %': f"{item.get('descuento', 0):.1f}%",
                        'IVA %': f"{item.get('iva', 0):.1f}%",
                        'Total': f"${item.get('total', 0):,.0f}"
                    })
            
            if items_data:
                items_df = pd.DataFrame(items_data)
                st.dataframe(items_df, use_container_width=True)
            else:
                st.info("No se pudieron cargar los detalles de los items.")
        else:
            st.info("Esta factura no tiene items registrados.")
    
    
    st.markdown("---")
    subtotal = invoice_row.get('subtotal', 0)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Subtotal", f"${subtotal:,.0f}" if pd.notna(subtotal) else "$0")
    with col2:
        descuento = invoice_row.get('descuento_total_factura', 0)
        st.metric("Descuento", f"${descuento:,.0f}" if pd.notna(descuento) else "$0")
    with col3:
        iva = invoice_row.get('iva_total_factura', 0)
        st.metric("IVA", f"${iva:,.0f}" if pd.notna(iva) else "$0")
    with col4:
        total = invoice_row.get('total_factura', invoice_row.get('total', 0))
        st.metric("Total Final", f"${total:,.0f}" if pd.notna(total) else "$0")

def show_billing_module_page(logo_path: Optional[str] = None, selected_option: str = None):
    st.subheader("🧾 Módulo de Facturación")
    st.markdown("---")
    product_options = {p.nombre: p for p in st.session_state.all_products}
    service_options = {s.nombre: s for s in st.session_state.all_services}
    client_options = {f"{c.nombre} ({c.documento})": c for c in st.session_state.all_clients}

    st.header("Generar Nueva Factura")
    st.subheader("Datos del Cliente")
    selected_client_name = st.selectbox(
        "Seleccione Cliente Existente",
        options=[""] + list(client_options.keys()),
        key="selected_client_invoice"
    )
    current_client: Optional[Cliente] = None
    if selected_client_name:
        current_client = client_options[selected_client_name]
        st.write(f"**Nombre:** {current_client.nombre}")
        st.write(f"**Documento:** {current_client.documento}")
        st.write(f"**Teléfono:** {current_client.telefono}")
        st.write(f"**Email:** {current_client.email}")
        st.write(f"**Dirección:** {current_client.direccion}")
    else:
        st.info("Seleccione un cliente o vaya a 'Gestión de Clientes' para añadir uno nuevo.")

    st.markdown("---")
    
    st.subheader("Añadir Productos a la Factura")
    if "invoice_items" not in st.session_state:
        st.session_state.invoice_items = []

    item_type = st.radio("Tipo de Ítem", ("Producto", "Servicio"), key="item_type_radio")
    selected_item = None
    if item_type == "Producto":
        product_selection_method = st.radio("Método de Selección", ("Lista Desplegable", "Código Rápido"), key="product_method_radio")
        
        if product_selection_method == "Lista Desplegable":
            selected_product_name = st.selectbox(
                "Seleccione Producto",
                options=[""] + list(product_options.keys()),
                key="selected_product_invoice"
            )
            if selected_product_name:
                selected_item = product_options[selected_product_name]
                
        else:  
            product_code = st.text_input("Ingrese Código del Producto", key="product_code_input")
            if product_code:
                
                for product in st.session_state.all_products:
                    if product.codigo.upper() == product_code.upper():
                        selected_item = product
                        break
                if not selected_item:
                    st.warning(f"No se encontró producto con código: {product_code}")
            
        if selected_item:
            st.write(f"Producto: {selected_item.nombre}")
            st.write(f"Precio: {format_currency(selected_item.precio)}")
            st.write(f"Stock Disponible: {selected_item.stock}")
            st.write(f"IVA Aplicable: {'Sí' if selected_item.iva_aplicable else 'No'}")
    else: 
        service_type = st.radio("Tipo de Servicio", ("Existente", "Temporal"), key="service_type_radio")
        
        if service_type == "Existente":
            selected_service_name = st.selectbox(
                "Seleccione Servicio",
                options=[""] + list(service_options.keys()),
                key="selected_service_invoice"
            )
            if selected_service_name:
                selected_item = service_options[selected_service_name]
                st.write(f"Precio: {format_currency(selected_item.precio)}")
                st.write(f"Temporal: {'Sí' if selected_item.temporal else 'No'}")
                
        else:  
            temp_service_name = st.text_input("Concepto del Servicio Temporal", key="temp_service_name")
            temp_service_price = st.number_input("Valor del Servicio Temporal", min_value=0.0, format="%.2f", key="temp_service_price")
            
            if temp_service_name and temp_service_price > 0:
                
                selected_item = Servicio(
                    id=0,  
                    codigo=f"TEMP_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    nombre=temp_service_name,
                    precio=temp_service_price,
                    temporal=True
                    )
                st.write(f"Precio: {format_currency(selected_item.precio)}")
                st.write("Servicio Temporal: Sí")
            else:
                selected_item = None
    
    if "_default_quantity" not in st.session_state:
        st.session_state["_default_quantity"] = 1
    if "_default_discount" not in st.session_state:
        st.session_state["_default_discount"] = 0.0

    col1, col2, col3 = st.columns(3)
    with col1:
        item_quantity = st.number_input("Cantidad", min_value=1, value=st.session_state["_default_quantity"], key="item_quantity_invoice")
    with col2:
        item_discount = st.number_input("Descuento (%)", min_value=0.0, max_value=100.0, value=st.session_state["_default_discount"], key="item_discount_invoice")
    with col3:
        if selected_item:
            if item_type == "Producto" and hasattr(selected_item, 'iva_aplicable'):
                default_iva = 19.0 if selected_item.iva_aplicable else 0.0
            else:
                default_iva = 19.0  
        else:
            default_iva = 0.0
        item_iva = st.number_input("IVA (%)", min_value=0.0, max_value=100.0, value=default_iva, key="item_iva_invoice")

    if st.button(" ➕ Añadir Producto a la Factura", key="add_item_button"):
        if selected_item and item_quantity > 0:
            if item_type == "Producto" and item_quantity > selected_item.stock:
                st.error(f"No hay suficiente stock para {selected_item.nombre}. Stock disponible: {selected_item.stock}")
            else:
                new_item = ItemFactura(
                    producto=selected_item if item_type == "Producto" else None,
                    servicio=selected_item if item_type == "Servicio" else None,
                    cantidad=item_quantity,
                    precio_unitario=selected_item.precio,
                    descuento=item_discount,
                    iva=item_iva
                )
                st.session_state.invoice_items.append(new_item)
                st.success(f"'{selected_item.nombre}' añadido a la factura.")
                
                del st.session_state["item_quantity_invoice"]
                del st.session_state["item_discount_invoice"]
                
                st.session_state["_default_quantity"] = 1
                st.session_state["_default_discount"] = 0.0     
                st.rerun()
        else:
            st.warning("Por favor, seleccione un ítem y especifique una cantidad válida.")
    if "reset_form" in st.session_state and st.session_state.reset_form:
        
        st.session_state.reset_form = False

    st.markdown("---")

    st.subheader("Productos en la Factura")
    if st.session_state.invoice_items:
        invoice_items_data = []
        
        total_qty = 0
        total_subtotal = 0
        total_total = 0
        total_items = len(st.session_state.invoice_items)
        
        for i, item in enumerate(st.session_state.invoice_items):
            item_name = item.producto.nombre if item.producto else item.servicio.nombre
            item_type_display = "Producto" if item.producto else "Servicio"
            
            base = item.cantidad * item.precio_unitario
            descuento_pesos = base * (item.descuento / 100)
            subtotal_con_descuento = base - descuento_pesos
            iva = subtotal_con_descuento * (item.iva / 100)
            total = subtotal_con_descuento + iva
            total_qty += item.cantidad
            total_subtotal += subtotal_con_descuento
            total_total += total          
            invoice_items_data.append({
                "Tipo": item_type_display,
                "Descripción": item_name,
                "Cantidad": item.cantidad,
                "P. Unitario": format_currency(item.precio_unitario),
                "Desc. (%)": f"{item.descuento:.1f}%",
                "IVA (%)": f"{item.iva:.1f}%",
                "Subtotal Item": format_currency(subtotal_con_descuento),
                "Total Item": format_currency(total)
                
                })        
        average_discount = sum(item.descuento for item in st.session_state.invoice_items) / total_items if total_items else 0
        invoice_items_data.append({
            "Tipo": "**Resumen**", 
            "Descripción": "",
            "Cantidad": total_qty,
            "P. Unitario": "",
            "Desc. (%)": f"{average_discount:.1f}%",
            "IVA (%)": "19.0%",  
            "Subtotal Item": format_currency(total_subtotal),
            "Total Item": format_currency(total_total)
        })

        df_invoice = pd.DataFrame(invoice_items_data)
        st.dataframe(df_invoice, use_container_width=True)

        current_totals = calculate_invoice_totals(st.session_state.invoice_items)
        st.markdown(f"**Subtotal General:** {format_currency(current_totals['subtotal_base'])}")
        st.markdown(f"**Descuento Total:** {format_currency(current_totals['descuento_total'])}")
        st.markdown(f"**IVA Total:** {format_currency(current_totals['iva_total'])}")
        st.markdown(f"**Total a Pagar:** {format_currency(current_totals['total_factura'])}")

        if st.button("Vaciar Ítems de Factura", key="clear_items_button"):
            st.session_state.invoice_items = []
            st.rerun() 
    else:
        st.info("No hay ítems añadidos a la factura.")

    st.markdown("---")
    st.subheader("Detalles Finales de Factura")
    col1, col2 = st.columns(2)
    
    with col1:
        selected_payment_method = st.selectbox(
            "Medio de Pago",
            options=[mp.value for mp in MedioPago],
            key="payment_method_invoice"
        )
    with col2:
        invoice_observations = st.text_area("Observaciones", key="invoice_observations")
        
    current_invoice_num_preview = generate_invoice_number(preview=True)
    st.info(f"Número de Factura Propuesto: {current_invoice_num_preview}")

    if st.button("Generar Factura", key="generate_invoice_button"):
        is_valid, validation_errors = validate_invoice_data(
            current_client, 
            st.session_state.invoice_items, 
            selected_payment_method
            )
        if not is_valid:
            st.error("La factura no puede ser guardada. Errores encontrados:")
            for error in validation_errors:
                st.error(error)
        else:
            invoice_number = generate_invoice_number()
            invoice_date = datetime.now()
            final_totals = calculate_invoice_totals(st.session_state.invoice_items)
            new_invoice = Factura(
                numero=invoice_number,
                fecha=invoice_date,
                cliente=current_client,
                items=st.session_state.invoice_items,
                medio_pago=MedioPago(selected_payment_method),
                subtotal=final_totals['subtotal_base'],
                descuento_total=final_totals['descuento_total'],
                iva_total=final_totals['iva_total'],
                total=final_totals['total_factura'],
                observaciones=invoice_observations
            )
            success, message = data_manager.save_invoice_registro(new_invoice)
            if success:
                st.success(message)
                pdf_output_path = Path("data") / "invoices" / f"factura_{new_invoice.numero}.pdf"
                generate_invoice_pdf(new_invoice, str(pdf_output_path), logo_path)
                
                if pdf_output_path.exists():
                    st.success(f"Factura PDF generada en: {pdf_output_path}")
                    st.markdown(get_pdf_download_link_auto(str(pdf_output_path)), unsafe_allow_html=True)
                    st.info("La factura se ha descargado automáticamente. Revisa tu carpeta de descargas.")
                else:
                    st.error("Error al generar el PDF de la factura.")

                st.session_state.invoice_items = []
                st.rerun() 
            else:
                st.error(f"Error al guardar factura: {message}")

    st.markdown("---")
    st.markdown("---") 
    st.header("Registro de Facturas Emitidas")
    invoices_df = data_manager.get_all_invoices_registro()

    if not invoices_df.empty:
        if 'fecha' in invoices_df.columns and not invoices_df.empty:
            invoices_df['fecha'] = pd.to_datetime(invoices_df['fecha'], errors='coerce', format='mixed')
        
        invoices_df = invoices_df.sort_values(by='fecha', ascending=False)
        st.subheader("Filtros de Búsqueda")
        col_search1, col_search2, col_search3 = st.columns(3)
        
        with col_search1:
            
            client_names = ["Todos"] + invoices_df['cliente_nombre'].unique().tolist() if not invoices_df.empty else ["Todos"]
            selected_client_filter = st.selectbox("Filtrar por Cliente", client_names, key="client_filter")
            
        with col_search2:
            
            payment_methods = ["Todos"] + invoices_df['medio_pago'].unique().tolist() if not invoices_df.empty else ["Todos"]
            selected_payment_filter = st.selectbox("Filtrar por Medio de Pago", payment_methods, key="payment_filter")
            
        with col_search3:
            
            invoice_search = st.text_input("Buscar por Número de Factura", key="invoice_number_search")

        filtered_df = invoices_df.copy()
        
        if selected_client_filter != "Todos":
            filtered_df = filtered_df[filtered_df['cliente_nombre'] == selected_client_filter]
            
        if selected_payment_filter != "Todos":
            filtered_df = filtered_df[filtered_df['medio_pago'] == selected_payment_filter]
            
        if invoice_search:
            filtered_df = filtered_df[filtered_df['numero'].str.contains(invoice_search, case=False, na=False)]
        
        st.markdown("---")
        st.subheader("Historico de Facturas")
        if not filtered_df.empty:
            columns_to_display = [
                'numero',
                'fecha',
                'cliente_documento',
                'cliente_nombre',
                'medio_pago',
                'total_factura',
                'observaciones'
                ]
            existing_columns_to_display = [col for col in columns_to_display if col in filtered_df.columns]
            col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([1.5, 2, 1.8, 2.5, 2, 1.5, 2, 0.8])
            with col1:
                st.markdown("**Número**")
            with col2:
                st.markdown("**Fecha**")
            with col3:
                st.markdown("**Documento**")
            with col4:
                st.markdown("**Cliente**")
            with col5:
                st.markdown("**Medio Pago**")
            with col6:
                st.markdown("**Total**")
            with col7:
                st.markdown("**Observaciones**")
            with col8:
                st.markdown("**Ver**")
        
            st.markdown("---")
            for idx, row in filtered_df.iterrows():
                col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([1.5, 2, 1.8, 2.5, 2, 1.5, 2, 0.8])
            
                with col1:
                    st.text(str(row.get('numero', '')))
            
                with col2:
                    if pd.notna(row.get('fecha')):
                        try:
                            fecha_formatted = pd.to_datetime(row['fecha']).strftime('%Y-%m-%d %H:%M:%S')
                            st.text(fecha_formatted)
                        except:
                            st.text(str(row.get('fecha', '')))
                    else:
                        st.text('')
            
                with col3:
                    st.text(str(row.get('cliente_documento', '')))
            
                with col4:
                    st.text(str(row.get('cliente_nombre', '')))
            
                with col5:
                    st.text(str(row.get('medio_pago', '')))
            
                with col6:
                    
                    total = row.get('total_factura', row.get('total', 0))
                    if pd.notna(total):
                        st.text(f"${total:,.0f}")
                    else:
                        st.text('$0')
            
                with col7:
                    st.text(str(row.get('observaciones', '')))
            
                with col8:
                    invoice_key = f'show_invoice_{row.get("numero", "")}'
                    # Botón para mostrar/ocultar detalles
                    if st.button("👁️", key=f"view_{row.get('numero', '')}_{idx}", help="Ver factura completa"):
                        # Limpiar todos los estados de visualización primero
                        for key in list(st.session_state.keys()):
                            if key.startswith('show_invoice_'):
                                del st.session_state[key]
                        # Establecer solo la factura actual como visible    
                        st.session_state[invoice_key] = True
                        st.rerun()
            
                # Mostrar detalles si la factura está marcada para visualización
                if st.session_state.get(invoice_key, False):
                    with st.expander(f"📄 Detalles de {row.get('numero', 'Factura')}", expanded=True):
                        show_invoice_details(row)
                        
                        if st.button("Cerrar detalles", key=f"close_{row.get('numero', '')}_{idx}"):
                            del st.session_state[invoice_key]
                            st.rerun()

    else:
        st.info("No hay facturas para mostrar.")

def show_products_page():
    st.subheader("📦 Gestión de Productos")
    st.markdown("---")

    with st.form("product_form", clear_on_submit=True):
        st.write("Añadir/Editar Producto")
        product_id = st.number_input("ID del Producto (dejar 0 para nuevo)", min_value=0, value=0, format="%d")
        product_code = st.text_input("Código")
        product_name = st.text_input("Nombre")
        product_price = st.number_input("Precio", min_value=0.0, format="%.2f")
        product_stock = st.number_input("Stock", min_value=0, format="%d")
        product_iva_applicable = st.checkbox("IVA Aplicable", value=True)

        submitted = st.form_submit_button("Guardar Producto")
        if submitted:
            if not product_code or not product_name:
                st.error("Código y Nombre del producto son obligatorios.")
            else:
                new_product = Producto(
                    id=product_id if product_id > 0 else data_manager.get_next_product_id(),
                    codigo=product_code,
                    nombre=product_name,
                    precio=product_price,
                    stock=product_stock,
                    iva_aplicable=product_iva_applicable
                )
                success, message = data_manager.add_or_update_product(new_product)
                if success:
                    st.success(message)
                    st.session_state.all_products = data_manager.get_all_products() 
                else:
                    st.error(message)

    st.markdown("---")
    st.subheader("Listado de Productos")
    if st.session_state.all_products:
        products_df = pd.DataFrame([p.to_dict() for p in st.session_state.all_products])
        st.dataframe(products_df, use_container_width=True)
        st.markdown(get_table_download_link(products_df, "productos.csv", "Descargar Productos CSV"), unsafe_allow_html=True)
    else:
        st.info("No hay productos registrados.")
     
    st.markdown("---")
    st.subheader("Eliminar Producto")
    product_to_delete_name = st.selectbox(
        "Seleccione Producto a Eliminar",
        options=[""] + [p.nombre for p in st.session_state.all_products],
        key="delete_product_select"
    )
    if st.button("Eliminar Producto Seleccionado", key="delete_product_button"):
        if product_to_delete_name:
            product_to_delete = next((p for p in st.session_state.all_products if p.nombre == product_to_delete_name), None)
            if product_to_delete:
                success, message = data_manager.delete_product(product_to_delete.id)
                if success:
                    st.success(message)
                    st.session_state.all_products = data_manager.get_all_products() 
                else:
                    st.error(message)
            else:
                st.warning("Producto no encontrado.")
        else:
            st.warning("Por favor, seleccione un producto para eliminar.")


def show_clients_page():
    st.subheader("👥 Gestión de Clientes")
    st.markdown("---")

    
    with st.form("client_form", clear_on_submit=True):
        st.write("Añadir/Editar Cliente")
        client_id = st.number_input("ID del Cliente (dejar 0 para nuevo)", min_value=0, value=0, format="%d")
        client_document = st.text_input("Documento")
        client_name = st.text_input("Nombre")
        client_phone = st.text_input("Teléfono")
        client_email = st.text_input("Email")
        client_address = st.text_area("Dirección")

        submitted = st.form_submit_button("Guardar Cliente")
        if submitted:
            if not client_document or not client_name:
                st.error("Documento y Nombre del cliente son obligatorios.")
            else:
                new_client = Cliente(
                    id=client_id if client_id > 0 else data_manager.get_next_client_id(),
                    documento=client_document,
                    nombre=client_name,
                    telefono=client_phone,
                    email=client_email,
                    direccion=client_address
                )
                success, message = data_manager.add_or_update_client(new_client)
                if success:
                    st.success(message)
                    st.session_state.all_clients = data_manager.get_all_clients() 
                else:
                    st.error(message)

    st.markdown("---")
    st.subheader("Listado de Clientes")
    if st.session_state.all_clients:
        clients_df = pd.DataFrame([c.to_dict() for c in st.session_state.all_clients])
        st.dataframe(clients_df, use_container_width=True)
        st.markdown(get_table_download_link(clients_df, "clientes.csv", "Descargar Clientes CSV"), unsafe_allow_html=True)
    else:
        st.info("No hay clientes registrados.")
    st.markdown("---")
    st.subheader("Eliminar Cliente")
    client_to_delete_name = st.selectbox(
        "Seleccione Cliente a Eliminar",
        options=[""] + [f"{c.nombre} ({c.documento})" for c in st.session_state.all_clients],
        key="delete_client_select"
    )
    if st.button("Eliminar Cliente Seleccionado", key="delete_client_button"):
        if client_to_delete_name:
            client_doc_to_delete = client_to_delete_name.split('(')[1][:-1] 
            client_to_delete = next((c for c in st.session_state.all_clients if c.documento == client_doc_to_delete), None)
            if client_to_delete:
                success, message = data_manager.delete_client(client_to_delete.id)
                if success:
                    st.success(message)
                    st.session_state.all_clients = data_manager.get_all_clients() 
                else:
                    st.error(message)
            else:
                st.warning("Cliente no encontrado.")
        else:
            st.warning("Por favor, seleccione un cliente para eliminar.")


def show_services_page():
    st.subheader("📊 Gestión de Servicios")
    st.markdown("---")

    with st.form("service_form", clear_on_submit=True):
        st.write("Añadir/Editar Servicio")
        service_id = st.number_input("ID del Servicio (dejar 0 para nuevo)", min_value=0, value=0, format="%d")
        service_code = st.text_input("Código")
        service_name = st.text_input("Nombre")
        service_price = st.number_input("Precio", min_value=0.0, format="%.2f")
        service_temporal = st.checkbox("Servicio Temporal", value=False)

        submitted = st.form_submit_button("Guardar Servicio")
        if submitted:
            if not service_code or not service_name:
                st.error("Código y Nombre del servicio son obligatorios.")
            else:
                new_service = Servicio(
                    id=service_id if service_id > 0 else data_manager.get_next_service_id(),
                    codigo=service_code,
                    nombre=service_name,
                    precio=service_price,
                    temporal=service_temporal
                )
                success, message = data_manager.add_or_update_service(new_service)
                if success:
                    st.success(message)
                    st.session_state.all_services = data_manager.get_all_services() 
                else:
                    st.error(message)

    st.markdown("---")
    st.subheader("Listado de Servicios")
    if st.session_state.all_services:
        services_df = pd.DataFrame([s.to_dict() for s in st.session_state.all_services])
        st.dataframe(services_df, use_container_width=True)
        st.markdown(get_table_download_link(services_df, "servicios.csv", "Descargar Servicios CSV"), unsafe_allow_html=True)
    else:
        st.info("No hay servicios registrados.")
    st.markdown("---")
    st.subheader("Eliminar Servicio")
    service_to_delete_name = st.selectbox(
        "Seleccione Servicio a Eliminar",
        options=[""] + [s.nombre for s in st.session_state.all_services],
        key="delete_service_select"
    )
    if st.button("Eliminar Servicio Seleccionado", key="delete_service_button"):
        if service_to_delete_name:
            service_to_delete = next((s for s in st.session_state.all_services if s.nombre == service_to_delete_name), None)
            if service_to_delete:
                success, message = data_manager.delete_service(service_to_delete.id)
                if success:
                    st.success(message)
                    st.session_state.all_services = data_manager.get_all_services() 
                else:
                    st.error(message)
            else:
                st.warning("Servicio no encontrado.")
        else:
            st.warning("Por favor, seleccione un servicio para eliminar.")


def show_configuration_page():
    st.subheader("⚙️ Configuración del Sistema")
    st.write("Aquí puedes establecer configuraciones generales, como prefijos de factura, etc.")
    if "invoice_prefix_config" not in st.session_state:
        st.session_state.invoice_prefix_config = _invoice_prefix
    if "invoice_suffix_config" not in st.session_state:
        st.session_state.invoice_suffix_config = _invoice_suffix

    new_prefix = st.text_input("Prefijo de Factura",
                                value=st.session_state.invoice_prefix_config,
                                key="invoice_prefix_config_input")
    new_suffix = st.text_input("Sufijo de Factura",
                                value=st.session_state.invoice_suffix_config,
                                key="invoice_suffix_config_input")
    
    if st.button("Guardar Configuración de Factura"):
        set_invoice_number_config(new_prefix, new_suffix)
        st.session_state.invoice_prefix_config = new_prefix
        st.session_state.invoice_suffix_config = new_suffix
        st.success("Configuración de prefijo/sufijo guardada correctamente.")
        st.rerun() 

def show_pending_module_page(module_name):
    """Displays a message for modules pending implementation."""
    st.subheader(f"{module_name}")
    st.markdown("---")
    st.info("🚧 Módulo pendiente por implementar")
    st.write("Este módulo estará disponible en una próxima versión.")
    
def main(selected_option):
    if 'all_products' not in st.session_state:
        st.session_state.all_products = data_manager.get_all_products()
    if 'all_services' not in st.session_state:
        st.session_state.all_services = data_manager.get_all_services()
    if 'all_clients' not in st.session_state:
        st.session_state.all_clients = data_manager.get_all_clients()

    
    st.title("LUXBEAUTY LAB - Sistema de Facturación")
    logo_path = Path("assets/logo_prepared.png") 
    if not logo_path.exists():   
        logo_path = Path("assets/logo.jpg") if Path("assets/logo.jpg").exists() else None
    if selected_option == "🏠 Inicio":
        st.subheader("Bienvenido al Sistema de Facturación LUXBEAUTY LAB")
        st.write("Utiliza el menú lateral para navegar por las diferentes secciones de la aplicación.")
        st.info("Asegúrate de haber colocado tu logo en la carpeta 'assets' para que aparezca en las facturas.")
    elif selected_option == "🧾 Facturación":
        show_billing_module_page(str(logo_path) if logo_path else None, selected_option)
    elif selected_option == "📦 Gestión de Productos":
        show_products_page()
    elif selected_option == "👥 Gestión de Clientes":
        show_clients_page()
    elif selected_option == "📊 Gestión de Servicios":
        show_services_page()
    elif selected_option == "🗳 Gestion de Inventario":
        show_pending_module_page("🗳 Gestion de Inventario")
    elif selected_option == "📊 Reportes":
        show_pending_module_page("📊 Reportes")
    elif selected_option == "📠 Cuandre de Caja":
        show_pending_module_page("📠 Cuandre de Caja")
    elif selected_option == "🙏 Solicitar Soporte":
        show_pending_module_page("🙏 Solicitar Soporte")
    elif selected_option == "🗝 Seguridad y Accesos":
        show_pending_module_page("🗝 Seguridad y Accesos")
    elif selected_option == "⚙️ Configuración":
        show_configuration_page()
    elif selected_option == "⚙️ Configuración": 
        show_configuration_page()
    
        
    with st.sidebar:
        # Información de la aplicación
        st.caption("💄 LUXBEAUTY LAB")
        st.caption("🏢 Sistema de Facturación")
        st.caption("📋 Versión 1.0")
        st.caption("© copyright")

if __name__ == "__main__":
    
    menu_options = [
        "🏠 Inicio",
        "👥 Gestión de Clientes",
        "📊 Gestión de Servicios",
        "🗳 Gestion de Inventario",
        "📊 Reportes",
        "🧾 Facturación",
        "📠 Cuandre de Caja",
        "🙏 Solicitar Soporte",
        "🗝 Seguridad y Accesos",
        "📦 Gestión de Productos",
        "⚙️ Configuración"
    ]

    logo_for_pdf_path = setup_assets()
    selected_option = setup_sidebar_navigation(menu_options)
    main(selected_option)
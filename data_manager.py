import streamlit as st
import pandas as pd
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime
import json
import numpy as np 

from models import Cliente, Producto, Factura, MedioPago, Servicio, ItemFactura

class DataManager:
    def __init__(self):
        self.data_path = Path("data")
        self.invoices_dir = self.data_path / "invoices"
        self.clients_file = self.data_path / "clients.csv"
        self.products_file = self.data_path / "products.csv"
        self.services_file = self.data_path / "services.csv"
        self.invoices_registro_file = self.invoices_dir / "invoices_registro.csv"

        self._ensure_files_exist()

    def _ensure_files_exist(self):
        self.data_path.mkdir(parents=True, exist_ok=True)
        self.invoices_dir.mkdir(parents=True, exist_ok=True)

        if not self.clients_file.exists():
            pd.DataFrame(columns=['id', 'documento', 'nombre', 'telefono', 'email', 'direccion']).to_csv(self.clients_file, index=False)

        if not self.products_file.exists():
            pd.DataFrame(columns=['id', 'codigo', 'nombre', 'precio', 'stock', 'iva_aplicable']).to_csv(self.products_file, index=False)
        
        if not self.services_file.exists():
            pd.DataFrame(columns=['id', 'codigo', 'nombre', 'precio', 'temporal']).to_csv(self.services_file, index=False)

        if not self.invoices_registro_file.exists():
            
            pd.DataFrame(columns=[
                'numero', 'fecha', 'cliente_id', 'medio_pago', 'subtotal_factura', 
                'descuento_total_factura', 'iva_total_factura', 'total_factura', 
                'observaciones', 'items_json' 
            ]).to_csv(self.invoices_registro_file, index=False)

    
    def get_all_clients(self) -> List[Cliente]:
        if not self.clients_file.exists() or self.clients_file.stat().st_size == 0:
            return []
        try:
            df = pd.read_csv(self.clients_file)
            return [Cliente(**row) for row in df.to_dict(orient='records')]
        except Exception as e:
            st.error(f"Error al cargar clientes: {e}")
            return []

    def get_next_client_id(self) -> int:
        clients = self.get_all_clients()
        if not clients:
            return 1
        return max(c.id for c in clients) + 1

    def add_or_update_client(self, client: Cliente) -> tuple[bool, str]:
        clients = self.get_all_clients()
        
        existing_client_index = -1
        for i, c in enumerate(clients):
            if c.id == client.id:
                existing_client_index = i
                break
        
        if existing_client_index != -1:
            
            clients[existing_client_index] = client
            message = f"Cliente '{client.nombre}' actualizado correctamente."
        else:
            
            clients.append(client)
            message = f"Cliente '{client.nombre}' añadido correctamente."
        
        try:
            df = pd.DataFrame([c.to_dict() for c in clients])
            df.to_csv(self.clients_file, index=False)
            return True, message
        except Exception as e:
            return False, f"Error al guardar cliente: {e}"

    def delete_client(self, client_id: int) -> tuple[bool, str]:
        clients = self.get_all_clients()
        initial_len = len(clients)
        clients = [c for c in clients if c.id != client_id]
        
        if len(clients) == initial_len:
            return False, "Cliente no encontrado."
        
        try:
            df = pd.DataFrame([c.to_dict() for c in clients])
            df.to_csv(self.clients_file, index=False)
            return True, "Cliente eliminado correctamente."
        except Exception as e:
            return False, f"Error al eliminar cliente: {e}"

    
    def get_all_products(self) -> List[Producto]:
        if not self.products_file.exists() or self.products_file.stat().st_size == 0:
            return []
        try:
            df = pd.read_csv(self.products_file)
            
            df['iva_aplicable'] = df['iva_aplicable'].apply(lambda x: bool(x) if pd.notna(x) else False)
            return [Producto(**row) for row in df.to_dict(orient='records')]
        except Exception as e:
            st.error(f"Error al cargar productos: {e}")
            return []

    def get_next_product_id(self) -> int:
        products = self.get_all_products()
        if not products:
            return 1
        return max(p.id for p in products) + 1

    def add_or_update_product(self, product: Producto) -> tuple[bool, str]:
        products = self.get_all_products()
        existing_product_index = -1
        for i, p in enumerate(products):
            if p.id == product.id:
                existing_product_index = i
                break
        
        if existing_product_index != -1:
            products[existing_product_index] = product
            message = f"Producto '{product.nombre}' actualizado correctamente."
        else:
            products.append(product)
            message = f"Producto '{product.nombre}' añadido correctamente."
        
        try:
            df = pd.DataFrame([p.to_dict() for p in products])
            df.to_csv(self.products_file, index=False)
            return True, message
        except Exception as e:
            return False, f"Error al guardar producto: {e}"

    def delete_product(self, product_id: int) -> tuple[bool, str]:
        products = self.get_all_products()
        initial_len = len(products)
        products = [p for p in products if p.id != product_id]
        
        if len(products) == initial_len:
            return False, "Producto no encontrado."
        
        try:
            df = pd.DataFrame([p.to_dict() for p in products])
            df.to_csv(self.products_file, index=False)
            return True, "Producto eliminado correctamente."
        except Exception as e:
            return False, f"Error al eliminar producto: {e}"

    def get_all_services(self) -> List[Servicio]:
        """Loads all services from the services.csv file."""
        if not self.services_file.exists() or self.services_file.stat().st_size == 0:
            return []
        try:
            df = pd.read_csv(self.services_file)
            
            df['temporal'] = df['temporal'].apply(lambda x: bool(x) if pd.notna(x) else False)
            return [Servicio(**row) for row in df.to_dict(orient='records')]
        except Exception as e:
            st.error(f"Error al cargar servicios: {e}")
            return []

    def get_next_service_id(self) -> int:
        services = self.get_all_services()
        if not services:
            return 1
        return max(s.id for s in services) + 1

    def add_or_update_service(self, service: Servicio) -> tuple[bool, str]:
        services = self.get_all_services()
        existing_service_index = -1
        for i, s in enumerate(services):
            if s.id == service.id:
                existing_service_index = i
                break
        
        if existing_service_index != -1:
            services[existing_service_index] = service
            message = f"Servicio '{service.nombre}' actualizado correctamente."
        else:
            services.append(service)
            message = f"Servicio '{service.nombre}' añadido correctamente."
        
        try:
            df = pd.DataFrame([s.to_dict() for s in services])
            df.to_csv(self.services_file, index=False)
            return True, message
        except Exception as e:
            return False, f"Error al guardar servicio: {e}"
        
    def _get_medio_pago_name(self, medio_pago) -> str:
        if medio_pago is None:
            return "No especificado"
        
        if hasattr(medio_pago, 'value'):
            return medio_pago.value
        
        if isinstance(medio_pago, str):
            return medio_pago
        
        return str(medio_pago)

    def delete_service(self, service_id: int) -> tuple[bool, str]:
        services = self.get_all_services()
        initial_len = len(services)
        services = [s for s in services if s.id != service_id]
        
        if len(services) == initial_len:
            return False, "Servicio no encontrado."
        try:
            df = pd.DataFrame([s.to_dict() for s in services])
            df.to_csv(self.services_file, index=False)
            return True, "Servicio eliminado correctamente."
        except Exception as e:
            return False, f"Error al eliminar servicio: {e}"
        
    def save_invoice_registro(self, factura: Factura) -> tuple[bool, str]:
        try:
            invoice_data = {
                'numero': factura.numero,
                'fecha': factura.fecha.isoformat() if isinstance(factura.fecha, datetime) else str(factura.fecha),
                'cliente_id': factura.cliente.id,  
                'medio_pago': factura.medio_pago.value if factura.medio_pago else "No especificado",
                'subtotal_factura': factura.subtotal,
                'descuento_total_factura': factura.descuento_total,
                'iva_total_factura': factura.iva_total,
                'total_factura': factura.total,
                'observaciones': factura.observaciones if factura.observaciones else "",
                'items_json': json.dumps([item.to_dict() for item in factura.items], ensure_ascii=False)
                }
            
            invoice_data_df = pd.DataFrame([invoice_data])
            header = not self.invoices_registro_file.exists() or self.invoices_registro_file.stat().st_size == 0
            invoice_data_df.to_csv(
                self.invoices_registro_file, 
                mode='a', 
                header=header, 
                index=False, 
                encoding='utf-8',
                escapechar='\\',  
                quotechar='"'     
                )
            return True, "Factura guardada correctamente."
        except Exception as e:
            st.error(f"Error al guardar la factura: {e}")
            return False, f"Error al guardar la factura: {e}"

    def _safe_json_loads(self, json_str):
        if pd.isna(json_str) or json_str == '' or json_str is None:
            return []
        
        if isinstance(json_str, str):
            json_str = json_str.strip()
            if not json_str:
                return []
            
            if not (json_str.startswith('[') or json_str.startswith('{')):
                st.warning(f"Valor no parece ser JSON válido: {json_str[:50]}...")
                return []
            
            try:
                return json.loads(json_str)
            except json.JSONDecodeError as e:
                st.warning(f"Error al parsear JSON: {json_str[:100]}... Error: {e}")
                return []
        
        
        if isinstance(json_str, (list, dict)):
            return json_str
            
        return []
    
    def _enrich_invoices_with_client_data(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty or 'cliente_id' not in df.columns:
            df['cliente_nombre'] = ""
            df['cliente_documento'] = ""
            df['cliente_telefono'] = ""
            df['cliente_email'] = ""
            return df
    
        
        clients = self.get_all_clients()
        clients_dict = {client.id: client for client in clients}
        df['cliente_nombre'] = df['cliente_id'].apply(
            lambda client_id: clients_dict.get(client_id).nombre if client_id in clients_dict else "Cliente no encontrado"
        )
        df['cliente_documento'] = df['cliente_id'].apply(
            lambda client_id: clients_dict.get(client_id).documento if client_id in clients_dict else ""
        )
        df['cliente_telefono'] = df['cliente_id'].apply(
            lambda client_id: clients_dict.get(client_id).telefono if client_id in clients_dict else ""
        )
        df['cliente_email'] = df['cliente_id'].apply(
            lambda client_id: clients_dict.get(client_id).email if client_id in clients_dict else ""
        )
        if 'total_factura' in df.columns and 'total' not in df.columns:
            df['total'] = df['total_factura']
        
        return df
        
    def get_all_invoices_registro(self) -> pd.DataFrame:        
        if not self.invoices_registro_file.exists() or self.invoices_registro_file.stat().st_size == 0:
            return pd.DataFrame(columns=[
                'numero', 'fecha', 'cliente_id', 'medio_pago', 'subtotal_factura', 
                'descuento_total_factura', 'iva_total_factura', 'total_factura', 
                'observaciones', 'items_json'
                ])
    
        try:
            df = pd.read_csv(
                self.invoices_registro_file, 
                encoding='utf-8',
                dtype=str,  
                na_values=['', 'nan', 'NaN', 'null', 'NULL'],  
                keep_default_na=True
            )
            
            if df.empty:
                return pd.DataFrame(columns=[
                    'numero', 'fecha', 'cliente_id', 'medio_pago', 'subtotal_factura', 
                    'descuento_total_factura', 'iva_total_factura', 'total_factura', 
                    'observaciones', 'items_json'
                ])
            
            expected_columns = [
                'numero', 'fecha', 'cliente_id', 'medio_pago', 'subtotal_factura', 
                'descuento_total_factura', 'iva_total_factura', 'total_factura', 
                'observaciones', 'items_json'
            ]
            
            if list(df.columns) == expected_columns:
                
                if 'items_json' in df.columns:
                    df['items_json'] = df['items_json'].apply(self._safe_json_loads)
                else:
                    df['items_json'] = [[] for _ in range(len(df))]
            
                numeric_columns = ['cliente_id', 'subtotal_factura', 'descuento_total_factura', 
                                'iva_total_factura', 'total_factura']
                
                for col in numeric_columns:
                    if col in df.columns:
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                
                if 'fecha' in df.columns:
                    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce', format='mixed')
                
                df = self._enrich_invoices_with_client_data(df)
                
                return df
            
            else:
                st.warning("Detectando problema en el formato del CSV. Intentando corregir...")              
                corrected_data = []
                for _, row in df.iterrows():
                    try:
                        row_values = row.values.tolist()
                        if len(row_values) >= 10:
                            corrected_row = {
                                'numero': row_values[0],  
                                'fecha': row_values[1],   
                                'cliente_id': 3,  
                                'medio_pago': "Tarjeta de Débito",  
                                'subtotal_factura': float(row_values[4]) if row_values[4] else 0.0,
                                'descuento_total_factura': float(row_values[5]) if row_values[5] else 0.0,
                                'iva_total_factura': float(row_values[6]) if row_values[6] else 0.0,
                                'total_factura': float(row_values[7]) if row_values[7] else 0.0,
                                'observaciones': row_values[8] if row_values[8] else "",
                                'items_json': self._safe_json_loads(row_values[2]) if len(row_values) > 2 else []
                            }
                            corrected_data.append(corrected_row)
                    except Exception as e:
                        st.warning(f"Error procesando fila: {e}")
                        continue
                
                if corrected_data:
                    corrected_df = pd.DataFrame(corrected_data)
                    numeric_columns = ['cliente_id', 'subtotal_factura', 'descuento_total_factura', 
                                    'iva_total_factura', 'total_factura']
                    
                    for col in numeric_columns:
                        if col in corrected_df.columns:
                            corrected_df[col] = pd.to_numeric(corrected_df[col], errors='coerce')
                    if 'fecha' in corrected_df.columns:
                        corrected_df['fecha'] = pd.to_datetime(corrected_df['fecha'], errors='coerce', format='mixed')
                    corrected_df = self._enrich_invoices_with_client_data(corrected_df)
                    
                    return corrected_df
                else:
                    return pd.DataFrame(columns=expected_columns)
        
        except Exception as e:
            st.error(f"Error al cargar el registro de facturas: {e}")
            
            return pd.DataFrame(columns=[
                'numero', 'fecha', 'cliente_id', 'medio_pago', 'subtotal_factura', 
                'descuento_total_factura', 'iva_total_factura', 'total_factura', 
                'observaciones', 'items_json'
            ])
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
import json

class MedioPago(Enum):
    EFECTIVO = "Efectivo"
    TRANSFERENCIA = "Transferencia Electrónica"
    TARJETA_CREDITO = "Tarjeta de Crédito"
    TARJETA_DEBITO = "Tarjeta de Débito"

@dataclass
class Cliente:
    id: int
    documento: str
    nombre: str
    telefono: str
    email: str
    direccion: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'documento': self.documento,
            'nombre': self.nombre,
            'telefono': self.telefono,
            'email': self.email,
            'direccion': self.direccion
        }

@dataclass
class Producto:
    id: int
    codigo: str
    nombre: str
    precio: float
    stock: int
    iva_aplicable: bool = True 
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'codigo': self.codigo,
            'nombre': self.nombre,
            'precio': self.precio,
            'stock': self.stock,
            'iva_aplicable': self.iva_aplicable
        }

@dataclass
class Servicio:
    id: int
    codigo: str
    nombre: str
    precio: float
    temporal: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'codigo': self.codigo,
            'nombre': self.nombre,
            'precio': self.precio,
            'temporal': self.temporal
        }

@dataclass
class ItemFactura:
    producto: Optional[Producto] 
    servicio: Optional[Servicio]
    cantidad: int = 1
    precio_unitario: float = 0.0
    descuento: float = 0.0 
    iva: float = 0.0   
    
    def subtotal_base(self) -> float:
        base = self.cantidad * self.precio_unitario
        return round(base, 2)
    
    def descuento_pesos(self) -> float:
        base_original = self.cantidad * self.precio_unitario
        descuento = base_original * (self.descuento / 100) 
        return round(descuento, 2)
    
    def iva_pesos(self):
        base_original = self.cantidad * self.precio_unitario
        iva = base_original * (self.iva / 100)
        return round(iva, 2)
        
    def subtotal(self):
        base_original = self.cantidad * self.precio_unitario
        subtotal = base_original * (1 + self.iva / 100) 
        return round(subtotal, 2)
    
    def total(self) -> float:
        base_original = self.cantidad * self.precio_unitario
        descuento_original = base_original * (self.descuento / 100)
        subtotal_con_descuento = base_original - descuento_original
        iva_original = subtotal_con_descuento * (self.iva / 100)
        total = subtotal_con_descuento + iva_original
        return round(total, 2)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'producto_id': self.producto.id if self.producto else None,
            'producto_nombre': self.producto.nombre if self.producto else None,
            'servicio_id': self.servicio.id if self.servicio else None,
            'servicio_nombre': self.servicio.nombre if self.servicio else None,
            'cantidad': self.cantidad,
            'precio_unitario': self.precio_unitario,
            'descuento': self.descuento,
            'iva': self.iva,
            'subtotal_base': self.subtotal_base(),
            'descuento_pesos': self.descuento_pesos(),
            'subtotal': self.subtotal(),
            'iva_pesos': self.iva_pesos(),
            'total': self.total()
        }

@dataclass
class Factura:
    numero: str
    fecha: datetime
    cliente: Cliente
    items: List
    medio_pago: MedioPago
    subtotal: float       
    descuento_total: float 
    iva_total: float     
    total: float          
    observaciones: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'numero': self.numero,
            'fecha': self.fecha.isoformat(),
            'cliente_id': self.cliente.id,
            'cliente_documento': self.cliente.documento,  
            'cliente_nombre': self.cliente.nombre,        
            'items_json': json.dumps([item.to_dict() for item in self.items]), 
            'medio_pago': self.medio_pago.value,
            'subtotal': self.subtotal,                    
            'descuento_total': self.descuento_total,      
            'iva_total': self.iva_total,                  
            'total': self.total,                          
            'observaciones': self.observaciones
        }
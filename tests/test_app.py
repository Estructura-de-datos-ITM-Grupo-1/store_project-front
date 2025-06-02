import unittest
from unittest.mock import Mock, patch
from datetime import datetime
from models import Cliente, Producto, ItemFactura, Factura, MedioPago
from data_manager import DataManager

class TestLuxBeautyLab(unittest.TestCase):
    def setUp(self):
        self.data_manager = DataManager()
        self.cliente_prueba = Cliente(
            documento="123456789",
            nombre="Cliente Test",
            telefono="3001234567",
            email="test@test.com"
        )
        
        self.producto_prueba = Producto(
            codigo="P001",
            nombre="Producto Test",
            precio=10000,
            stock=10,
            iva_aplicable=True
        )
    
    def test_crear_factura(self):
        # Crear item de factura
        item = ItemFactura(
            producto=self.producto_prueba,
            cantidad=2,
            precio_unitario=10000,
            iva=19
        )
        
        # Crear factura
        factura = Factura(
            numero="F001",
            fecha=datetime.now(),
            cliente=self.cliente_prueba,
            items=[item],
            medio_pago=MedioPago.EFECTIVO,
            observaciones="Factura de prueba"
        )
        
        # Calcular totales
        factura.calcular_totales()
        
        # Verificar cálculos
        self.assertEqual(factura.subtotal, 20000)  # 10000 * 2
        self.assertEqual(factura.iva_total, 3800)  # 20000 * 0.19
        self.assertEqual(factura.total, 23800)     # 20000 + 3800

if __name__ == '__main__':
    unittest.main()
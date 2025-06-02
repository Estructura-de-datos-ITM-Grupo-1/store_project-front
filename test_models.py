import unittest
from datetime import datetime
from models import MedioPago, Cliente, Producto, Servicio, ItemFactura, Factura
from utils import calculate_invoice_totals

class TestModels(unittest.TestCase):
    def setUp(self):
        # Crear datos de prueba
        self.cliente = Cliente(
            id=1,
            documento="123456789",
            nombre="Cliente Prueba",
            telefono="3001234567",
            email="test@test.com",
            direccion="Calle Test #123"
        )

        self.producto = Producto(
            id=1,
            codigo="P001",
            nombre="Producto Prueba",
            precio=50000.0,
            stock=10,
            iva_aplicable=True
        )

        self.servicio = Servicio(
            id=1,
            codigo="S001",
            nombre="Servicio Prueba",
            precio=100000.0,
            temporal=False
        )

    def test_medio_pago(self):
        """Prueba la enumeración MedioPago"""
        self.assertEqual(MedioPago.EFECTIVO.value, "Efectivo")
        self.assertEqual(MedioPago.TRANSFERENCIA.value, "Transferencia Electrónica")
        self.assertEqual(MedioPago.TARJETA.value, "Tarjeta")

    def test_item_factura_producto(self):
        """Prueba cálculos de ItemFactura con producto"""
        item = ItemFactura(producto=self.producto, cantidad=2, 
                         precio_unitario=50000.0, descuento=10, iva=19)
        self.assertIsNotNone(item.producto)
        self.assertIsNone(item.servicio)
        self.assertEqual(item.cantidad, 2)
        self.assertEqual(item.precio_unitario, 50000.0)
        self.assertEqual(item.descuento, 10)
        self.assertEqual(item.iva, 19)
        self.assertAlmostEqual(item.subtotal(), 90000.0) # (50000 * 2) - 10%
        self.assertAlmostEqual(item.total(), 107100.0) # 90000 + 19% IVA

    def test_item_factura_servicio(self):
        """Prueba cálculos de ItemFactura con servicio"""
        item = ItemFactura(servicio=self.servicio, cantidad=1, 
                         precio_unitario=100000.0, iva=19)
        self.assertIsNone(item.producto)
        self.assertIsNotNone(item.servicio)
        self.assertEqual(item.cantidad, 1)
        self.assertEqual(item.precio_unitario, 100000.0)
        self.assertEqual(item.descuento, 0)
        self.assertEqual(item.iva, 19)
        self.assertAlmostEqual(item.subtotal(), 100000.0)
        self.assertAlmostEqual(item.total(), 119000.0) # 100000 + 19% IVA
        
    def test_factura_totals_calculation(self):
        """Prueba el cálculo de los totales de la Factura"""
        item1 = ItemFactura(producto=self.producto, cantidad=2, 
                          precio_unitario=50000.0, iva=19)
        item2 = ItemFactura(servicio=self.servicio, cantidad=1, 
                          precio_unitario=100000.0, iva=19)
        
        factura = Factura(
            numero="F001",
            fecha=datetime.now(),
            cliente=self.cliente,
            items=[item1, item2],
            medio_pago=MedioPago.EFECTIVO,
            observaciones="Factura de prueba"
        )
        
        # Call the function from utils.py and assign results
        totals = calculate_invoice_totals(factura.items, descuento_porcentaje=0.0, iva_activado=True)
        factura.subtotal = totals['subtotal_base'] # Adjust if calculate_invoice_totals returns 'subtotal_base'
        factura.descuento_total = totals['descuento_total']
        factura.iva_total = totals['iva_total']
        factura.total = totals['total_factura']
        
        # Prueba totales
        self.assertEqual(factura.subtotal, 200000.0)  # (50000 * 2) + 100000
        self.assertEqual(factura.iva_total, 38000.0)  # 19% de 200000
        self.assertEqual(factura.total, 238000.0)  # 200000 + 38000
        
    def test_factura_to_dict(self):
        """Prueba la conversión de Factura a diccionario"""
        item = ItemFactura(producto=self.producto, cantidad=1, 
                         precio_unitario=50000.0, iva=19)
        
        factura = Factura(
            numero="F001",
            fecha=datetime.now(),
            cliente=self.cliente,
            items=[item],
            medio_pago=MedioPago.EFECTIVO,
            subtotal=50000.0, # Manually set for the test or calculate as shown above
            descuento_total=0.0,
            iva_total=9500.0,
            total=59500.0
        )
        
        factura_dict = factura.to_dict()
        self.assertEqual(factura_dict['numero'], "F001")
        self.assertEqual(factura_dict['cliente_id'], self.cliente.id)
        self.assertEqual(factura_dict['medio_pago'], MedioPago.EFECTIVO.value)
        self.assertEqual(factura_dict['total_factura'], 59500.0)

if __name__ == '__main__':
    unittest.main()
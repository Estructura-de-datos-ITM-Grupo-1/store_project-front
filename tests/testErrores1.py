import unittest
from models import MedioPago

class TestMedioPago(unittest.TestCase):
    def test_medio_pago(self):
        # Probar cada valor del enum
        self.assertEqual(MedioPago.EFECTIVO.value, "Efectivo")
        self.assertEqual(MedioPago.TRANSFERENCIA.value, "Transferencia Electrónica")
        self.assertEqual(MedioPago.TARJETA.value, "Tarjeta")

if __name__ == "__main__":
    unittest.main()
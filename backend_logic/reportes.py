import pandas as pd
from io import BytesIO
import numpy as np
from datetime import datetime, timedelta

def cargar_movimientos_inventario():
    data = {
        'Fecha': pd.to_datetime([
            '2025-05-25', '2025-05-18', '2025-05-25',
            '2024-05-25', '2025-05-25'
        ]),
        'Tipo': ['Entrada', 'Salida', 'Entrada', 'Entrada', 'Salida'],
        'Producto': ['Labial Rojo', 'Base Clara', 'Corrector', 'Rubor Rosa', 'Delineador Negro'],
        'Cantidad': [20, 10, -2, 15, 5],
        'Costo Unitario': [3.5, 7.0, 5.0, 4.5, 2.5],
        'Responsable': ['Ana', 'Luis', 'Ana', 'Carlos', 'Marta'],
        'Observaciones': [
            'Compra a proveedor',
            'Venta en mostrador',
            'Error de conteo',
            'Reabastecimiento',
            'Venta en promoción'
        ]
    }
    return pd.DataFrame(data)

def filtrar_movimientos(df, fecha_inicio, fecha_fin, tipos):
    mask = (
        (df['Fecha'] >= pd.to_datetime(fecha_inicio)) &
        (df['Fecha'] <= pd.to_datetime(fecha_fin)) &
        (df['Tipo'].isin(tipos))
    )
    return df.loc[mask]

def convertir_a_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Movimientos')
    output.seek(0)
    return output.getvalue()


def cargar_servicios():
    data = {
        'Fecha': pd.to_datetime([
            '2025-05-25', '2025-05-18', '2025-05-25',
            '2024-05-25', '2025-05-25'
        ]),
        'Servicio': ['Manicura', 'Maquillaje', 'Peinado', 'Facial', 'Depilación'],
        'Empleado': ['Ana', 'Luis', 'Carlos', 'Ana', 'Marta'],
        'Cliente': ['Cliente1', 'Cliente2', 'Cliente3', 'Cliente1', 'Cliente2'],
        'Precio': [30, 50, 40, 60, 35],
        'MetodoPago': ['Efectivo', 'Tarjeta', 'Efectivo', 'Transferencia', 'Tarjeta'],
        'Observaciones': ['', 'Servicio express', '', 'Con máscara incluida', ''],
    }
    return pd.DataFrame(data)



def cargar_clientes():
    # Datos simulados en un DataFrame
    data = {
        'Fecha': [
            '2025-04-01', '2025-04-05', '2025-04-07', '2025-04-10',
            '2025-04-15', '2025-04-18', '2025-04-20', '2025-04-21',
            '2025-04-25', '2025-04-30'
        ],
        'Cliente': [
            'Ana López', 'Carlos Pérez', 'Ana López', 'María Ruiz',
            'Carlos Pérez', 'Ana López', 'Juan Gómez', 'María Ruiz',
            'Ana López', 'Juan Gómez'
        ],
        'Monto': [
            150, 200, 300, 100,
            250, 120, 180, 220,
            170, 190
        ],
        'Producto': [
            'Labial', 'Sombra de ojos', 'Base de maquillaje', 'Delineador',
            'Polvo compacto', 'Máscara de pestañas', 'Blush', 'Corrector',
            'Labial', 'Sombras'
        ]
    }

    df = pd.DataFrame(data)
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    return df

def generar_datos_financieros(modo="Diario"):
    hoy = datetime.now()

    if modo == "Diario":
        fechas = [hoy - timedelta(days=i) for i in range(30)]
    elif modo == "Semanal":
        fechas = [hoy - timedelta(weeks=i) for i in range(12)]
    elif modo == "Mensual":
        fechas = pd.date_range(end=hoy, periods=12, freq='M')
    elif modo == "Anual":
        fechas = pd.date_range(end=hoy, periods=5, freq='Y')
    else:
        fechas = [hoy]

    ingresos = np.random.randint(500, 2000, len(fechas))
    egresos = np.random.randint(300, 1800, len(fechas))

    df = pd.DataFrame({
        "Fecha": fechas,
        "Ingresos": ingresos,
        "Egresos": egresos
    })

    return df
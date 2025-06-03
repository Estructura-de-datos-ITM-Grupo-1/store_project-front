import pandas as pd
import json
import io

# ===== CARGA DE DATOS =====
def cargar_ventas_diarias():
    """Carga y estructura el resumen diario de ventas con valores editables."""
    data = {
        'Fecha': pd.to_datetime(['2025-06-01'] * 4),
        'Descripción': ['Labial Rojo', 'Base Clara', 'Pestañina', 'Base Mate'],
        'Cantidad': [2, 1, 3, 2],
        'Precio Unitario': [12000, 25000, 35000, 40000],
        'Total': [24000, 25000, 105000, 80000],
        'Método de Pago': ['Efectivo', 'Tarjeta', 'Transferencia electrónica', 'Efectivo'],
        'Cliente': ['Ana', 'Luis', 'Carlos', 'Marta']
    }
    return pd.DataFrame(data)

def cargar_egresos_diarios():
    """Carga y estructura el registro diario de egresos."""
    data = {
        'Fecha': pd.to_datetime(['2025-06-01', '2025-06-01']),
        'Descripción': ['Pago Proveedor A', 'Pago Proveedor B'],
        'Monto': [15000, 20000],
        'Método de Pago': ['Efectivo', 'Transferencia']
    }
    return pd.DataFrame(data)

# ===== CÁLCULOS AUTOMÁTICOS =====
def obtener_total_ingresos():
    """Calcula el total de ingresos por ventas."""
    df_ventas = cargar_ventas_diarias()
    return df_ventas['Total'].sum()

def obtener_total_egresos():
    """Calcula el total de egresos registrados."""
    df_egresos = cargar_egresos_diarios()
    return df_egresos['Monto'].sum()

def obtener_pagos_en_otros_medios():
    """Calcula el monto total de pagos NO realizados en efectivo."""
    df_ventas = cargar_ventas_diarias()
    pagos_otro_medio = df_ventas[df_ventas['Método de Pago'] != "Efectivo"]['Total'].sum()
    return pagos_otro_medio

# ===== MANEJO DE BASE DE CAJA =====
CONFIG_FILE = "config.json"

def obtener_base_caja():
    """Carga la base de caja desde un archivo JSON."""
    try:
        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)
            return config.get("base_caja", 50000)
    except FileNotFoundError:
        config = {"base_caja": 50000}
        with open(CONFIG_FILE, "w") as file:
            json.dump(config, file, indent=4)
        return config["base_caja"]

def actualizar_base_caja(nuevo_valor):
    """Actualiza la base de caja en el archivo JSON."""
    try:
        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)
        
        config["base_caja"] = nuevo_valor

        with open(CONFIG_FILE, "w") as file:
            json.dump(config, file, indent=4)

        print(f"Base de caja actualizada a ${nuevo_valor:.2f}")
    except FileNotFoundError:
        print("Error: Archivo de configuración no encontrado.")

    return obtener_base_caja()

# ===== GENERACIÓN DE REPORTES =====
def convertir_a_excel(df):
    """Convierte un DataFrame en un archivo Excel descargable."""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name="Reporte")
        writer.book.close()
    output.seek(0)
    return output

def obtener_registros_auditoria():
    """Simula la carga de registros de auditoría del sistema."""
    data = {
        'Fecha': pd.to_datetime(['2025-05-30', '2025-06-01']),
        'Usuario': ['Juan Pérez', 'María Gómez'],
        'Total Ingresos': [450000, 620000],
        'Total Egresos': [200000, 250000],
        'Efectivo Declarado': [250000, 370000],
        'Diferencia en Caja': [-5000, 20000],
        'Estado': ['Descuadre', 'Correcto']
    }
    return pd.DataFrame(data)
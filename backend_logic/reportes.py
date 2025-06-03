import pandas as pd
from io import BytesIO
import requests
from datetime import datetime, timedelta

API_URL = "http://localhost:8000/api/v1"

def cargar_clientes():
    response = requests.get(f"{API_URL}/clientes")
    response.raise_for_status()
    data = response.json()
    df = pd.DataFrame(data)
    return df

def guardar_clientes_crud(df):
    data = df.to_dict(orient="records")
    response = requests.post(f"{API_URL}/clientes", json=data)
    response.raise_for_status()
    return df

def cargar_servicios():
    response = requests.get(f"{API_URL}/servicios")
    response.raise_for_status()
    data = response.json()
    df = pd.DataFrame(data)
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    return df

def cargar_movimientos_inventario():
    response = requests.get(f"{API_URL}/inventario/productos")
    response.raise_for_status()
    data = response.json()
    df = pd.DataFrame(data)
    # df['Fecha'] = pd.to_datetime(df['Fecha'])
    return df

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

def generar_datos_financieros(modo="Diario"):
    response = requests.get(f"{API_URL}/finanzas?modo={modo}")
    response.raise_for_status()
    data = response.json()
    df = pd.DataFrame(data)
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    return df

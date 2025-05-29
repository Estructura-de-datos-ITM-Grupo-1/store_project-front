📦 Tienda de Maquillaje — Frontend

🚀 Descripción  
Interfaz web interactiva y personalizable para la gestión de ventas, reportes y cuadre de caja de una tienda de maquillaje.  
Desarrollada con:

- Streamlit (Interfaz web ligera y rápida en Python)
- Plotly (Gráficas interactivas para visualización de datos)
- Python puro (con archivos .py organizados por módulos)
  
🌟 Características Principales

✔️ Visualización de reportes de ventas, inventario y clientes frecuentes  
✔️ Cuadre de caja diario con desglose por métodos de pago  
✔️ Gráficas de desempeño financiero con filtros por fecha  
✔️ Interfaz personalizable (sidebar, colores y estilos CSS)  
✔️ Organización modular por secciones (login, reportes, caja, etc.)  
✔️ Fácil de desplegar con solo ejecutar un script  

🛠️ Tecnologías

Frontend:
- Streamlit
- Plotly
- Python 3.9+

Visualización:
- Plotly (líneas, barras, comparativas)

Estilos:
- HTML y CSS embebido en Streamlit

📂 Estructura del Proyecto

caja_tienda_frontend/
├── app.py # Script principal con configuración global
├── backend_logic.py # Módulo con lógica simulada o real
├── secciones/
│ ├── login.py # Módulo de login (en desarrollo o futuro)
│ ├── reportes.py # Módulo de reportes (ventas, clientes, finanzas)
│ ├── caja.py # Módulo de cuadre de caja
│ └── utils.py # Funciones auxiliares (formateo, colores, etc.)
├── data/ # (opcional) Archivos .json o .csv si se usan 
├── assets/ # Archivos estáticos (imágenes, logo, etc.) 
├── README.md 
└── requirements.txt 


🚀 Primeros Pasos

1. Clonar y preparar entorno
```bash
git clone https://github.com/tu_usuario/caja_tienda_frontend.git
cd caja_tienda_frontend
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
pip install -r requirements.txt

2. Ejecutar app
streamlit run app.py

La app se abrirá en tu navegador en http://localhost:8501

# backend/configuracion_backend.py

# Simulación de base de datos (temporal)
_configuracion_general = {
    "nombre_tienda": "LuxBeauty Lab",
    "telefono": "123456789",
    "direccion": "Calle Belleza 101",
    "leyenda_factura": "Gracias por tu compra. ¡Vuelve pronto!"
}

def obtener_configuracion():
    """Retorna los parámetros generales actuales."""
    return _configuracion_general.copy()

def guardar_configuracion(nombre_tienda, telefono, direccion, leyenda):
    """Guarda los parámetros generales (simulado)."""
    _configuracion_general["nombre_tienda"] = nombre_tienda
    _configuracion_general["telefono"] = telefono
    _configuracion_general["direccion"] = direccion
    _configuracion_general["leyenda_factura"] = leyenda
    return True

#PUNTO DOS
ROLES = {
    "Soporte": {
        "descripcion": "Acceso total y absoluto al sistema. Para mantenimiento, soporte técnico y resolución de problemas.",
        "permisos": [
            "Acceso completo al sistema sin restricciones"
        ]
    },
    "Admin": {
        "descripcion": "Permisos para administrar inventarios, servicios, reportes avanzados, cuadre de caja, facturas y reportes administrativos.",
        "permisos": [
            "Crear y modificar inventarios",
            "Crear y modificar servicios ofrecidos",
            "Generar y revisar reportes avanzados",
            "Cuadre de caja diario",
            "Generar facturas",
            "Acceder a reportes administrativos del sistema"
        ]
    },
    "Caja": {
        "descripcion": "Permisos limitados para crear facturas, realizar cuadre de caja y consultar reportes de ventas y caja.",
        "permisos": [
            "Creación de facturas",
            "Realización del cuadre de caja diario",
            "Consulta de reportes de ventas y caja"
        ]
    }
}

# Función simulada para obtener usuarios (en la práctica vendría de base de datos)
def obtener_usuarios():
    return ["usuario1", "usuario2", "usuario3"]

# Función simulada para guardar asignación de usuarios a roles
def guardar_asignacion_usuarios(rol, lista_usuarios):
    # Aquí implementarías la lógica para guardar en base de datos o archivo
    # Por ahora simulamos con un print o logging
    print(f"Guardando usuarios {lista_usuarios} para el rol {rol}")
    return True
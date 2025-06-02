# backend_logic/configuracion.py
import json
import os

CONFIG_VISUAL_FILE = "config_visual.json"
CONFIG_GENERAL_FILE = "config_general.json"
CONFIG_SISTEMA_FILE = "config_sistema.json"

# --- Configuración visual ---
def cargar_config_visual():
    if os.path.exists(CONFIG_VISUAL_FILE):
        with open(CONFIG_VISUAL_FILE, "r") as f:
            return json.load(f)
    else:
        # Configuración visual por defecto
        return {
            "color_primario": "#C71585",
        }

def guardar_configuracion_visual(color_primario):
    config = {
        "color_primario": color_primario,
    }
    with open(CONFIG_VISUAL_FILE, "w") as f:
        json.dump(config, f, indent=4)
    print("Configuración visual guardada correctamente.")
    return True

def obtener_configuracion():
    # Esta función devuelve la configuración general cargada
    return cargar_config_general()

# --- Configuración general ---
def cargar_config_general():
    if os.path.exists(CONFIG_GENERAL_FILE):
        with open(CONFIG_GENERAL_FILE, "r") as f:
            return json.load(f)
    else:
        return {
            "nombre_tienda": "LuxBeauty Lab",
            "telefono": "3173603298",
            "direccion": "Calle Belleza 101",
            "leyenda_factura": "Gracias por tu compra. ¡Vuelve pronto!"
        }

def guardar_configuracion(nombre_tienda, telefono, direccion, leyenda_factura):
    config = {
        "nombre_tienda": nombre_tienda,
        "telefono": telefono,
        "direccion": direccion,
        "leyenda_factura": leyenda_factura
    }
    with open(CONFIG_GENERAL_FILE, "w") as f:
        json.dump(config, f, indent=4)
    print("Configuración general guardada correctamente.")
    return True

# --- Configuración del sistema ---
def cargar_config_sistema():
    if os.path.exists(CONFIG_SISTEMA_FILE):
        with open(CONFIG_SISTEMA_FILE, "r") as f:
            return json.load(f)
    else:
        return {
            "formato_fecha": "%d/%m/%Y",
            "prefijo_factura": "LUX-",
            "consecutivo_inicial": 1001
        }

def guardar_configuracion_sistema(formato_fecha, prefijo_factura, consecutivo_inicial):
    config = {
        "formato_fecha": formato_fecha,
        "prefijo_factura": prefijo_factura,
        "consecutivo_inicial": consecutivo_inicial
    }
    with open(CONFIG_SISTEMA_FILE, "w") as f:
        json.dump(config, f, indent=4)
    print("Configuración del sistema guardada correctamente.")
    return True


# --- Roles y usuarios ---
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

# Simulación de usuarios (podrías cambiar a base de datos o archivo)
_usuarios = [
    {"nombre": "Usuario1", "correo": "user1@ejemplo.com", "usuario": "usuario1", "activo": True},
    {"nombre": "Usuario2", "correo": "user2@ejemplo.com", "usuario": "usuario2", "activo": False},
    {"nombre": "Usuario3", "correo": None, "usuario": "usuario3", "activo": True},
]

def obtener_usuarios():
    return _usuarios.copy()

def crear_usuario(nombre, correo, usuario, contraseña):
    # Aquí agregarías lógica para guardar el usuario en BD
    # Por ahora simulamos:
    nuevo_usuario = {
        "nombre": nombre,
        "correo": correo,
        "usuario": usuario,
        "activo": True
    }
    _usuarios.append(nuevo_usuario)
    print(f"Usuario {usuario} creado.")
    return True

def cambiar_estado_usuario(index, nuevo_estado):
    if 0 <= index < len(_usuarios):
        _usuarios[index]["activo"] = nuevo_estado
        print(f"Estado de usuario {_usuarios[index]['usuario']} cambiado a {nuevo_estado}")
        return True
    return False

def guardar_asignacion_usuarios(rol, lista_usuarios):
    # Simulación de guardar asignaciones
    print(f"Usuarios asignados al rol {rol}: {lista_usuarios}")
    return True

usuarios = []

def obtener_usuarios():
    return usuarios

def crear_usuario(nombre, correo, usuario, contraseña):
    nuevo = {
        "nombre": nombre,
        "correo": correo,
        "usuario": usuario,
        "contraseña": contraseña,
        "activo": True
    }
    usuarios.append(nuevo)
    return True

def cambiar_estado_usuario(indice, activo):
    if 0 <= indice < len(usuarios):
        usuarios[indice]["activo"] = activo
        return True
    return False

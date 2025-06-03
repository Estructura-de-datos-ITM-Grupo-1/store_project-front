from datetime import datetime, timedelta

productos = []
movimientos = []

UMBRAL_BAJO_STOCK = 5
UMBRAL_ALTA_DEMANDA = 5

MOTIVOS_VALIDOS = ["venta", "devolución", "daño", "pérdida", "reposición"]

def actualizar_producto(referencia, nombre=None, categoria=None, marca=None, color=None, precio=None):
    global productos
    producto = next((p for p in productos if p['referencia'] == referencia), None)
    if producto is None:
        return False, "Producto no encontrado."

    if nombre: producto['nombre'] = nombre
    if categoria: producto['categoria'] = categoria
    if marca: producto['marca'] = marca
    if color: producto['color'] = color
    if precio is not None: producto['precio'] = precio

    return True, "Producto actualizado correctamente."

def crear_producto(nombre, descripcion, categoria, marca, referencia, color, valor_costo, valor_venta, cantidad):
    global productos
    if any(p['referencia'] == referencia for p in productos):
        return False, "La referencia ya existe."

    producto = {
        'nombre': nombre,
        'descripcion': descripcion,
        'categoria': categoria,
        'marca': marca,
        'referencia': referencia,
        'color': color,
        'valor_costo': valor_costo,
        'valor_venta': valor_venta,
        'cantidad': cantidad,
        'fecha_ingreso': datetime.now(),
        'bloqueado': cantidad == 0
    }
    productos.append(producto)
    return True, "Producto creado."

def agregar_producto(nombre, categoria, marca, referencia, color, precio, cantidad):
    return crear_producto(nombre, categoria, marca, referencia, color, precio, cantidad)

def obtener_productos_con_nombre():
    return [(p['referencia'], p['nombre']) for p in productos]

def esta_bloqueado(referencia):
    producto = next((p for p in productos if p['referencia'] == referencia), None)
    if producto:
        return producto.get('bloqueado', False)
    return False

def registrar_movimiento(referencia, tipo, cantidad, motivo):
    global productos, movimientos
    producto = next((p for p in productos if p['referencia'] == referencia), None)
    if producto is None:
        return False, "Producto no encontrado."

    if motivo.lower() not in MOTIVOS_VALIDOS:
        return False, f"Motivo inválido. Debe ser uno de: {', '.join(MOTIVOS_VALIDOS)}"

    if tipo == 'salida':
        if producto.get('bloqueado', False):
            return False, "Producto con stock cero, no se permite venta hasta actualizar stock."
        if producto['cantidad'] < cantidad:
            return False, "Stock insuficiente para salida."
        producto['cantidad'] -= cantidad
        if producto['cantidad'] == 0:
            producto['bloqueado'] = True
    elif tipo == 'entrada':
        producto['cantidad'] += cantidad
        if producto['cantidad'] > 0:
            producto['bloqueado'] = False
    else:
        return False, "Tipo inválido."

    movimientos.append({
        'referencia': referencia,
        'tipo': tipo,
        'cantidad': cantidad,
        'motivo': motivo.lower(),
        'fecha': datetime.now()
    })
    return True, "Movimiento registrado."

def obtener_productos_bajo_stock():
    return [(p['referencia'], p['nombre'], p['cantidad']) for p in productos if p['cantidad'] <= UMBRAL_BAJO_STOCK]

def obtener_productos_alta_demanda():
    fecha_limite = datetime.now() - timedelta(days=7)
    salida_count = {}

    for m in movimientos:
        if m['tipo'] == 'salida' and m['fecha'] >= fecha_limite:
            salida_count[m['referencia']] = salida_count.get(m['referencia'], 0) + 1

    resultado = []
    for ref, count in salida_count.items():
        if count >= UMBRAL_ALTA_DEMANDA:
            prod = next((p for p in productos if p['referencia'] == ref), None)
            if prod:
                resultado.append((prod['referencia'], prod['nombre'], count))

    return resultado

def obtener_historial_movimientos():
    return sorted(movimientos, key=lambda x: x['fecha'], reverse=True)

def agregar_stock(referencia, cantidad_adicional):
    global productos, movimientos

    producto = obtener_producto_por_referencia(referencia)
    if producto is None:
        return False, "Producto no encontrado."

    if cantidad_adicional <= 0:
        return False, "La cantidad a agregar debe ser mayor que cero."

    # Sumar cantidad
    producto['cantidad'] += cantidad_adicional

    # Si el producto estaba bloqueado por stock cero, desbloquearlo
    if producto['bloqueado'] and producto['cantidad'] > 0:
        producto['bloqueado'] = False

    # Registrar movimiento de entrada con motivo 'reposición'
    movimientos.append({
        'referencia': referencia,
        'tipo': 'entrada',
        'cantidad': cantidad_adicional,
        'motivo': 'reposición',
        'fecha': datetime.now()
    })

    return True, f"Se agregaron {cantidad_adicional} unidades al inventario."
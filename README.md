# LuxBeauty Lab Login

Esta es una aplicación web sencilla para el inicio de sesión de LuxBeauty Lab. Gestiona y optimiza procesos laborales a través de su interfaz de usuario.

## Características

* Interfaz de inicio de sesión.
* Validación básica de credenciales (demo).
* Diseño responsivo.
* Fondo difuminado en el panel de login.

## Tecnologías Utilizadas

* **Backend:** Python 3, Flask
* **Frontend:** HTML, Tailwind CSS, JavaScript
* **Otros:** Pip (administrador de paquetes de Python)

## Requisitos Previos

Asegúrate de tener instalado lo siguiente en tu sistema:

* Python 3.x
* pip (viene con Python)

## Configuración e Instalación

Sigue estos pasos para configurar y ejecutar el proyecto localmente:

1.  **Clonar el repositorio:**
    ```bash
    git clone <URL_DE_TU_REPOSITORIO>
    cd LuxBeautyLab
    ```

2.  **Crear y activar un entorno virtual:**
    Es una buena práctica aislar las dependencias de tu proyecto.
    ```bash
    python -m venv venv
    ```
    * **En Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    * **En macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

3.  **Instalar las dependencias:**
    Todas las librerías necesarias están listadas en `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

## Cómo Ejecutar la Aplicación

1.  Asegúrate de que tu entorno virtual esté activado.
2.  Desde la raíz del proyecto, ejecuta el archivo principal de la aplicación:
    ```bash
    python app.py
    ```

## Uso

Una vez que la aplicación esté corriendo, abre tu navegador web y navega a la siguiente dirección:

[http://127.0.0.1:5000](http://127.0.0.1:5000)

Podrás interactuar con la página de inicio de sesión. Las credenciales de demo para probar el inicio de sesión son:
* **Usuario:** `user@example.com`
* **Contraseña:** `password123`
from flask import Flask, render_template, request, jsonify, send_from_directory
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(
    __name__,
    static_folder=os.path.join(BASE_DIR, 'static'), 
    template_folder=BASE_DIR
)

@app.route('/')
def index():
    """
    Sirve la página principal (index.html).
    """
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json() 
    username = data.get('username')
    password = data.get('password')

    if username == 'user@example.com' and password == 'password123':
        return jsonify({'success': True, 'message': '¡Inicio de sesión exitoso!'}), 200
    else:
        return jsonify({'success': False, 'message': 'Usuario o contraseña incorrectos'}), 401

if __name__ == '__main__':
    app.run(debug=True, port=5000)
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

usuarios = {"admin": "password123"}

@app.route("/")
def login():
    return render_template("index.html")

@app.route("/auth", methods=["POST"])
def auth():
    usuario = request.form.get("usuario")
    contraseña = request.form.get("contraseña")

    if usuario in usuarios and usuarios[usuario] == contraseña:
        return redirect(url_for("dashboard", username=usuario))
    else:
        return "❌ Usuario o contraseña incorrectos. <a href='/'>Volver</a>"

@app.route("/dashboard/<username>")
def dashboard(username):
    return f"<h1>Bienvenido, {username} 🎉</h1><p>Panel principal</p>"

if __name__ == "__main__":
    app.run(debug=True)
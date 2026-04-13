import os
import unicodedata

from flask import Flask, redirect, render_template, request, session
import pandas

from dashboard import creartablero
from database import conectar
from database import insertar_estudiante
from pandas import isna

pd = pandas

server = Flask(__name__)
server.secret_key = os.getenv("SECRET_KEY", "190305")


@server.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


#Funcion para quitar acentos/tildes

def quitar_acentos(texto):
    if pd.isna(texto):
        return texto 
    texto = str(texto)
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )


@server.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["nombre"]
        password = request.form["password"]

        conn = conectar() 
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM usuarios WHERE nombre=%s AND password=%s",
            (username, password),
        )
        usuario = cursor.fetchone()
        conn.close()

        if usuario:
            session["nombre"] = usuario["nombre"]
            session["rol"] = usuario["rol"]
            return redirect("/tablero/")

        return render_template(
            "login.html",
            error="Usuario o contrasena incorrectos",
        )

    return render_template("login.html")


@server.route("/insertar_estudiante/", methods=["POST", "GET"])
def insertar_estudiante_route():
    if "nombre" not in session:
        return redirect("/")

    if request.method == "POST":
        nombre = request.form["nombre"]
        edad = request.form["edad"]
        carrera = request.form["carrera"]
        nota1 = float(request.form["nota1"])
        nota2 = float(request.form["nota2"])
        nota3 = float(request.form["nota3"])

        insertar_estudiante(nombre, edad, carrera, nota1, nota2, nota3)
        return redirect("/tablero/")

    return render_template("registro-estudiante.html")




@server.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@server.before_request
def proteger_tablero():
    if request.path.startswith("/tablero") and "nombre" not in session:
        return redirect("/")
    return None

def calculardesempeño(nota1, nota2, nota3):
    promedio = (nota1 + nota2 + nota3) / 3
    if promedio >= 4.5:
        return "Excelente"
    elif promedio >= 3.5:
        return "Bueno"
    elif promedio >= 2.5:
        return "Regular"
    else:
        return "Deficiente"


creartablero(server)


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    server.run(host="0.0.0.0", port=port, debug=True)

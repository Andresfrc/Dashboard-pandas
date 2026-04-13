import os
from urllib.parse import urlparse

import mysql.connector
import pandas as pd


def conectar():
    db_url = (
        os.getenv("DATABASE_URL")
        or os.getenv("MYSQL_URL")
        or os.getenv("MYSQLDATABASE_URL")
    )
    if db_url:
        parsed = urlparse(db_url)
        host = parsed.hostname
        user = parsed.username
        password = parsed.password
        database = parsed.path.lstrip("/")
        port = parsed.port or 3306
    else:
        host = os.getenv("MYSQLHOST") or os.getenv("DB_HOST") or "localhost"
        user = os.getenv("MYSQLUSER") or os.getenv("DB_USER") or "root"
        password = os.getenv("MYSQLPASSWORD") or os.getenv("DB_PASSWORD") or ""
        database = os.getenv("MYSQLDATABASE") or os.getenv("DB_NAME") or "bd_tablero"
        port = int(os.getenv("MYSQLPORT") or os.getenv("DB_PORT") or "3306")

    conexion = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        port=port,
    )
    return conexion


def obtener_usuarios(nombre=None):
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)

    if nombre:
        # CORREGIDO: columna es 'nombre', no 'user'
        cursor.execute("SELECT * FROM usuarios WHERE nombre=%s", (nombre,))
    else:
        cursor.execute("SELECT * FROM usuarios")

    usuarios = cursor.fetchall()
    conexion.close()
    return usuarios


def obtener_estudiantes():
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM estudiantes")
    estudiantes = cursor.fetchall()
    conexion.close()

    # Retorna directamente el DataFrame
    df = pd.DataFrame(estudiantes)
    return df



def insertar_estudiante(nombre, edad, carrera, nota1, nota2, nota3):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO estudiantes (nombre, edad, carrera, nota1, nota2, nota3) VALUES (%s, %s, %s, %s, %s, %s)",
        (nombre, edad, carrera, nota1, nota2, nota3)
    )
    conexion.commit()
    conexion.close()


if __name__ == "__main__":
    conexion = conectar()
    if conexion.is_connected():
        print("Conexión exitosa a la base de datos")
    else:
        print("Error al conectar a la base de datos")

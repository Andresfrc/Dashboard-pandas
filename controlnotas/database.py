import os
from urllib.parse import urlparse

import mysql.connector
import pandas as pd


def conectar():
    return mysql.connector.connect(
        host=os.getenv("MYSQLHOST"),
        port=int(os.getenv("MYSQLPORT",)),
        user=os.getenv("MYSQLUSER"),
        password=os.getenv("MYSQLPASSWORD"),
        database=os.getenv("MYSQLDATABASE")
        
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

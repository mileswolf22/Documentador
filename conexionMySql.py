import mysql.connector
from tkinter import messagebox

def conectar_db():
    try:
        conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "Zelda()23",
            database = "documentador"
        )
        if conn:
            print("conexion exitosa")
        return conn
    except mysql.connector.Error as e:
        messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos: {e}")
        return None

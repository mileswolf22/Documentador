import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import conexionMySql
import subir_publicacion
import sesion

class etiquetascreation(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Crear etiqueta")
        self.geometry("300x200")
        self.resizable(False, True)
        # Crear atributos vacios para las etiquetas
        self.iniciar()
        

    def iniciar(self):
        # Panel superior
        panel_superior = tk.Frame(self, bd=1, relief=tk.FLAT)
        panel_superior.pack(side=tk.TOP, fill="x", padx=10, pady=10)

        label_etiqueta = tk.Label(panel_superior, text="Crear Etiqueta")
        label_etiqueta.pack(pady=5)

        entrada_etiqueta = tk.Entry(panel_superior)
        entrada_etiqueta.pack(pady=5)

        btn_subir_etiqueta = tk.Button(panel_superior, width=20, text="Subir etiqueta", command = lambda: self.guardar_etiqueta(entrada_etiqueta.get()))
        btn_subir_etiqueta.pack(pady=5)
    
    def guardar_etiqueta(self, nombre):
        try: 
            conn = conexionMySql.conectar_db()
            cursor = conn.cursor(buffered = True)
            procedure = "crear_etiqueta"
            print(nombre)
            args = (nombre,)
            
            cursor.callproc(procedure, args)
            
            conn.commit()
            messagebox.showinfo(title="Exito", message="Etiqueta Creada")

        except mysql.connector.Error as e:
            messagebox.showerror(title="Error", message=f"Error de base de datos: {e}")
            conn.rollback()  # Revertir los cambios si ocurre un error
        except mysql.connector.errors.DatabaseError as e:
            messagebox.showerror(title="Error", message=f"Error de base de datos: {e}")
        except ValueError as e:
            messagebox.showerror(title="Error", message=str(e))
        finally:
            # Cerrar conexión y cursor de forma segura
            subir_publicacion.SubirPublicacion.actualizar_combo_etiquetas(self)
            if cursor:
                cursor.close()
            if conn:
                conn.close()
import tkinter  as tk
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from tkinter.font import Font
import conexionMySql
import mysql.connector

class registro(tk.Toplevel):
#[ ]
    def __init__(self, master = None):
        super().__init__(master)
        self.title("Documentador - Registro")
        self.geometry("500x450")
        self.resizable(False, False)
        self.iniciar()

    def iniciar(self):
        label_font = Font(family="Roboto Cn", size = 14)
        label_font_minus = Font(family="Roboto Cn", size = 12)

        etiqueta = tk.Label(self, text="Ingresa tu informacion para registrarte en el sistema", font=label_font)
        etiqueta.pack(pady = 10)

        contenedor_principal = ttkb.Frame(self, bootstyle = "light", relief = "raised", padding = 10)
        contenedor_principal.pack(padx=10, pady=(0,20), fill="x")

        label_usuario = ttkb.Label(contenedor_principal, bootstyle="primary", text="Usuario", font=label_font_minus)
        label_usuario.pack( anchor="w")

        usuario_text = ttkb.Entry(contenedor_principal, bootstyle = "info")
        usuario_text.pack( anchor="w", fill="x")

        label_contra = ttkb.Label(contenedor_principal, bootstyle="primary", text="Contraseña", font=label_font_minus)
        label_contra.pack( anchor="w")

        pass_text = ttkb.Entry(contenedor_principal, bootstyle = "info")
        pass_text.pack( anchor="w", fill="x")

        label_correo = ttkb.Label(contenedor_principal, bootstyle="primary", text="Correo", font=label_font_minus)
        label_correo.pack( anchor="w")

        correo_text = ttkb.Entry(contenedor_principal, bootstyle = "info")
        correo_text.pack( anchor="w", fill="x")

        label_nombre = ttkb.Label(contenedor_principal, bootstyle="primary", text="Nombre(s)", font=label_font_minus)
        label_nombre.pack( anchor="w")

        nombre_text = ttkb.Entry(contenedor_principal, bootstyle = "info")
        nombre_text.pack( anchor="w", fill="x")


        label_apellido = ttkb.Label(contenedor_principal, bootstyle="primary", text="Apellido Paterno", font=label_font_minus)
        label_apellido.pack( anchor="w")

        apellido_text = ttkb.Entry(contenedor_principal, bootstyle = "info")
        apellido_text.pack( anchor="w", fill="x")

        label_apellido_materno = ttkb.Label(contenedor_principal, bootstyle="primary", text="Apellido Materno", font=label_font_minus)
        label_apellido_materno.pack( anchor="w")

        apellido_materno_text = ttkb.Entry(contenedor_principal, bootstyle = "info")
        apellido_materno_text.pack( anchor="w", fill="x")


        boton_registrar = ttkb.Button(self, text="Registro", bootstyle="primary", 
                                      command = lambda: registrar_usuario(usuario_text.get(),
                                                                            pass_text.get(),
                                                                            correo_text.get(),
                                                                            nombre_text.get(),
                                                                            apellido_text.get(),
                                                                            apellido_materno_text.get()) )
        boton_registrar.pack()

        def registrar_usuario(usuario, contra, correo, nombre, apellido_pat, apellido_mat):
            conn = conexionMySql.conectar_db()
            cursor = conn.cursor()
            procedure = "alta_usuario"
            args = (usuario, contra, correo, nombre, apellido_pat, apellido_mat)
            cursor.callproc(procedure, args)
            conn.commit()
        
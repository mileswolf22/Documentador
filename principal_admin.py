import tkinter  as tk
from tkinter import ttk
from PIL import Image, ImageTk
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from tkinter.font import Font
import sesion
import conexionMySql
import mysql.connector

class DashAdmin(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Bienvenido ...")
        self.geometry("550x700")
        self.resizable(False, True)
        # Crear atributos vacios para las etiquetas
        self.usuario_label = None  
        self.correo_label = None
        self.nombres_label = None
        self.apellido_label = None
        self.iniciar()

    def iniciar(self):
        
       # Panel superior
        panel_superior = tk.Frame(self, bd=1, relief=tk.FLAT)
        panel_superior.pack(side=tk.TOP, fill="x", padx=10, pady=10)

        # Imagen de perfil
        self.imagen_perfil = ImageTk.PhotoImage(Image.open("perfil.jpg").resize((100, 100)))
        label_imagen = tk.Label(panel_superior, image=self.imagen_perfil, width=100, height=100)
        label_imagen.grid(row=0, column=0, padx=5)

        # Frame para agrupar los datos a la derecha de la imagen
        datos_frame = tk.Frame(panel_superior)
        datos_frame.grid(row=0, column=1, padx=10, sticky="w")
        
        # Etiquetas para mostrar información del usuario
        self.label_usuario = tk.Label(datos_frame, text="Usuario: ", font=("Dosis", 14))
        self.label_usuario.pack(anchor="w")
        
        self.label_correo = tk.Label(datos_frame, text="Correo: ", font=("Dosis", 14))
        self.label_correo.pack(anchor="w")
        
        self.label_nombres = tk.Label(datos_frame, text="Nombre: ", font=("Dosis", 14))
        self.label_nombres.pack(anchor="w")

        # Panel de banner
        panel_banner = tk.Frame(self, bd=1, relief=tk.FLAT)
        panel_banner.pack(side=tk.TOP, fill="x", pady=5)
        etiqueta_banner = tk.Label( panel_banner, text="Banner de bienvenida", font=("Dosis", 20), bg="burlywood", width=60)
        etiqueta_banner.pack(pady=5)

        # Panel central
        panel_central = tk.Frame(self)
        panel_central.pack(fill="both", expand=True, padx=10)

        # Espacio izquierdo del Treeview
        panel_izquierdo = tk.Frame(panel_central, width=200)
        panel_izquierdo.pack(side=tk.LEFT, fill="y", padx=5, pady=5)

        label_publicaciones = tk.Label(panel_izquierdo, text="Publicaciones en revision", font=("Dosis", 14))
        label_publicaciones.pack(anchor="w", pady=5)

        self.tree = ttk.Treeview(panel_izquierdo, height=10, columns=("Nombre", "Categoria", "Tipo"), show="headings")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Categoria", text="Categoria")
        self.tree.heading("Tipo", text="Tipo")
        self.tree.column("Nombre", width=120)
        self.tree.column("Categoria", width=80)
        self.tree.column("Tipo", width=80)
        self.tree.pack(fill="both", expand=True)


        btn_ver_publi = tk.Button(panel_izquierdo, text="Ver Publicación", font=("Dosis", 12), width=20, command= lambda: self.seleccionar_item_tree(self.tree.selection()))
        btn_ver_publi.pack(pady=10)

        # Panel derecho
        panel_derecho = tk.Frame(panel_central, width=300)
        panel_derecho.pack(side=tk.RIGHT, fill="y", padx=5, pady=5)

        tk.Label(panel_derecho, text="Opciones", font=("Dosis", 14)).grid(row=0, column=0, pady=5, sticky="w")

        tk.Label(panel_derecho, text="Categorías", font=("Dosis", 12)).grid(row=2, column=0, pady=5, sticky="w")
        combo = ttk.Combobox(panel_derecho)
        combo['value'] = sesion.Sesion.categoria
        combo.grid(row=2, column=1, pady=(0,10), sticky="nsew")

        btn_buscar = tk.Button(panel_derecho, text="Buscar", width=10, font=("Dosis", 12))
        btn_buscar.grid(row=3, column=0, columnspan=2, pady=10)

        
        btn_subir = tk.Button(panel_derecho, text="Subir Publicacion", width=20, font=("Dosis", 12))
        btn_subir.grid(row=4, column=0, columnspan=2, pady=10)

        btn_aprobar = tk.Button(panel_derecho, text="Aprobar Publicacion", font=("Dosis", 12), width=20)
        btn_aprobar.grid(row=5, column=0, columnspan=2, pady=10)

        btn_rechazar = tk.Button(panel_derecho, text="Rechazar Publicacion", font=("Dosis", 12), width=20)
        btn_rechazar.grid(row=6, column=0, columnspan=2, pady=10)

        # Ajustar tamaño de panel derecho       
        panel_derecho.grid_columnconfigure(1, weight=1)
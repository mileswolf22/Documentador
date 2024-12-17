import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import subir_publicacion
import sesion
import ver_publicacion

class DashCommon(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Bienvenido")
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

        label_publicaciones = tk.Label(panel_izquierdo, text="Publicaciones recientes", font=("Dosis", 14))
        label_publicaciones.pack(anchor="w", pady=5)

        self.tree = ttk.Treeview(panel_izquierdo, height=15, columns=("Nombre", "Categoria", "Tipo"), show="headings")
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

        tk.Label(panel_derecho, text="Búsqueda", font=("Dosis", 12)).grid(row=1, column=0, pady=5, sticky="w")
        tk.Entry(panel_derecho).grid(row=1, column=1, pady=5, sticky="ew")

        tk.Label(panel_derecho, text="Categorías", font=("Dosis", 12)).grid(row=2, column=0, pady=5, sticky="w")
        combo = ttk.Combobox(panel_derecho)
        combo['value'] = sesion.Sesion.categoria
        combo.grid(row=2, column=1, pady=(0,10), sticky="nsew")

        btn_buscar = tk.Button(panel_derecho, text="Buscar", width=10, font=("Dosis", 12))
        btn_buscar.grid(row=3, column=0, columnspan=2, pady=10)

        
        btn_subir = tk.Button(panel_derecho, text="Subir Publicacion", width=20, font=("Dosis", 12), command = subir_publicacion.SubirPublicacion)
        btn_subir.grid(row=4, column=0, columnspan=2, pady=10)

        btn_solicitar_revision = tk.Button(panel_derecho, text="Solicitar Revision", font=("Dosis", 12), width=20)
        btn_solicitar_revision.grid(row=5, column=0, columnspan=2, pady=10)

        btn_status = tk.Button(panel_derecho, text="Estatus Publicaciones", font=("Dosis", 12), width=20)
        btn_status.grid(row=6, column=0, columnspan=2, pady=10)

        btn_globales = tk.Button(panel_derecho, text="Publicaciones Globales", font=("Dosis", 12), width=20)
        btn_globales.grid(row=7, column=0, columnspan=2, pady=10)

        # Ajustar tamaño de panel derecho       
        panel_derecho.grid_columnconfigure(1, weight=1)


    def show_info(self, usuario, correo, nombres, apellido_pat, apellido_mat):
        """Actualizar las etiquetas con la información recibida."""
        self.label_usuario.config(text=f"Usuario: {usuario}")
        self.label_correo.config(text=f"Correo: {correo}")
        self.label_nombres.config(text=f"Nombre: {nombres} {apellido_pat} {apellido_mat}")

 

    def mostrar_publicaciones(self):
        print("Ingresa a la función de llenado")

        # Verificar que haya publicaciones antes de iterar
        if not hasattr(sesion.Sesion, "publicaciones") or not sesion.Sesion.publicaciones:
            print("No hay publicaciones disponibles.")
            return

        # Limpiar el Treeview antes de agregar nuevos datos
        for item in self.tree.get_children():
            self.tree.delete(item)
        print("!!!AQUI ESTOY!!!")
        # Iterar sobre las publicaciones y agregarlas al Treeview
        for publicacion in sesion.Sesion.publicaciones:
            self.tree.insert("", "end", values=(
                publicacion["nombre_publicacion_doc"],
                publicacion["categoria_publicacion"],
                publicacion["tipo_publicacion"],
            ))

    def seleccionar_item_tree(self, seleccion):
        publicacion = ver_publicacion
        if seleccion:
            item_tree = self.tree.item(seleccion[0])
            valores = item_tree['values']
            print(valores)

            publicacion.ver_archivo(valores)
        return valores  

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal
    root.protocol("WM_DELETE_WINDOW", sesion.Sesion.cerrar_sesion )
    app = DashCommon()
    app.mainloop()
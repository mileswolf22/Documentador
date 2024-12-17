import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import filedialog
from tkinter import messagebox
import sesion
import os
import mysql.connector
import conexionMySql


class SubirPublicacion(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Subir Publicación")
        self.geometry("1100x500")
        self.resizable(False, False)
        # Crear atributos vacíos para las etiquetas
        self.usuario_label = None
        # llenar combo al cargar la pagina
        self.tree = None

        conn = conexionMySql.conectar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT nombre_etiqueta FROM etiquetas")
        etiquetas = [fila[0] for fila in cursor.fetchall()]
        sesion.Sesion.etiqueta_get(etiquetas)

        self.iniciar()

    def iniciar(self):

        seleccion = tk.StringVar()
        sesion_iniciada = sesion.Sesion()
        # Panel de banner
        panel_banner = tk.Frame(self, bd=1, relief=tk.FLAT, bg="burlywood")
        panel_banner.pack(side=tk.TOP, fill="x", pady=5)
        etiqueta_banner = tk.Label(
            panel_banner,
            text="Subir Publicación",
            font=("Dosis", 20, "bold"),
            bg="burlywood",
            fg="white"
        )
        etiqueta_banner.pack(pady=5)

        # Panel central
        panel_central = tk.Frame(self)
        panel_central.pack(fill="both", expand=True, padx=10, pady=10)

        # Espacio izquierdo del Treeview
        panel_izquierdo = tk.Frame(panel_central, width=250)
        panel_izquierdo.grid(row=0, column=0, padx=10, pady=10, sticky="nsw")

        self.tree = ttk.Treeview(
            panel_izquierdo,
            height=15,
            columns=("Tipo", "Nombre", "Peso", "Ruta"),
            show="headings"
        )
        self.tree.heading("Tipo", text="Tipo")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Peso", text="Peso(KB)")
        self.tree.heading("Ruta", text="Ruta")
        self.tree.column("Tipo", width=80)
        self.tree.column("Nombre", width=120)
        self.tree.column("Peso", width=80)
        self.tree.column("Ruta", width=80)
        self.tree.pack(fill="both", expand=True)

        # Panel derecho
        panel_derecho = tk.Frame(panel_central, bd=3, relief="groove", padx=10, pady=10)
        panel_derecho.grid(row=0, column=2, sticky="nsew")

        panel_derecho_new = tk.Frame(panel_central, bd=3, relief="groove",padx=10,pady=10)
        panel_derecho_new.grid(row = 0, column = 1, sticky = "nsew")

        label_usuario = tk.Label(panel_derecho, text=f"Usuario: {sesion_iniciada.nombre_usuario}", font=("Dosis", 14))
        label_usuario.pack(anchor="w")

        #nombre_usuario = label_usuario.cget("text").replace("Usuario: ", "")  # Remueve el prefijo

        # Checkbuttons para opciones
        frame_opciones = tk.Frame(panel_derecho)
        frame_opciones.pack(fill="x", pady=5)

        ttk.Checkbutton(frame_opciones, text="Personal", variable=seleccion, onvalue="Personal", offvalue=0).pack(side="left", padx=5)
        ttk.Checkbutton(frame_opciones, text="Global", variable=seleccion, onvalue="Global", offvalue=0).pack(side="left", padx=5)

        # Categorías
        tk.Label(
            panel_derecho, text="Categorías", font=("Dosis", 12, "bold")
        ).pack(anchor="w", pady=(10, 0))
        categoria = ttk.Combobox(panel_derecho, state="readonly")
        categoria.pack(fill="x", pady=5)
        categoria['value'] = sesion.Sesion.categoria

        tk.Label(panel_derecho, text="Subcategoria", font=("Dosis", 12, "bold")).pack(anchor="w", pady=(10,0))

        subcategoria = ttk.Combobox(panel_derecho, state="readonly")
        subcategoria.pack(fill="x", pady=5)
        subcategoria['value'] = sesion.Sesion.etiquetas

        # Botones
        btn_explorar = tk.Button(
            panel_derecho, text="Examinar", width=20, font=("Dosis", 12), command = lambda: self.seleccionar_archivos()
        )
        btn_explorar.pack(pady=10)

        btn_subir = tk.Button(
            panel_derecho, text="Subir Publicación", width=20, font=("Dosis", 12), bg="#4CAF50", fg="white", command = lambda : self.guardar_archivos(seleccion.get(), categoria.get(), descripcion_text.get("1.0", tk.END).strip(), subcategoria.get())
        )
        btn_subir.pack(pady=10)

        tk.Label(panel_derecho_new, text="Descripcion del documento", font=("Dosis", 12, "bold")).pack(anchor="w", pady=(10,0))
        #Area de texto para la descripcion
        descripcion_text = tk.Text(panel_derecho_new, height=20, width=50)
        descripcion_text.pack(pady=5)

        etiqueta_tree = ttk.Treeview(
            panel_derecho_new,
            height=5,
            columns=("Etiqueta"),
            show="headings"
        )


        # Ajustar proporciones
        panel_central.grid_columnconfigure(1, weight=1)

    def seleccionar_etiquetas(self, etiqueta, tree):
        tree.insert("", "end", values=(etiqueta))
        print(f"La etiqueta {etiqueta} ha sido ingresada")


    # Seleccionar archivos y ponerlos en el treeview
    def seleccionar_archivos(self):
        archivo = filedialog.askopenfilename(filetypes=[("Archivos pdf", "*.pdf")])
        if archivo: 
            tipo = os.path.splitext(archivo)[1].upper()[1:]
            nombre = os.path.basename(archivo)
            peso = f"{os.path.getsize(archivo) /1024:.2f}"
            self.tree.insert("", "end", values=(tipo, nombre, peso, archivo))
            self.archivo_seleccionado = archivo


    def guardar_archivos(self, seleccion, categoria, descripcion, subcategoria):
        try:
            # Conexión a la base de datos
            conn = conexionMySql.conectar_db()
            cursor = conn.cursor(buffered=True)

            print(f"seleccion: {seleccion}")
            items_archivos = self.tree.get_children()

            if not items_archivos:
                messagebox.showerror(title="Error", message="No hay archivos que guardar")
                return

            # Recorrer todos los elementos dentro del tree
            for item in items_archivos:
                tipo = self.tree.item(item, "values")[0]
                nombre = self.tree.item(item, "values")[1]
                peso = self.tree.item(item, "values")[2]
                ruta = self.tree.item(item, "values")[3]

                try: 
                    # Leer el archivo como binario
                    with open(ruta, "rb") as file:
                        archivo_binario = file.read()
                except FileNotFoundError:
                    messagebox.showerror(title="Error", message=f"Archivo no encontrado: {ruta}")
                    continue  # Saltar este archivo y continuar con el siguiente
                except IOError as e:
                    messagebox.showerror(title="Error", message=f"Error al leer el archivo: {e}")
                    continue

                # Crear los argumentos para el procedimiento almacenado
                args = (sesion.Sesion.id_usuario, nombre, categoria, subcategoria, tipo, archivo_binario, float(peso), descripcion, seleccion)

                try:
                    # Llamar al procedimiento almacenado
                    cursor.execute("CALL guardar_publicacion(%s, %s, %s, %s, %s, %s, %s, %s, %s)", args)
                       
                    if seleccion == 'Personal':
                        messagebox.showinfo(title="Exito", message="Subida de archivos personales exitosa.")
                        print(f"Nombre: {nombre}")
                        for item in self.tree.get_children():
                            self.tree.delete(item)
                    elif seleccion == 'Global':
                        messagebox.showinfo(title="Exito", message="Subida de archivos exitosa, revision en curso.")
                        for item in self.tree.get_children():
                            self.tree.delete(item)
                    # Confirmar cambios
                    conn.commit()

                except mysql.connector.Error as e:
                    messagebox.showerror(title="Error", message=f"Error de base de datos: {e}")
                    conn.rollback()  # Revertir los cambios si ocurre un error

                
        except mysql.connector.errors.DatabaseError as e:
            messagebox.showerror(title="Error", message=f"Error de base de datos: {e}")
        except ValueError as e:
            messagebox.showerror(title="Error", message=str(e))
        finally:
            # Cerrar conexión y cursor de forma segura
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    

    # def actualizar_combo_etiquetas(self):
    #     conn = conexionMySql.conectar_db()
    #     cursor = conn.cursor(buffered=True)

    #     etiquetas_act = cursor.execute("SELECT nombre_etiqueta FROM etiquetas")
    #     self.etiquetas['values'] = etiquetas_act

# Crear ventana para probar
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    ventana = SubirPublicacion()
    root.mainloop()
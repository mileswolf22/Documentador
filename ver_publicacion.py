import tkinter as tk
from tkinter import Toplevel, Button, Scrollbar, Frame, Canvas
from PIL import Image, ImageTk
import sesion
import fitz  # PyMuPDF
import fitz

def ver_archivo(datos):
        nombre = datos[0]
        for publicacion in sesion.Sesion.publicaciones: 
            if nombre == publicacion["nombre_publicacion_doc"]:
                archivo = publicacion["archivo_publicacion"]
                print("Entra en funcion ver_archivo")
                # Si el archivo está en binario, escribirlo en un archivo temporal
                ruta_pdf = "temp.pdf"
                with open(ruta_pdf, "wb") as file:
                    file.write(archivo)

                mostrar_pdf_en_ventana(ruta_pdf)

def mostrar_pdf_en_ventana(ruta_pdf):
    class PDFViewer(Toplevel):
        def __init__(self, pdf_path):
            super().__init__()
            self.title("Visor de PDF")
            self.geometry("800x600")  # Tamaño inicial de la ventana

            # Crear el Canvas y los Scrollbars
            self.canvas = Canvas(self)
            self.scroll_y = Scrollbar(self, orient="vertical", command=self.canvas.yview)
            self.scroll_x = Scrollbar(self, orient="horizontal", command=self.canvas.xview)

            self.canvas.configure(yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)

            # Posicionar elementos en la ventana
            self.scroll_y.pack(side="right", fill="y")
            self.scroll_x.pack(side="bottom", fill="x")
            self.canvas.pack(side="left", fill="both", expand=True)

            # Cargar el documento PDF
            self.document = fitz.open(pdf_path)
            self.current_page = 0

            # Contenedor para las imágenes de las páginas
            self.image_container = None

            # Botones para navegación
            btn_frame = Frame(self)
            btn_frame.pack(fill="x")
            Button(btn_frame, text="Página anterior", command=self.prev_page).pack(side="left", padx=10)
            Button(btn_frame, text="Página siguiente", command=self.next_page).pack(side="right", padx=10)

            # Mostrar la primera página
            self.mostrar_pagina(self.current_page)

        def mostrar_pagina(self, numero_pagina):
            try:
                pagina = self.document.load_page(numero_pagina)
                pix = pagina.get_pixmap()
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                img_tk = ImageTk.PhotoImage(img)

                # Limpiar el contenedor anterior
                if self.image_container:
                    self.canvas.delete(self.image_container)

                # Añadir la imagen al Canvas
                self.image_container = self.canvas.create_image(0, 0, anchor="nw", image=img_tk)
                self.canvas.image = img_tk  # Evita que Python elimine la referencia

                # Configurar el tamaño del Canvas según el tamaño de la página
                self.canvas.config(scrollregion=self.canvas.bbox("all"), width=pix.width, height=pix.height)
            except Exception as e:
                print(f"Error al cargar la página: {e}")

        def next_page(self):
            if self.current_page < len(self.document) - 1:
                self.current_page += 1
                self.mostrar_pagina(self.current_page)

        def prev_page(self):
            if self.current_page > 0:
                self.current_page -= 1
                self.mostrar_pagina(self.current_page)

    # Crear y mostrar el visor de PDF
    visor = PDFViewer(ruta_pdf)
    visor.mainloop()
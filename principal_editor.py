import tkinter  as tk
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from tkinter.font import Font
import conexionMySql

class DashEditor(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Bienvenido ...")
        self.geometry("500x700")
        self.resizable(False, True)
        self.iniciar()

    def iniciar(self):
        # Panel superior
        panel_superior = tk.Frame(self, bd=1, relief=tk.FLAT)
        panel_superior.pack(side=tk.TOP, fill="x", padx=10, pady=10)

        # Imagen de perfil
        label_prueba = tk.Label(panel_superior, text="Editor")
        label_prueba.pack()

import tkinter  as tk
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from tkinter.font import Font
from tkinter import messagebox
import conexionMySql
import registro
import principal_comun
import principal_admin
import principal_editor
import mysql.connector
import sesion

class menuApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Documentador")
        self.geometry("300x370")
        self.resizable(False, False)
        self.iniciar()

    # def verificar_entrada(self, entrada):
    #     entry_us = entrada
    #     print(entry_us)
    #     if entry_us == "":
    #         principal_comun.DashCommon()
    #         print("vacio")
    #     elif entry_us == "admin":
    #         principal_admin.DashAdmin()
    #         print("admin")
    #     elif entry_us == "editor":
    #         principal_editor.DashEditor()
    #         print("editor")
    
    def iniciar(self):
        label_font = Font(family="Roboto Cn", size = 14)
        label_font_minus = Font(family="Roboto Cn", size = 12)

        etiqueta = tk.Label(self, text="Bienvenido", font=label_font)
        etiqueta.pack(pady = 10)

        contenedor_principal = ttkb.Frame(self, bootstyle = "light", relief = "raised", padding = 10)
        contenedor_principal.pack(padx=10, pady=(0,20), fill="x")

        label_usuario = ttkb.Label(contenedor_principal, bootstyle="primary", text="Usuario", font=label_font_minus)
        label_usuario.pack(pady=10, anchor="w")

        usuario_text = ttkb.Entry(contenedor_principal, bootstyle = "info")
        usuario_text.pack(pady=10, anchor="w", fill="x")


        label_usuario = ttkb.Label(contenedor_principal, bootstyle="primary", text="Contraseña", font=label_font_minus)
        label_usuario.pack(pady=10, anchor="w")

        pass_text = ttkb.Entry(contenedor_principal, bootstyle = "info", show="*")
        pass_text.pack(pady=10, anchor="w", fill="x")

        boton_acceder = ttkb.Button(self, text="Acceder", bootstyle="success", command= lambda: 
                                                                                            self.iniciar_sesion(
                                                                                                usuario_text.get(),
                                                                                                pass_text.get()))
        boton_acceder.pack(pady=(15, 5))

        boton_registrar = ttkb.Button(self, text="Registro", bootstyle="primary", command = registro.registro)
        boton_registrar.pack(pady=(5, 10))

    def iniciar_sesion(self, ingress_usuario, ingress_pass):
        id_result = 0
        id_permiso = 0
        nombre = ""
        ap_pat = ""
        ap_mat = ""
        correo = ""
        usuario_prod = ""
       
        if ingress_usuario == "" or ingress_pass == "":
                messagebox.showwarning(title="Aviso", message="Complete los campos correspondientes") 
        else:
            try: 
                conn = conexionMySql.conectar_db()
                cursor = conn.cursor()

                procedure = "verif_usuario" #verifica usuario y contraseña
                procedure_second = "verificar_permisos" #verifica permisos del usuario
                procedure_third = "traer_info_usuario" #trae informacion del usuario encontrado

                args = (ingress_usuario, ingress_pass, id_result)

                id_result = cursor.callproc(procedure, args)
                
                print(f"id_result: {id_result}")
                args_second = [id_result[2], id_permiso]    
                print(args_second)

                id_permiso = cursor.callproc(procedure_second, args_second)
                print(id_permiso)

                args_third = [id_result[2], nombre, ap_pat, ap_mat, correo, usuario_prod]  
                print(f"Args_thado: {args_third}")
                informacion_resultante = cursor.callproc(procedure_third, args_third)
                print(f"info: {informacion_resultante}")
                #la info resultante es una tupla

                cursor.execute("SELECT nombre_categoria FROM categoria")

                # Obtener todos los resultados
                categorias = [fila[0] for fila in cursor.fetchall()]
                print(f"categorias: {categorias}")

                sesion.Sesion.catego_get(categorias)
            
                
                print(id_permiso)
                if id_permiso[1] == 3:
                    ventana_comun = principal_comun.DashCommon()
                    ventana_comun.show_info(
                    informacion_resultante[5],  # usuario
                    informacion_resultante[4],  # correo
                    informacion_resultante[1],  # nombres
                    informacion_resultante[2],  # apellido paterno
                    informacion_resultante[3],  # apellido materno
                    )


                    sesion.Sesion.iniciar_sesion(id_result[2], informacion_resultante[5], id_permiso[1])
                    
                    print("Antes de crashear")
                    cursor.execute(f"SELECT id_publicacion, nombre_publicacion, categoria, tipo, archivo FROM publicacion WHERE id_publicacion_usuario = {sesion.Sesion.id_usuario} AND publicacion_personal = 1")

                    print("Antes de crashear, continua")
                    docs_result = cursor.fetchall()
                   
                    if docs_result:
                        for docs in docs_result:
                            print(f"Cantidad de resultados: {len(docs_result)}")
                
                            sesion.Sesion.publicaciones_get(docs[0] ,docs[1], docs[2], docs[3], docs[4])
                            print(f"Nombre publi: {docs[0]}")                   
                    else:
                        print("sin documentos cargados")
                    # lista_documentos = [fila_doc[0] for fila_doc in (cursor.execute(query)).fetchall()]
                    # print(lista_documentos.fetchall())

                    conn.commit()

                    ventana_comun.mostrar_publicaciones()
                    # docs_result = [fila[0] for fila in cursor.fetchall()]
                    # print(docs_result[1])
                #todo: resolver la forma en la que se traen los datos devuelta
                #por ahora trae todos los datos, ahora hay que ver la forma de seccionarlos y usarlos a conveniencia
                elif id_permiso[1] == 1:
                    principal_admin.DashAdmin()
                elif id_permiso[1] == 4:
                    principal_editor.DashEditor()
                else:
                    messagebox.showerror(title="Error", message="Permiso no válido.")
            except mysql.connector.errors.DatabaseError as e:
                messagebox.showerror(title="Error", message=f"Error de base de datos: {e}")
            except ValueError as e:
                messagebox.showerror(title="Error", message=str(e))
            finally:
                cursor.close()
                conn.close()
            
# Uso de la clase
if __name__ == "__main__":
    app = menuApp()
    app.mainloop()
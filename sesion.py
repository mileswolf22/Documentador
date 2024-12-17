class Sesion:
    id_usuario = None
    nombre_usuario = None
    permisos = None
    categoria = []
    publicaciones = []
    etiquetas = []
    id_publicacion = None
    nombre_publicacion = None
    categoria_publicacion = None
    tipo_publicacion = None
    archivo_publicacion = None


#Guadara datos de interes para la sesion del usuario
    @classmethod
    def iniciar_sesion(cls, id_usuario, nombre_usuario, permisos):
        cls.id_usuario = id_usuario
        cls.nombre_usuario = nombre_usuario
        cls.permisos = permisos
#Cerrara la sesion, blanqueando los datos del usuario en curso
    @classmethod
    def cerrar_sesion(cls):
        cls.id_usuario = None
        cls.nombre_usuario = None
        cls.permisos = None

        cls.nombre_publicacion_doc = None
        cls.categoria_publicacion = None
        cls.tipo_publicacion = None
        cls.archivo_publicacion = None

#Almacenara las categorias existentes en la base de datos
    @classmethod
    def catego_get(cls, categoria):
        cls.categoria = categoria
#Recuperara las publicaciones realizadas por el usuario
    @classmethod
    def publicaciones_get(cls, id_puliccacion, nombre_publicacion_doc ,categoria_publicacion ,tipo_publicacion ,archivo_publicacion):
        # if not hasattr(cls, "publicaciones"):
        #     cls.publicaciones = []  # Inicializa una lista para almacenar todas las publicaciones
        # Guarda cada registro como un diccionario dentro de la lista
        cls.publicaciones.append({
            "id_publicacion": id_puliccacion,
            "nombre_publicacion_doc": nombre_publicacion_doc,
            "categoria_publicacion": categoria_publicacion,
            "tipo_publicacion": tipo_publicacion,
            "archivo_publicacion": archivo_publicacion
    })
        print("Publicacion guardada")

    #Almacenara las categorias existentes en la base de datos
    @classmethod
    def etiqueta_get(cls, etiquetas):
        cls.etiquetas = etiquetas
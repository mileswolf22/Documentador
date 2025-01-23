CREATE DATABASE documentador;
use documentador;

CREATE TABLE usuario (
	id_usuario INT PRIMARY KEY AUTO_INCREMENT NOT NULL, 
	nombres VARCHAR(30),
    apellido_paterno VARCHAR(10),
    apellido_materno VARCHAR(10),
    correo VARCHAR(20) NOT NULL UNIQUE,
    usuario_us VARCHAR (20) NOT NULL UNIQUE,
    pass VARCHAR(8) NOT NULL,
    foto BLOB,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)CHARSET=latin1;

/*Publicaciones Globales*/
CREATE TABLE publicacion(
/*El peso de la publicacion se determina en kb*/
	id_publicacion INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    id_publicacion_usuario INT,
    FOREIGN KEY(id_publicacion_usuario) REFERENCES usuario(id_usuario),
    nombre_publicacion VARCHAR(100),
    categoria VARCHAR(10),
    tipo varchar(200) NOT NULL, /*tipo de archivo*/
	archivo longblob NOT NULL,
    descripcion MEDIUMTEXT,
    peso FLOAT,
    revision BOOL DEFAULT 0,
    publicado BOOL DEFAULT 0,
    publicacion_global BOOL DEFAULT 0,
    publicacion_personal BOOL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*
ALTER TABLE publicacion ADD publicacion_global BOOL DEFAULT 0;
ALTER TABLE publicacion ADD publicacion_personal BOOL DEFAULT 0;
ALTER TABLE publicacion CHANGE aprobado revision BOOL DEFAULT 0;
ALTER TABLE publicacion_personal MODIFY nombre_publicacion VARCHAR(100);

Las publicaciones personales no necesitan ser aprobadas
 pero tampoco son visibles al publico
 unicamente para el usuario autor
*/

/*
ALTER TABLE publicacion ADD peso FLOAT;
ALTER TABLE publicacion ADD descripcion MEDIUMTEXT;
ALTER TABLE publicacion_personal ADD descripcion MEDIUMTEXT;
*/
CREATE TABLE carpeta(
	id_carpeta INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    id_carpeta_usuario INT,
    FOREIGN KEY(id_carpeta_usuario) REFERENCES usuario (id_usuario),
    nombre_carpeta VARCHAR(30),
    categoria VARCHAR(20)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

ALTER TABLE publicacion ADD descripcion VARCHAR(250);

CREATE TABLE categoria(
	id_categoria INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    nombre_categoria VARCHAR(30)
);

ALTER TABLE categoria MODIFY nombre_categoria VARCHAR(30);
insert into categoria (nombre_categoria) value ('Tecnologias');
select * from categoria;

CREATE TABLE permisos(
	id_permiso INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    nombre_permiso VARCHAR(50) UNIQUE NOT NULL
);
/*Tabla intermedia para asignar permisos*/
CREATE TABLE usuario_permisos (
    id_usuario INT,
    id_permiso INT,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
    FOREIGN KEY (id_permiso) REFERENCES permisos(id_permiso),
    PRIMARY KEY (id_usuario, id_permiso)
);

CREATE TABLE etiquetas(
	id_etiqueta INT,
    id_publicacion INT,
    FOREIGN KEY (id_publicacion) REFERENCES publicacion(id_publicacion),
    nombre_etiqueta VARCHAR(20)
);

-- EJEMPLO DE CREACION DE PERMISO
INSERT INTO permisos(nombre_permiso)
VALUES('admin');

INSERT INTO permisos(nombre_permiso)
VALUES('lector');

INSERT INTO permisos(nombre_permiso)
VALUES('creador');

INSERT INTO permisos(nombre_permiso)
VALUES('editor');

INSERT INTO permisos(nombre_permiso)
VALUES('eliminar');

SELECT * FROM permisos;


-- EJEMPLO DE AISGNACION DE PERMISO A USUARIO
-- INSERT INTO usuario_permisos (1, 1)
INSERT INTO usuario_permisos (id_usuario, id_permiso)
VALUES (7, (SELECT id_permiso FROM permisos WHERE nombre_permiso = 'creador'));

select * from usuario_permisos;
DELETE FROM usuario_permisos;

/*Views*/
/*
FORMATO
CREATE VIEW view_name AS
SELECT column1, column2, ...
FROM table_name
WHERE condition;*/

CREATE VIEW common_usuario_view AS
SELECT id_usuario, nombres, apellido_paterno, apellido_materno, foto, correo, pass
where common_user = 1;

CREATE VIEW editor_usuario_view AS
SELECT id_usuario, nombres, apellido_paterno, apellido_materno, foto, correo, pass
where editor_user = 1;

CREATE VIEW admin_usuario_view AS
SELECT id_usuario, nombres, apellido_paterno, apellido_materno, foto, correo, pass
where admin_user = 1;

CREATE VIEW publicaciones_aprobadas AS
SELECT id_publicacion, nombre_publicacion, categoria, tipo, archivo
where aprobado = 1;

/*Store Procedures*/
DELIMITER //
CREATE PROCEDURE alta_usuario(
IN prod_usuario VARCHAR(20),
IN prod_pass VARCHAR(10),
IN prod_correo VARCHAR(20),
IN prod_nombres VARCHAR(50),
IN prod_apellido_paterno VARCHAR(10),
IN prod_apellido_materno VARCHAR(10)
)
BEGIN
/*Primero verificar que el usuario no exista */
	IF EXISTS (SELECT 1 FROM usuario WHERE usuario_us = prod_usuario AND correo = prod_correo) THEN
		SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = "Datos ya existentes";
	ELSE 
/*Agregar el nuevo usuario*/
		INSERT INTO usuario(
			usuario_us,
            pass,
            correo,
            nombres,
            apellido_paterno,
            apellido_materno
        )VALUES(
			prod_usuario,
            prod_pass,
            prod_correo,
            prod_nombres,
            prod_apellido_paterno,
            prod_apellido_materno
        );
        
	END IF;
END //

DELIMITER //
/*CONSULTAR USUARIO CON RETORNO DE ID*/
CREATE PROCEDURE verif_usuario(
	IN prod_user VARCHAR(20),
    IN prod_pass VARCHAR(8),
    OUT prod_id INT
)
BEGIN
	-- Busca el usuario con las credenciales dadas
    SELECT id_usuario
    INTO prod_id
    FROM usuario
    WHERE usuario_us = prod_user
      AND pass = prod_pass;

    -- Si no encuentra coincidencias, establece p_id como NULL
    IF prod_id IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Usuario o contraseña incorrectos.';
    END IF;
END //


	/*set @id_usuario = NULL;
	CALL verif_usuario("Bryan", "Zelda", @id_usuario);
	select @id_usuario;*/



DROP PROCEDURE verificar_permisos
DELIMITER //
CREATE PROCEDURE verificar_permisos(
	IN prod_user_id INT,
    OUT prod_id_permiso INT
)
BEGIN
	SELECT id_permiso INTO prod_id_permiso FROM usuario_permisos WHERE id_usuario = prod_user_id;
END //

CALL verificar_permisos(1);

use documentador
DROP PROCEDURE traer_info_usuario;
DELIMITER //
CREATE PROCEDURE traer_info_usuario(
	IN prod_id_usuario INT,
    OUT prod_nombre VARCHAR(30),
    OUT prod_ap_pat VARCHAR(10),
    OUT prod_ap_mat VARCHAR(10),
    OUT prod_correo VARCHAR(20),
    OUT prod_usuario VARCHAR(20)
    )
BEGIN
	SELECT
		nombres,
        apellido_paterno,
        apellido_materno,
        correo,
        usuario_us
	INTO
		prod_nombre,
        prod_ap_pat,
        prod_ap_mat,
        prod_correo,
        prod_usuario
	FROM usuario WHERE id_usuario = prod_id_usuario;
END //

drop procedure guardar_publicacion;
DELIMITER // 
CREATE PROCEDURE guardar_publicacion(
	IN prod_id_user INT,
	IN prod_nombre_publicacion VARCHAR(100),
    IN prod_categoria VARCHAR(30),
    IN prod_tipo varchar(200),
	IN prod_archivo longblob,
    IN prod_peso FLOAT,
    IN prod_descripcion MEDIUMTEXT,
    IN modo VARCHAR(20)
)
BEGIN
	-- Verifica si el usuario tiene permiso de crear publicaciones
    IF NOT EXISTS(
    SELECT 1
    FROM usuario_permisos
    JOIN permisos ON usuario_permisos.id_permiso = permisos.id_permiso
    WHERE usuario_permisos.id_usuario = prod_id_user
    AND (permisos.nombre_permiso = 'creador'
    OR permisos.nombre_permiso = 'admin')
    ) THEN
		SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El usuario no tiene permiso para creacion';
	ELSE
		INSERT INTO publicacion(
			id_publicacion_usuario,
            nombre_publicacion,
            categoria,
            tipo,
            archivo,
            peso,
            descripcion
        )VALUES(
			prod_id_user,
            prod_nombre_publicacion,
            prod_categoria,
            prod_tipo,
            prod_archivo,
            prod_peso,
            prod_descripcion
        );
        
	UPDATE publicacion
    SET
		publicacion_global = CASE
				WHEN modo = 'Global' THEN TRUE
                ELSE FALSE
			END,
		publicacion_personal = CASE
				WHEN modo = 'Personal' THEN TRUE
                ELSE FALSE
			END,
		revision = CASE
				WHEN modo = 'Global' THEN TRUE
				ELSE FALSE
			END
		WHERE id_publicacion = LAST_INSERT_ID();
	END IF;
END //

CALL traer_info_usuario(1);
CALL traer_categorias;
select * from usuario;
use documentador;
DELETE FROM usuario;
ALTER TABLE usuario AUTO_INCREMENT = 1;

SHOW ENGINE INNODB STATUS;
SHOW PROCESSLIST;
KILL 431


SET GLOBAL max_allowed_packet = 1073741824;
SHOW VARIABLES LIKE 'max_allowed_packet';
SHOW VARIABLES LIKE 'config_file';
SHOW VARIABLES LIKE 'net_buffer_length';

SELECT nombre_publicacion,categoria,tipo,archivo FROM publicacion WHERE id_publicacion_usuario = 7 AND publicacion_personal = 1

SELECT * FROM publicacion
SELECT publicacion.nombre_publicacion,publicacion.categoria,publicacion.tipo,publicacion.archivo, usuario.id_usuario FROM publicacion INNER JOIN usuario ON usuario.id_usuario = 7 and  publicacion.id_publicacion_usuario = 7 AND publicacion_personal = 1;
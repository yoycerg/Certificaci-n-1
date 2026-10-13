from datetime import date
from flask_app.config.mysqlconnection import connectToMySQL
DB = 'cinepedia'
class Pelicula:
    @staticmethod
    def buscar_por_nombre(nombre):
        db = connectToMySQL(DB)
        try:
            filas = db.query_db("SELECT id FROM peliculas WHERE nombre=%s", (nombre,))
            return filas[0] if filas else None
        finally: db.close()
    @staticmethod
    def validar(d, id=None):
        errores = []
        for campo, etiqueta, maximo in (('nombre', 'Nombre de la película', 150), ('director', 'Director', 120), ('fecha_estreno', 'Fecha de Estreno', None), ('sinopsis', 'Sinopsis', None)):
            if not d[campo]: errores.append(f'{etiqueta} no puede estar vacío.' if campo != 'sinopsis' and campo != 'fecha_estreno' else f'{etiqueta} no puede estar vacía.')
            elif campo != 'fecha_estreno' and len(d[campo]) < 3: errores.append(f'{etiqueta} debe tener al menos 3 caracteres.')
            elif maximo and len(d[campo]) > maximo: errores.append(f'{etiqueta} no puede superar los {maximo} caracteres.')
        if d['fecha_estreno']:
            try: date.fromisoformat(d['fecha_estreno'])
            except ValueError: errores.append('La fecha de estreno no es válida.')
        if d['nombre'] and not errores:
            existente = Pelicula.buscar_por_nombre(d['nombre'])
            if existente and existente['id'] != id: errores.append('Ya existe una película con ese nombre.')
        return errores
    @staticmethod
    def todas():
        db = connectToMySQL(DB)
        try: return db.query_db("SELECT p.*, CONCAT(u.nombre,' ',u.apellido) AS autor FROM peliculas p JOIN usuarios u ON u.id=p.usuario_id ORDER BY p.creado_en DESC")
        finally: db.close()
    @staticmethod
    def buscar(id):
        db = connectToMySQL(DB)
        try:
            filas = db.query_db("SELECT p.*, CONCAT(u.nombre,' ',u.apellido) AS autor FROM peliculas p JOIN usuarios u ON u.id=p.usuario_id WHERE p.id=%s", (id,))
            return filas[0] if filas else None
        finally: db.close()
    @staticmethod
    def crear(d):
        db = connectToMySQL(DB)
        try: return db.query_db('INSERT INTO peliculas (usuario_id,nombre,director,fecha_estreno,sinopsis) VALUES (%(usuario_id)s,%(nombre)s,%(director)s,%(fecha_estreno)s,%(sinopsis)s)', d)
        finally: db.close()
    @staticmethod
    def actualizar(d):
        db = connectToMySQL(DB)
        try: return db.query_db('UPDATE peliculas SET nombre=%(nombre)s,director=%(director)s,fecha_estreno=%(fecha_estreno)s,sinopsis=%(sinopsis)s WHERE id=%(id)s AND usuario_id=%(usuario_id)s', d)
        finally: db.close()
    @staticmethod
    def eliminar(id, usuario_id):
        db = connectToMySQL(DB)
        try: return db.query_db('DELETE FROM peliculas WHERE id=%s AND usuario_id=%s', (id, usuario_id))
        finally: db.close()

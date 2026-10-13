from flask_app.config.mysqlconnection import connectToMySQL
DB = 'cinepedia'
class Comentario:
    @staticmethod
    def todos_de_pelicula(id):
        db = connectToMySQL(DB)
        try: return db.query_db("SELECT c.*, CONCAT(u.nombre,' ',u.apellido) AS autor FROM comentarios c JOIN usuarios u ON u.id=c.usuario_id WHERE c.pelicula_id=%s ORDER BY c.creado_en DESC", (id,))
        finally: db.close()
    @staticmethod
    def crear(d):
        db = connectToMySQL(DB)
        try: return db.query_db('INSERT INTO comentarios (pelicula_id,usuario_id,contenido) VALUES (%(pelicula_id)s,%(usuario_id)s,%(contenido)s)', d)
        finally: db.close()
    @staticmethod
    def buscar(id):
        db = connectToMySQL(DB)
        try:
            rows = db.query_db('SELECT * FROM comentarios WHERE id=%s', (id,))
            return rows[0] if rows else None
        finally: db.close()
    @staticmethod
    def eliminar(id, usuario_id):
        db = connectToMySQL(DB)
        try: return db.query_db('DELETE FROM comentarios WHERE id=%s AND usuario_id=%s', (id, usuario_id))
        finally: db.close()

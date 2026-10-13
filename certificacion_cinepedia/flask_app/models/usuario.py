from flask_app.config.mysqlconnection import connectToMySQL
DB = 'cinepedia'
class Usuario:
    @staticmethod
    def crear(datos):
        db = connectToMySQL(DB)
        try:
            return db.query_db('INSERT INTO usuarios (nombre, apellido, email, password_hash) VALUES (%(nombre)s, %(apellido)s, %(email)s, %(password_hash)s)', datos)
        finally: db.close()
    @staticmethod
    def buscar_por_email(email):
        db = connectToMySQL(DB)
        try:
            filas = db.query_db('SELECT * FROM usuarios WHERE email=%s', (email,))
            return filas[0] if filas else None
        finally: db.close()


from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "cambia-esta-clave-por-una-frase-segura"
bcrypt = Bcrypt(app)

MESES = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

@app.template_filter('fecha_corta')
def fecha_corta(f):
    return f"{f.day} de {MESES[f.month - 1]}"

from flask_app.controllers import usuarios
from flask_app.controllers import cine

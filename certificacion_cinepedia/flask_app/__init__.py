
import os
from dotenv import load_dotenv
from flask import Flask
from flask_bcrypt import Bcrypt

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
bcrypt = Bcrypt(app)

MESES = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

# muestra la fecha como "10 de Mayo"
@app.template_filter('fecha_corta')
def fecha_corta(f):
    return f"{f.day} de {MESES[f.month - 1]}"

from flask_app.controllers import usuarios
from flask_app.controllers import cine

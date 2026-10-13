import re
from flask import render_template, request, redirect, session, flash
from flask_app import app, bcrypt
from flask_app.models.usuario import Usuario

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


@app.route('/')
@app.route('/registro')
def registro():
    if 'usuario_id' in session:
        return redirect('/cine')
    return render_template('registro.html')


@app.route('/registrar', methods=['POST'])
def registrar():
    nombre = request.form.get('nombre', '').strip()
    apellido = request.form.get('apellido', '').strip()
    email = request.form.get('email', '').strip().lower()
    password = request.form.get('password', '')
    confirmar = request.form.get('confirmar', '')

    valido = True
    if len(nombre) < 2 or len(apellido) < 2:
        flash('Nombre y apellido deben tener al menos 2 caracteres.')
        valido = False
    if not EMAIL_REGEX.match(email):
        flash('El e-mail no es válido.')
        valido = False
    elif Usuario.buscar_por_email(email):
        flash('Ese e-mail ya está registrado.')
        valido = False
    if len(password) < 8:
        flash('La contraseña debe tener al menos 8 caracteres.')
        valido = False
    if password != confirmar:
        flash('Las contraseñas no coinciden.')
        valido = False
    if not valido:
        return redirect('/registro')

    usuario_id = Usuario.crear({
        'nombre': nombre,
        'apellido': apellido,
        'email': email,
        'password_hash': bcrypt.generate_password_hash(password).decode('utf-8'),
    })
    session['usuario_id'] = usuario_id
    session['nombre'] = nombre
    return redirect('/cine')


@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email', '').strip().lower()
    usuario = Usuario.buscar_por_email(email)
    if not usuario or not bcrypt.check_password_hash(usuario['password_hash'], request.form.get('password', '')):
        flash('E-mail o contraseña incorrectos.')
        return redirect('/registro')
    session['usuario_id'] = usuario['id']
    session['nombre'] = usuario['nombre']
    return redirect('/cine')


@app.route('/cerrar_sesion')
def cerrar_sesion():
    session.clear()
    return redirect('/registro')

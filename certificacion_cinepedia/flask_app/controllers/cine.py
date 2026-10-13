from flask import render_template, request, redirect, session, flash, abort
from flask_app import app
from flask_app.models.pelicula import Pelicula
from flask_app.models.comentario import Comentario

def login_requerido(): return 'usuario_id' in session

@app.route('/cine')
def cine():
    if not login_requerido(): return redirect('/registro')
    return render_template('cine.html', peliculas=Pelicula.todas())

def datos_formulario():
    return {'nombre': request.form.get('nombre', '').strip(), 'director': request.form.get('director', '').strip(),
            'fecha_estreno': request.form.get('fecha_estreno', '').strip(), 'sinopsis': request.form.get('sinopsis', '').strip()}

@app.route('/cine/nuevo', methods=['GET','POST'])
def nueva_pelicula():
    if not login_requerido(): return redirect('/registro')
    datos = {}
    if request.method=='POST':
        datos = datos_formulario()
        errores = Pelicula.validar(datos)
        if not errores:
            datos['usuario_id'] = session['usuario_id']
            Pelicula.crear(datos)
            return redirect('/cine')
        for e in errores: flash(e)
    return render_template('nueva_pelicula.html', datos=datos)

@app.route('/cine/<int:id>')
def ver_pelicula(id):
    if not login_requerido(): return redirect('/registro')
    p=Pelicula.buscar(id)
    if not p: abort(404)
    return render_template('ver_pelicula.html', pelicula=p, comentarios=Comentario.todos_de_pelicula(id))

@app.route('/cine/editar/<int:id>', methods=['GET','POST'])
def editar_pelicula(id):
    if not login_requerido(): return redirect('/registro')
    p=Pelicula.buscar(id)
    if not p: abort(404)
    if p['usuario_id'] != session['usuario_id']: abort(403)
    datos = p
    if request.method=='POST':
        datos = datos_formulario()
        errores = Pelicula.validar(datos, id)
        if not errores:
            datos.update({'id': id, 'usuario_id': session['usuario_id']})
            Pelicula.actualizar(datos)
            return redirect('/cine')
        for e in errores: flash(e)
    return render_template('editar_pelicula.html', datos=datos)

@app.route('/cine/eliminar/<int:id>', methods=['POST'])
def eliminar_pelicula(id):
    if not login_requerido(): return redirect('/registro')
    Pelicula.eliminar(id,session['usuario_id']); return redirect('/cine')

@app.route('/cine/<int:id>/comentarios', methods=['POST'])
def crear_comentario(id):
    if not login_requerido(): return redirect('/registro')
    p=Pelicula.buscar(id)
    if not p: abort(404)
    contenido=request.form.get('contenido','').strip()
    if p['usuario_id']==session['usuario_id']: flash('No puedes comentar tu propia película.')
    elif not contenido: flash('El comentario no puede estar vacío.')
    elif len(contenido)>1000: flash('El comentario no puede superar los 1000 caracteres.')
    else: Comentario.crear({'pelicula_id':id,'usuario_id':session['usuario_id'],'contenido':contenido})
    return redirect(f'/cine/{id}')

@app.route('/comentarios/<int:id>/eliminar', methods=['POST'])
def eliminar_comentario(id):
    if not login_requerido(): return redirect('/registro')
    c=Comentario.buscar(id)
    if c and c['usuario_id']==session['usuario_id']: Comentario.eliminar(id,session['usuario_id'])
    return redirect(request.referrer or '/cine')

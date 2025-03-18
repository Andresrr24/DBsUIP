from flask import Flask, render_template, request, redirect, url_for
import keydb

app = Flask(__name__)

db = keydb.KeyDB(host='localhost', port=6379, db=0)

@app.route('/')
def index():
    libros = []
    for key in db.scan_iter('libro:*'):
        libro = db.hgetall(key)
        libro_decodificado = {k.decode('utf-8'): v.decode('utf-8') for k, v in libro.items()} 
        libro_decodificado['id'] = key.decode('utf-8').split(':')[1]  
        libros.append(libro_decodificado)
    return render_template('index.html', libros=libros)

# Agregar libros
@app.route('/agregar_libro', methods=['GET', 'POST'])
def agregar_libro():
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        genero = request.form['genero']
        libro_id = db.incr("libro_id") 
        libro_key = f"libro:{libro_id}"
        db.hset(libro_key, mapping={
            "id": libro_id,
            "titulo": titulo,
            "autor": autor,
            "genero": genero
        })
        return redirect(url_for('index'))
    return render_template('agregar_libro.html')

# Editar un libro existente
@app.route('/editar_libro/<int:id>', methods=['GET', 'POST'])
def editar_libro(id):
    libro_key = f"libro:{id}"
    libro = db.hgetall(libro_key)
    libro_decodificado = {k.decode('utf-8'): v.decode('utf-8') for k, v in libro.items()}  
    libro_decodificado['id'] = id 
    if request.method == 'POST':
        db.hset(libro_key, mapping={
            "titulo": request.form['titulo'],
            "autor": request.form['autor'],
            "genero": request.form['genero']
        })
        return redirect(url_for('index'))
    return render_template('editar_libro.html', libro=libro_decodificado)

# Eliminar un libro
@app.route('/eliminar_libro/<int:id>')
def eliminar_libro(id):
    libro_key = f"libro:{id}"
    if db.exists(libro_key): 
        db.delete(libro_key)
    return redirect(url_for('index'))

# Buscar libros
@app.route('/buscar_libros', methods=['GET', 'POST'])
def buscar_libros():
    if request.method == 'POST':
        query = request.form['query']
        libros = []
        for key in db.scan_iter("libro:*"):
            libro = db.hgetall(key)
            libro_decodificado = {k.decode('utf-8'): v.decode('utf-8') for k, v in libro.items()}
            if query.lower() in libro_decodificado.get('titulo', '').lower() or \
               query.lower() in libro_decodificado.get('autor', '').lower() or \
               query.lower() in libro_decodificado.get('genero', '').lower():
                libros.append(libro_decodificado)
        return render_template('buscar_libros.html', libros=libros, query=query)
    return render_template('buscar_libros.html')

if __name__ == '__main__':
    app.run(debug=True)

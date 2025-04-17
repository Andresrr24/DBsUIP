from flask import Flask, render_template, request, redirect, url_for
import requests
import os

app = Flask(__name__)
API_BASE_URL = 'http://localhost:5001/api'

@app.route('/')
def index():
    response = requests.get(f"{API_BASE_URL}/libros")
    libros = response.json().get('libros', [])
    return render_template('index.html', libros=libros)

@app.route('/agregar_libro', methods=['GET', 'POST'])
def agregar_libro():
    if request.method == 'POST':
        data = {
            'titulo': request.form['titulo'],
            'autor': request.form['autor'],
            'genero': request.form['genero']
        }
        requests.post(f"{API_BASE_URL}/libros", json=data)
        return redirect(url_for('index'))
    return render_template('agregar_libro.html')

@app.route('/editar_libro/<int:id>', methods=['GET', 'POST'])
def editar_libro(id):
    if request.method == 'POST':
        data = {
            'titulo': request.form['titulo'],
            'autor': request.form['autor'],
            'genero': request.form['genero']
        }
        requests.put(f"{API_BASE_URL}/libros/{id}", json=data)
        return redirect(url_for('index'))
    
    response = requests.get(f"{API_BASE_URL}/libros/{id}")
    libro = response.json()
    return render_template('editar_libro.html', libro=libro)

@app.route('/eliminar_libro/<int:id>')
def eliminar_libro(id):
    requests.delete(f"{API_BASE_URL}/libros/{id}")
    return redirect(url_for('index'))

@app.route('/buscar_libros', methods=['GET', 'POST'])
def buscar_libros():
    if request.method == 'POST':
        query = request.form['query']
        response = requests.get(f"{API_BASE_URL}/libros/buscar?q={query}")
        libros = response.json().get('libros', [])
        return render_template('buscar_libros.html', libros=libros, query=query)
    return render_template('buscar_libros.html')

if __name__ == '__main__':
    app.run(port=5000)
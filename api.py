from flask import Flask, request, jsonify
import keydb
from flask_restful import Api, Resource
from functools import wraps

app = Flask(__name__)
api = Api(app)
db = keydb.KeyDB(host='localhost', port=6379, db=0)

# Decorador para manejar errores comunes
def handle_errors(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            return {'error': str(e)}, 500
    return wrapper

class LibroResource(Resource):
    @handle_errors
    def get(self, libro_id):
        libro_key = f"libro:{libro_id}"
        if not db.exists(libro_key):
            return {'error': 'Libro no encontrado'}, 404
        
        libro = db.hgetall(libro_key)
        return {k.decode('utf-8'): v.decode('utf-8') for k, v in libro.items()}

    @handle_errors
    def put(self, libro_id):
        libro_key = f"libro:{libro_id}"
        if not db.exists(libro_key):
            return {'error': 'Libro no encontrado'}, 404
        
        data = request.get_json()
        db.hset(libro_key, mapping={
            "titulo": data.get('titulo'),
            "autor": data.get('autor'),
            "genero": data.get('genero')
        })
        return {'message': 'Libro actualizado correctamente'}

    @handle_errors
    def delete(self, libro_id):
        libro_key = f"libro:{libro_id}"
        if not db.exists(libro_key):
            return {'error': 'Libro no encontrado'}, 404
        
        db.delete(libro_key)
        return {'message': 'Libro eliminado correctamente'}

class LibrosResource(Resource):
    @handle_errors
    def get(self):
        libros = []
        for key in db.scan_iter('libro:*'):
            libro = db.hgetall(key)
            libros.append({k.decode('utf-8'): v.decode('utf-8') for k, v in libro.items()})
        return {'libros': libros}

    @handle_errors
    def post(self):
        data = request.get_json()
        libro_id = db.incr("libro_id")
        libro_key = f"libro:{libro_id}"
        
        db.hset(libro_key, mapping={
            "id": libro_id,
            "titulo": data.get('titulo'),
            "autor": data.get('autor'),
            "genero": data.get('genero')
        })
        return {'message': 'Libro creado correctamente', 'id': libro_id}, 201

class BuscarLibrosResource(Resource):
    @handle_errors
    def get(self):
        query = request.args.get('q', '').lower()
        if not query:
            return {'error': 'Parámetro de búsqueda requerido'}, 400
        
        libros = []
        for key in db.scan_iter('libro:*'):
            libro = db.hgetall(key)
            libro_decod = {k.decode('utf-8'): v.decode('utf-8') for k, v in libro.items()}
            if (query in libro_decod.get('titulo', '').lower() or
                query in libro_decod.get('autor', '').lower() or
                query in libro_decod.get('genero', '').lower()):
                libros.append(libro_decod)
        
        return {'libros': libros}

# Configuración de rutas API
api.add_resource(LibrosResource, '/api/libros')
api.add_resource(LibroResource, '/api/libros/<int:libro_id>')
api.add_resource(BuscarLibrosResource, '/api/libros/buscar')

if __name__ == '__main__':
    app.run(port=5001)
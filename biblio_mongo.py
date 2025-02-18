from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client['biblioteca']
collection = db['libros']

def agregar_libro():
    titulo = input('Titulo: ')
    autor = input('Autor: ')
    genero = input('Genero: ')
    estado = input('Estado: ')

    libro = {'titulo': titulo, 'autor': autor, 'genero': genero, 'estado': estado}
    collection.insert_one(libro)

    return f'libro {titulo} agregado.'

def actualizar_libro():
    titulo = input('Nombre del libro a actualizar: ')
    libro = collection.find_one({'titulo': titulo})

    registros_actualizar = input('Registros a actualizar: ')
    registros_actualizar = registros_actualizar.lower()

    nuevo_titulo = None
    nuevo_autor = None
    nuevo_genero = None
    nuevo_estado = None

    if 'titulo' in registros_actualizar:
        nuevo_titulo = input('Nuevo titulo: ')
    if 'autor' in registros_actualizar:
        nuevo_autor = input('Nuevo autor: ')
    if 'genero' in registros_actualizar:
        nuevo_genero = input('Nuevo genero: ')
    if 'estado' in registros_actualizar:
        nuevo_estado = input('Nuevo estado: ')

    resultado = collection.update_one(
        {'titulo': titulo},
        {'$set': {'titulo': nuevo_titulo if nuevo_titulo else libro['titulo'], 
                  'autor': nuevo_autor if  nuevo_autor else libro['autor'], 
                  'genero': nuevo_genero if nuevo_genero else libro['genero'], 
                  'estado': nuevo_estado if nuevo_estado else libro['estado']
                  }}
    )

    if resultado.modified_count:
        print('Cambios realizados con exito')
    else:
        print('Error al realizar los cambios, verifique informacion')

def eliminar_libro():
    titulo = input('Nombre del libro a eliminar: ')
    resultado = collection.delete_one({'titulo': titulo})

    if resultado.deleted_count:
        print('Cambios realizados con exito')
    else:
        print('Error al realizar los cambios, verifique informacion')

def ver_libros():
    print('Lista de libros:\n')
    for libro in collection.find():
        print(f"{libro['titulo']}, autor: {libro['autor']}, genero: {libro['genero']}, estado: {libro['estado']}")

def buscar_por_titulo():
    titulo = input('Nombre del libro: ')
    resultado = collection.find({'titulo': titulo})

    for libro in resultado:
        print(libro)
        encontrado = True

    if not encontrado:
        print(f'No se encontraron libros con el nombre "{titulo}".')

if __name__ == '__main__':
    while True:
        print("""
        Biblioteca
        1. Agregar libro
        2. Actualizar libro
        3. Eliminar libro
        4. Ver todos los libros
        5. Buscar por nombre
        6. Salir      
            """)
        opcion = int(input("Seleccione una opcion: "))

        if opcion == 1:
            agregar_libro()
        elif opcion == 2: 
            actualizar_libro()
        elif opcion == 3:
            eliminar_libro()
        elif opcion == 4:
            ver_libros()
        elif opcion == 5:
            buscar_por_titulo()
        elif opcion == 6:
            print('Saliendo...')
            break
        else:
            print('Opcion invalida')


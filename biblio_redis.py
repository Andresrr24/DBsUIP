import redis # type:ignore

# Conexion a redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Verificar conexion
print(f'Estado de la conexion: {r.ping()}')

def agregar_libro():
    if not r.exists('contador_libros'):
        r.set('contador_libros', 0)

    titulo = input('Titulo: ')
    autor = input('Autor: ')
    genero = input('Genero: ')
    estado = input('Estado: ')

    id = r.incr('contador_libros') 
    r.hset(f'libro:{id}', mapping={
        'titulo': titulo,
        'autor': autor,
        'genero': genero,
        'estado': estado
    })
    r.sadd(f'genero:{genero}', id)
    r.sadd(f'autor: {autor}', id)

    print('Libro agregado.')

def actualizar_libro():
    id = input('Ingrese el ID del libro a actualizar: ')
    if not r.exists(f'libro:{id}'):
        print("Libro no encontrado.")
        return

    libro = r.hgetall(f'libro:{id}')
    print("Datos actuales del libro:")
    for campo, valor in libro.items():
        print(f"{campo.decode()}: {valor.decode()}")

    print("\nIngrese los nuevos datos (deje en blanco para mantener el valor actual):")
    nuevo_titulo = input('Nuevo título: ') or libro[b'titulo'].decode()
    nuevo_autor = input('Nuevo autor: ') or libro[b'autor'].decode()
    nuevo_genero = input('Nuevo género: ') or libro[b'genero'].decode()
    nuevo_estado = input('Nuevo estado (disponible/prestado): ') or libro[b'estado'].decode()

    # Actualizar el libro
    r.hset(f'libro:{id}', mapping={
        'titulo': nuevo_titulo,
        'autor': nuevo_autor,
        'genero': nuevo_genero,
        'estado': nuevo_estado
    })

    # Actualizar índices
    if nuevo_genero != libro[b'genero'].decode():
        r.srem(f'genero:{libro[b"genero"].decode()}', id)  
        r.sadd(f'genero:{nuevo_genero}', id)       

    if nuevo_autor != libro[b'autor'].decode():
        r.srem(f'autor:{libro[b"autor"].decode()}', id)
        r.sadd(f'autor:{nuevo_autor}', id)             

    print('Libro actualizado correctamente.')

def eliminar_libro():
    id = input('Ingrese el ID del libro a eliminar: ')
    if not r.exists(f'libro:{id}'):
        print("Libro no encontrado.")
        return

    libro = r.hgetall(f'libro:{id}')
    r.delete(f'libro:{id}')  # Eliminar el libro
    r.srem(f'genero:{libro[b"genero"].decode()}', id)  
    r.srem(f'autor:{libro[b"autor"].decode()}', id)

    print("Libro eliminado correctamente.")

def ver_libros():
    libros_keys = r.keys('libro:*')
    if not libros_keys:
        print("No hay libros registrados.")
        return
    
    print("\nLista de libros:")
    for key in libros_keys:
        libro = r.hgetall(key)
        print(f"ID: {key.decode().split(':')[1]}")
        for campo, valor in libro.items():
            print(f"{campo.decode()}: {valor.decode()}")
        print('-' * 30)
    
def buscar_por_titulo():
    palabra_clave = input('Ingrese una palabra clave del título: ')
    libros_keys = r.keys('libro:*')
    resultados = []

    for key in libros_keys:
        libro = r.hgetall(key)
        if palabra_clave.lower() in libro[b'titulo'].decode().lower():
            resultados.append(libro)

    if not resultados:
        print("No se encontraron libros con ese título.")
        return

    print("\nResultados de la búsqueda:")
    for libro in resultados:
        for campo, valor in libro.items():
            print(f"{campo.decode()}: {valor.decode()}")
        print('-' * 30)

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
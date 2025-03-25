import sqlite3 # type: ignore

DATABASE = 'presupuest.db'

def conexion_db():
    conexion = sqlite3.connect(DATABASE)
    return conexion

def crear_tabla():
    conexion = conexion_db()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS articulos (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       nombre TEXT NOT NULL,
                       precio REAL NOT NULL,
                       cantidad INTEGER NOT NULL
                       )
        ''')
        conexion.commit()
        print('Tabla creada')
        conexion.close()

def registrar_articulo():
    nombre = str(input('Registre el nombre del articulo: '))
    precio = float(input(f'Precio del producto {nombre}: '))
    cantidad = int(input(f'Cantidad de unidades disponibles del producto {nombre}: '))

    conexion = conexion_db()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute('''
                       INSERT INTO articulos (nombre, precio, cantidad)
                       VALUES (?, ?, ?)
                       ''', (nombre, precio, cantidad))
        conexion.commit()
        print('Articulo agregado con exito')
        conexion.close()

def buscar_articulo():
    nombre = str(input('Articulo a buscar: '))
    conexion = conexion_db()

    cursor = conexion.cursor()
    cursor.execute('''
        SELECT * FROM articulos WHERE nombre LIKE ?
        ''', (f'%{nombre}%',))
    resultados = cursor.fetchall()
    
    if resultados:
        for articulo in resultados:
            print(f'ID: {articulo[0]}, nombre: {articulo[1]}, precio: {articulo[2]}, cantidad: {articulo[3]}')

    conexion.close()

def editar_articulo():
    id_articulo = int(input("ID del artículo a editar: "))
    nuevo_precio = float(input("Nuevo precio: "))
    nueva_cantidad = int(input("Nueva cantidad: "))

    conexion = conexion_db()
    cursor = conexion.cursor()

    cursor.execute('''
                   UPDATE articulos
                   SET precio = ?, cantidad = ?
                   WHERE id = ?
                   ''', (nuevo_precio, nueva_cantidad, id_articulo))
    conexion.commit()
    print('Articulo modificado')
    conexion.close()

def eliminar_articulo():
    id_articulo = int(input('ID del artiuco a eliminar: '))

    conexion = conexion_db()
    cursor = conexion.cursor()

    cursor.excute('''
                DELETE * FROM articulos WHERE id = ?   
                ''', (id_articulo, ))

    conexion.commit()
    print('Articulo eliminado')
    conexion.close()

def menu():
    crear_tabla()
    while True:
        print("\n--- Sistema de Registro de Presupuesto ---")
        print("1. Registrar artículo")
        print("2. Buscar artículo")
        print("3. Editar artículo")
        print("4. Eliminar artículo")
        print("5. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_articulo()
        elif opcion == "2":
            buscar_articulo()
        elif opcion == "3":
            editar_articulo()
        elif opcion == "4":
            eliminar_articulo()
        elif opcion == "5":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == '__main__':
    menu()
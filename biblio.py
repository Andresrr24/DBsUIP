import sqlite3

# Creacion db con su respectiva tabla
con = sqlite3.connect("database.db")
cursor = con.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS libros (
                id INTEGER PRIMARY KEY, 
                titulo TEXT NOT NULL,
                autor TEXT NOT NULL,
                genero TEXT NOT NULL,
                estado BOOL)""")
con.commit()
con.close()

# Agregar libros
def add_book(titulo, autor, genero, estado):
    con = sqlite3.connect("database.db")
    cursor = con.cursor()
    cursor.execute("INSERT INTO libros (titulo, autor, genero, estado) VALUES (?, ?, ?, ?)", 
                   (titulo, autor, genero, estado))
    con.commit()
    con.close()

# Actualizacion para cada campo de un libro
def update_book(book_id, new_titulo=None, new_autor=None, new_genero=None, new_estado=None):
    con = sqlite3.connect("database.db")
    cursor = con.cursor()

    query = []
    new_data = []

    if new_titulo:
        query.append("titulo = ?")
        new_data.append(new_titulo)
    if new_autor:
        query.append("autor = ?")
        new_data.append(new_autor)
    if new_genero:
        query.append("genero = ?")
        new_data.append(new_genero)
    if new_estado is not None:
        query.append("estado = ?")
        new_data.append(new_estado)

    if query:
        final_query = f'UPDATE libros SET {", ".join(query)} WHERE id = ?'
        new_data.append(book_id)
        cursor.execute(final_query, tuple(new_data))
        con.commit()

    con.close()

# Eliminar libros
def del_book(book_id):
    con = sqlite3.connect("database.db")
    cursor = con.cursor()
    cursor.execute("DELETE FROM libros WHERE id = ?", (book_id,))
    con.commit()
    con.close()

# Mostrar todos los libros
def read_book():
    con = sqlite3.connect("database.db")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM libros")
    books = cursor.fetchall()
    con.close()

    if books:
        for book in books:
            estado = "Leído" if book[4] else "No leído"
            print(f"ID: {book[0]}, Título: {book[1]}, Autor: {book[2]}, Género: {book[3]}, Estado: {estado}")
    else:
        print("No hay libros en la base de datos.")

# Buscar libros por cualquier termino
def search_books(search):
    con = sqlite3.connect("database.db")
    cursor = con.cursor()
    cursor.execute("""SELECT * FROM libros WHERE 
                   titulo LIKE ? OR 
                   autor LIKE ? OR 
                   genero LIKE ?""", (f'%{search}%', f'%{search}%', f'%{search}%'))
    books = cursor.fetchall()
    con.close()

    if books:
        for book in books:
            estado = "Leído" if book[4] else "No leído"
            print(f"ID: {book[0]}, Título: {book[1]}, Autor: {book[2]}, Género: {book[3]}, Estado: {estado}")
    else:
        print("Ningún libro coincide con la búsqueda.")

# Menu
def menu():
    print("\nOpciones:")
    print("1. Agregar libro")
    print("2. Actualizar libro")
    print("3. Eliminar libro")
    print("4. Ver libros existentes")
    print("5. Buscar libro")
    print("6. Salir")
    return int(input("Seleccione una opción: "))
# Ejecucion principal
def main():
    while True:
        option = menu()

        if option == 1:
            titulo = input("Introduce el título del libro: ")
            autor = input("Introduce el autor del libro: ")
            genero = input("Introduce el género del libro: ")
            estado = input("Introduce el estado de lectura (leído/no leído): ").strip().lower()
            estado_bool = True if estado in ["leído", "leido", "si"] else False
            add_book(titulo, autor, genero, estado_bool)
            print(f"Libro '{titulo}' agregado con éxito.")

        elif option == 2:
            book_id = int(input("Introduce el ID del libro que deseas actualizar: "))
            print("Deja en blanco los campos que no desees actualizar.")
            new_titulo = input("Nuevo título: ").strip() or None
            new_autor = input("Nuevo autor: ").strip() or None
            new_genero = input("Nuevo género: ").strip() or None
            new_estado = input("Nuevo estado (leído/no leído): ").strip().lower()
            new_estado_bool = None
            if new_estado:
                new_estado_bool = True if new_estado in ["leído", "leido", "si"] else False
            update_book(book_id, new_titulo, new_autor, new_genero, new_estado_bool)
            print("Libro actualizado con éxito.")

        elif option == 3:
            book_id = int(input("Introduce el ID del libro que deseas eliminar: "))
            del_book(book_id)
            print(f"Libro con ID {book_id} eliminado con éxito.")

        elif option == 4:
            read_book()

        elif option == 5:
            search = input("Introduce el término de búsqueda (título, autor o género): ")
            search_books(search)

        elif option == 6:
            print("Saliendo del programa...")
            break

        else:
            print("Opción no válida, por favor selecciona de nuevo.")

if __name__ == "__main__":
    main()

from sqlalchemy import create_engine, String, Column, Boolean, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Libro(Base):
    __tablename__ = "libros"

    id = Column(Integer, primary_key=True)
    titulo = Column(String, nullable=False)
    autor = Column(String, nullable=False)
    genero = Column(String, nullable=False)
    estado = Column(String, nullable=True)

    def __repr__(self):
        return f'Libro{self.titulo}: id {self.id}, autor {self.autor}, genero {self.genero}, estado {self.estado}'

user = 'abdel25'
password = 'jorgepitty'
host = 'localhost'
port = '3306'
database = 'biblioteca'

url_con = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
engine = create_engine(url_con)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def add_book(titulo, autor, genero, estado):
    nuevo_libro = Libro(titulo=titulo, autor=autor, genero=genero, estado=estado)
    session.add(nuevo_libro)
    session.commit()

# Actualizar libro
def update_book(book_id, new_titulo=None, new_autor=None, new_genero=None, new_estado=None):
    libro = session.query(Libro).filter_by(id=book_id).first()
    if libro:
        if new_titulo:
            libro.titulo = new_titulo
        if new_autor:
            libro.autor = new_autor
        if new_genero:
            libro.genero = new_genero
        if new_estado is not None:
            libro.estado = new_estado
        session.commit()

# Eliminar libro
def del_book(book_id):
    libro = session.query(Libro).filter_by(id=book_id).first()
    if libro:
        session.delete(libro)
        session.commit()

# Mostrar todos los libros
def read_books():
    libros = session.query(Libro).all()
    if libros:
        for libro in libros:
            print(libro)
    else:
        print("No hay libros en la base de datos.")

# Buscar libros por cualquier término
def search_books(search):
    libros = session.query(Libro).filter(
        (Libro.titulo.like(f'%{search}%')) |
        (Libro.autor.like(f'%{search}%')) |
        (Libro.genero.like(f'%{search}%'))
    ).all()
    if libros:
        for libro in libros:
            print(libro)
    else:
        print("Ningún libro coincide con la búsqueda.")

# Menú de opciones
def menu():
    print("\nOpciones:")
    print("1. Agregar libro")
    print("2. Actualizar libro")
    print("3. Eliminar libro")
    print("4. Ver libros existentes")
    print("5. Buscar libro")
    print("6. Salir")
    return int(input("Seleccione una opción: "))

# Ejecución principal
def main():
    while True:
        option = menu()

        if option == 1:
            titulo = input("Introduce el título del libro: ")
            autor = input("Introduce el autor del libro: ")
            genero = input("Introduce el género del libro: ")
            estado = input("Introduce el estado de lectura (leído/no leído): ")
            add_book(titulo, autor, genero, estado)
            print(f"Libro '{titulo}' agregado con éxito.")

        elif option == 2:
            book_id = int(input("Introduce el ID del libro que deseas actualizar: "))
            print("Deja en blanco los campos que no desees actualizar.")
            new_titulo = input("Nuevo título: ").strip() or None
            new_autor = input("Nuevo autor: ").strip() or None
            new_genero = input("Nuevo género: ").strip() or None
            new_estado = input("Nuevo estado (leído/no leído): ").strip() or None

            update_book(book_id, new_titulo, new_autor, new_genero, new_estado)
            print("Libro actualizado con éxito.")

        elif option == 3:
            book_id = int(input("Introduce el ID del libro que deseas eliminar: "))
            del_book(book_id)
            print(f"Libro con ID {book_id} eliminado con éxito.")

        elif option == 4:
            read_books()

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
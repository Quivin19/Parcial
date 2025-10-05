# -*- coding: utf-8 -*-
import csv


# ========== Carga y representación de datos  ==========

def cargar_inventario():
    """
    Carga el inventario de libros desde el archivo CSV.
    
    Returns:
        list: Lista de diccionarios, donde cada diccionario representa un libro
              con todos sus campos convertidos al tipo de dato correspondiente.
              Retorna lista vacía si el archivo no existe.
    """
    lista_libros = []
    
    try:
        
        with open('Inventario.csv', 'r', encoding='utf-8') as archivo:
            # Crear objeto lector CSV
            lector_csv = csv.DictReader(archivo)
            
            for fila in lector_csv:
                # Crear diccionario con tipos de datos correctos
                libro = {
                    'ID': int(fila['ID']),                    # Convertir a entero
                    'Título': fila['Título'],                 # Mantener como texto
                    'Autor': fila['Autor'],                   # Mantener como texto
                    'Año': int(fila['Año']),                  # Convertir a entero
                    'Categoría': fila['Categoría'],           # Mantener como texto
                    'Editorial': fila['Editorial'],           # Mantener como texto
                    'Precio': float(fila['Precio']),          # Convertir a decimal
                    'Cantidad': int(fila['Cantidad'])         # Convertir a entero
                }
                lista_libros.append(libro)
        
        # Imprimir información de los libros cargados
        print("=" * 80)
        print("Inventario de libros cargado desde 'Inventario.csv'")
        print("=" * 80)
        print(f"Total de libros en inventario: {len(lista_libros)}\n")
        
        for libro in lista_libros:
            print(f"ID: {libro['ID']} | {libro['Título']} - {libro['Autor']}")
            print(f"   Año: {libro['Año']} | Categoría: {libro['Categoría']}")
            print(f"   Editorial: {libro['Editorial']} | Precio: ${libro['Precio']:.2f}")
            print(f"   Cantidad disponible: {libro['Cantidad']}")
            print("-" * 80)
        
        return lista_libros
    
    except FileNotFoundError:
        print("Error: El archivo 'Inventario.csv' no fue encontrado.")
        return []
    
    except Exception as error:
        print(f"Error al cargar el inventario: {error}")
        return []


# ========== Operaciones sobre el inventario  ==========

def buscar_libro_por_titulo(lista_libros, titulo_buscar):
    """
    Busca un libro por su título en el inventario (búsqueda case-insensitive).
    
    Args:
        lista_libros (list): Lista de diccionarios con los libros del inventario
        titulo_buscar (str): Título del libro a buscar
    
    Returns:
        dict: Diccionario con la información del libro si se encuentra, None si no existe
    """
    print("\n" + "=" * 80)
    print(f"Buscando libro: '{titulo_buscar}'")
    print("=" * 80)
    
    # Convertir el título a buscar a minúsculas para comparación
    titulo_buscar_lower = titulo_buscar.lower()
    
    # Recorrer todos los libros del inventario
    for libro in lista_libros:
        # Comparar títulos ignorando mayúsculas/minúsculas
        if libro['Título'].lower() == titulo_buscar_lower:
            print("Libro Encontrado:\n")
            print(f"ID: {libro['ID']}")
            print(f"Título: {libro['Título']}")
            print(f"Autor: {libro['Autor']}")
            print(f"Año: {libro['Año']}")
            print(f"Categoría: {libro['Categoría']}")
            print(f"Editorial: {libro['Editorial']}")
            print(f"Precio: ${libro['Precio']:.2f}")
            print(f"Cantidad: {libro['Cantidad']} unidades")
            print("=" * 80)
            return libro
    
    # Si no se encontró el libro
    print("Libro no encontrado en el inventario")
    print("=" * 80)
    return None


def agregar_libro(lista_libros, nuevo_libro):
    """
    Agrega un nuevo libro al inventario si el ID no está repetido.
    Guarda los cambios en el archivo CSV.
    
    Args:
        lista_libros (list): Lista de diccionarios con los libros del inventario
        nuevo_libro (dict): Diccionario con la información del nuevo libro a agregar
    
    Returns:
        bool: True si el libro fue agregado exitosamente, False si el ID ya existe
    """
    print("\n" + "=" * 80)
    print("Intentando agregar nuevo libro al inventario")
    print("=" * 80)
    
    # Verificar si el ID ya existe en el inventario
    for libro in lista_libros:
        if libro['ID'] == nuevo_libro['ID']:
            print(f" Error: Ya existe un libro con el ID {nuevo_libro['ID']}")
            print(f"   Libro existente: '{libro['Título']}' de {libro['Autor']}")
            print("=" * 80)
            return False
    
    # Si el ID no existe, agregar el libro a la lista
    lista_libros.append(nuevo_libro)
    
    # Guardar los cambios en el archivo CSV
    try:
        with open('Inventario.csv', 'w', newline='', encoding='utf-8') as archivo:
            # Definir los nombres de las columnas
            campos = ['ID', 'Título', 'Autor', 'Año', 'Categoría', 'Editorial', 'Precio', 'Cantidad']
            
            # Crear objeto escritor CSV
            escritor_csv = csv.DictWriter(archivo, fieldnames=campos)
            
            # Escribir encabezados
            escritor_csv.writeheader()
            
            # Escribir todos los libros
            escritor_csv.writerows(lista_libros)
        
        print("Libro agregado exitosamente al inventario:")
        print(f"   ID: {nuevo_libro['ID']}")
        print(f"   Título: {nuevo_libro['Título']}")
        print(f"   Autor: {nuevo_libro['Autor']}")
        print(f"   Precio: ${nuevo_libro['Precio']:.2f}")
        print(f"   Cantidad: {nuevo_libro['Cantidad']} unidades")
        print(" Archivo 'Inventario.csv' actualizado correctamente")
        print("=" * 80)
        return True
    
    except Exception as error:
        print(f"Error al guardar el archivo: {error}")
        # Remover el libro de la lista si no se pudo guardar
        lista_libros.remove(nuevo_libro)
        print("=" * 80)
        return False


def libros_por_autor(lista_libros, nombre_autor):
    """
    Busca y muestra todos los libros escritos por un autor específico.
    
    Args:
        lista_libros (list): Lista de diccionarios con los libros del inventario
        nombre_autor (str): Nombre del autor a buscar
    
    Returns:
        list: Lista de libros del autor especificado
    """
    print("\n" + "=" * 80)
    print(f"Linros del autor: '{nombre_autor}'")
    print("=" * 80)
    
    # Convertir nombre del autor a minúsculas para comparación
    nombre_autor_lower = nombre_autor.lower()
    
    # Lista para almacenar los libros encontrados del autor
    libros_encontrados = []
    
    # Buscar todos los libros del autor
    for libro in lista_libros:
        if libro['Autor'].lower() == nombre_autor_lower:
            libros_encontrados.append(libro)
    
    # Mostrar resultados
    if libros_encontrados:
        print(f"Se encontraron {len(libros_encontrados)} libro(s):\n")
        for i, libro in enumerate(libros_encontrados, 1):
            print(f"{i}. {libro['Título']}")
            print(f"   ID: {libro['ID']} | Año: {libro['Año']}")
            print(f"   Categoría: {libro['Categoría']} | Editorial: {libro['Editorial']}")
            print(f"   Precio: ${libro['Precio']:.2f} | Cantidad: {libro['Cantidad']} unidades")
            print("-" * 80)
    else:
        print(f"No se encontraron libros del autor '{nombre_autor}'")
    
    print("=" * 80)
    return libros_encontrados


# ========== Función principal y pruebas ==========

def menu_principal():
    """
    Función principal que ejecuta el sistema de gestión de inventario.
    Muestra un menú interactivo para probar todas las funcionalidades.
    """
    print("\n")
    print("*" * 80)
    print("*" + " " * 78 + "*")
    print("*" + " " * 20 + "Sistema de gestión de Inventario" + " " * 25 + "*")
    print("*" + " " * 30 + "Librería" + " " * 41 + "*")
    print("*" + " " * 78 + "*")
    print("*" * 80)
    print()
    
    # Cargar el inventario desde el archivo
    inventario = cargar_inventario()
    
    if not inventario:
        print("\n No se pudo cargar el inventario. Verifique que el archivo existe.")
        return
    
    # Menú interactivo
    while True:
        print("\n" + "=" * 80)
        print("Menú de opciones")
        print("=" * 80)
        print("1. Buscar libro por título")
        print("2. Agregar nuevo libro")
        print("3. Buscar libros por autor")
        print("4. Mostrar inventario completo")
        print("5. Salir")
        print("=" * 80)
        
        opcion = input("\nSeleccione una opción (1-5): ").strip()
        
        if opcion == '1':
            # Buscar libro por título
            titulo = input("\nIngrese el título del libro a buscar: ").strip()
            buscar_libro_por_titulo(inventario, titulo)
        
        elif opcion == '2':
            # Agregar nuevo libro
            print("\n--- Agregar nuevo Libro ---")
            try:
                nuevo = {
                    'ID': int(input("ID del libro: ")),
                    'Título': input("Título: ").strip(),
                    'Autor': input("Autor: ").strip(),
                    'Año': int(input("Año de publicación: ")),
                    'Categoría': input("Categoría: ").strip(),
                    'Editorial': input("Editorial: ").strip(),
                    'Precio': float(input("Precio: ")),
                    'Cantidad': int(input("Cantidad: "))
                }
                agregar_libro(inventario, nuevo)
            except ValueError:
                print("\nERROR: Datos inválidos. Verifique los valores numéricos.")
        
        elif opcion == '3':
            # Buscar libros por autor
            autor = input("\nIngrese el nombre del autor: ").strip()
            libros_por_autor(inventario, autor)
        
        elif opcion == '4':
            # Mostrar inventario completo
            print("\n" + "=" * 80)
            print("Inventario completo de libros")
            print("=" * 80)
            for libro in inventario:
                print(f"ID: {libro['ID']} | {libro['Título']} - {libro['Autor']}")
                print(f"   Precio: ${libro['Precio']:.2f} | Cantidad: {libro['Cantidad']}")
                print("-" * 80)
        
        elif opcion == '5':
            # Salir del programa
            print("\n" + "=" * 80)
            print("Gracias por usar el Sistema de Gestión de Inventario")
            print("=" * 80)
            break
        
        else:
            print("\n Opción inválida. Por favor seleccione una opción del 1 al 5.")


# ========== Ejecución del programa ==========

if __name__ == "__main__":
    # Ejecutar el menú principal
    menu_principal()
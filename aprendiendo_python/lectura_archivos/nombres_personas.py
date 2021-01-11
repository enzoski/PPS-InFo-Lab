# Programa en el cual le pedire al usuario que ingrese nombres de personas para guardarlas en un archivo de texto.

nombre_archivo = "personas.txt"

with open(nombre_archivo, 'w') as arch:
    condicion = True
    while condicion:
        nombre = input("Ingresa el nombre de una persona ('s' para salir): ")
        if nombre.lower() == 's':
            condicion = False
        else:
            arch.write(f"{nombre.title()}\n")

print("Archivo generado!")

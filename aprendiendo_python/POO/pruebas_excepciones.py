# EXCEPCIONES
#
# Cuando ocurre un error durante la ejecucion de un programa que no puede ser manejado por Python, se crea un objeto 'exception',
# se detiene la ejecucion del programa y se muestra el 'traceback' (que nos indica qué excepción lanzó Python y una descripcion del error).
#
# Pero es posible manjear las excepciones que se lanzan mendiante bloques 'try-except', donde se intenta ejecutar código y en caso de que
# se lance alguna excepcion, le diremos a Python qué debe hacer (en vez de detener el programa, sigue con la ejecución).

try:
    print(7/4)
    print(5/0)
    print(4/4)
except ZeroDivisionError: #exception object
    print("You can't divide by zero!")
else:
    print("aca solo se entra si se ejecuta todo el bloque 'try' exitosamente.")

print("Continuando con la ejecución del programa...")

# Si en el código dentro del 'try' se lanza alguna excepcion, deja de ejecutarse lo que quede en el 'try' y se buscará algun bloque 'except'
# que matchee con la excepcion lanzada y se ejecutará ese bloque. Si no hay ningun catch de esa excepcion, Python sí detendra la ejecución.
# Tanto como si se ejecuta todo el 'try' sin problemas como si entra a algun bloque 'except', luego se seguirá ejecutando nuestro programa
# con lo que haya debajo de todo el 'try-except'. Adicionalmente podemos agregar el bloque 'else' que solo se ejecuta si el bloque 'try' se
# ejecutó correctamente, sin lanzar excepciones.

try:
    print(1/4)
except ZeroDivisionError: #exception object
    print("You can't divide by zero!")
else:
    print("aca solo se entra si se ejecuta todo el bloque 'try' exitosamente.")

print("Continuando con la ejecución del programa...")

# ------------------------------
# MANEJANDO ERRORES DE ARCHIVOS
#
# Leer un archivo inexistente.

filename = 'alice.txt'
try:
    with open(filename, encoding='utf-8') as f: #como no aclaramos el modo, por defecto será 'r' (lectura)
        contents = f.read()
except FileNotFoundError:
    print(f"El archivo '{filename}' no se encuentra en el sistema.")

# The encoding argument: this argument is needed when your system’s default encoding doesn’t match the encoding of the file
# that’s being read."

# Ejemplo contador de palabras.
#------------------------------
def count_words(filename):
    """Count the approximate number of words in a file."""
    try:
        with open(filename, encoding='utf-8') as f:
            contents = f.read()
    except FileNotFoundError:
        print(f"Sorry, the file '{filename}' does not exist.") # si quisieramos no hacer nada frente a un error, ponemos 'pass'.*
    else:
        words = contents.split()
        num_words = len(words)
        print(f"The file '{filename}' has about {num_words} words.")

filenames = ['alice.txt', 'siddhartha.txt', 'palabras.txt', 'moby_dick.txt', 'little_women.txt'] # https://www.gutenberg.org/
for filename in filenames:
    count_words(filename)
#------------------------------
# * con la sentencia 'pass' Python interpreta que no debe hacer nada en el bloque que esté escrito (try, except o else), y saldrá de él,
# siguiendo con la ejecución del programa. Sirve mas que nada como una justificación de que vos realmente decidiste no hacer nada en
# cierto bloque de código (ya que sería lo mismo que dejarlo en blanco). O también puede servir como un recordatorio para implementar
# algo luego.
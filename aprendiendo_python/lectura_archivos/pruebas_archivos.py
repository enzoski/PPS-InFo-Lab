# ARCHIVOS
# --------
#
# LEYENDO ARCHIVOS DE TEXTO (sobre binarios no dice nada, pero será parecido cambiando la extension .txt por .bin, .dat, etc...)
#
# "Reading from a file is particularly useful in data analysis applications, but it’s also applicable to any situation in which you want to
# analyze or modify information stored in a file."
#
# "When you want to work with the information in a text file, the first step is to read the file into memory. You can read the entire
# contents of a file, or you can work through the file one line at a time."
#
# -----------------------------
# LEER LA TOTALIDAD DEL ARCHIVO

with open('pi_digits.txt') as file_object:
    contents = file_object.read() #este read devuelve un gran string con la totalidad del archivo de texto.
print(contents) #si se muestra una linea en blanco extra, es debido a que cuando el read() llega al final del archivo, devuelve eso.

# open(): para empezar a manipular un archivo, siempre primero debemos abrirlo para acceder a él. Esta funcion requiere un solo argumento:
#         el nombre del archivo de texto que queremos abrir (debe estar en el mismo directorio que nuestro programa).
#         Esta funcion devuelve un objeto que representa al archivo, y se guarda en la variable 'file_object' (puede tener otro nombre).
#         Esta variable la usaremos para acceder a las funciones que manipulan archivos (pero solo tenemos acceso a este objeto del archivo
#         dentro del bloque 'with', una vez que salgamos no podremos usar más la variable).
# close(): Podriamos escribir explicitamente la funcion close(), para cerrar el archivo luego de haber terminado de utilizarlo (para no
#          tener una posible corrupcion de los datos). Pero esto lo hace automaticamente Python cuando termina el bloque de código del
#          'with', o sea, en este ejemplo, luego de ejecutar "contents = file_object.read()", como ahi termina el bloque de código,
#          cierra el archivo.

# Nota: si quisieramos abrir un archivo que no está en el directorio actual, podemos indicarle a open() la ruta al archivo en nuestro
#       sistema. Podemos tanto poner el path completo (absoluto), como el path relativo (a partir de la carpeta que estamos, vamos
#       escribiendo la ruta, como algo así: "text_files/filename.txt", donde dentro de la carpeta actual [que no se escribe], tenemos otra
#       donde ahí se encuentra el archivo.).
#       
# Nota2: "Windows systems use a backslash (\) instead of a forward slash (/) when displaying file paths, but you can still use
#        forward slashes in your code."
#
# Nota3: "If you try to use backslashes in a file path, you’ll get an error because the backslash is used to escape characters in strings.
#         For example, in the path "C:\path\to\file.txt", the sequence \t is interpreted as a tab. If you need to use backslashes,
#         you can escape each one in the path, like this: "C:\\path\\to\\file.txt"."
#
# Nota4: Cuando se lee de un archivo de texto, Python siempre lo interpreta como strings. Si queremos leer números para luego hacer
#        operaciones numéricas, tendremos que aplicar a los strings que vamos leyendo la funcion 'int()' o 'float()' para convertirlos.

print("")

# -----------------------------
# LEER LINEA A LINEA UN ARCHIVO
#
# Esto en Python se hace con un ciclo for. El ciclo mismo detecta el end of file.

filename = 'pi_digits.txt' #esta bueno poner el nombre del archivo en una variable, asi en cualquier momento podemos asignarle otro archivo
                           #sin necesidad de estar cambiando el string en cada posible 'open()'.
with open(filename) as file_object:
    for line in file_object:
        print(line.rstrip())

# Nota: el método 'rstrip()' elimina los espacios en blanco o saltos de linea a la derecha de un string. Esto lo hacemos en este caso para
#       evitar ver por consola un salto de linea extra, ya que cada linea del archivo de texto de por sí tienen un salto de linea al final,
#       y ademas la funcion 'print()' agrega un salto de linea, entonces veríamos 2 saltos de linea, y no es lo que tiene el archivo.

print("")

# -----------------------------
# HACER UNA LISTA CON LAS LINEAS DE UN ARCHIVO
#
# En Python podemos directamente almacenar cada linea de un archivo dentro de una lista, para luego poder usarla.

filename = 'pi_digits.txt'

with open(filename) as file_object:
    lines = file_object.readlines() #este método arma una lista donde cada elemento se corresponde con cada línea del archivo.

for line in lines:
    print(line.rstrip())

print(lines)

# -------curiosidad jeje -------------------------

'''filename = 'pi_million_digits.txt'

with open(filename) as file_object:
    lines = file_object.readlines() #este método arma una lista donde cada elemento se corresponde con cada línea del archivo.

pi_string = ""
for line in lines:
    pi_string += line.strip()

birthday = input("Enter your birthday, in the form mmddyy: ")
if birthday in pi_string:
    print("Your birthday appears in the first million digits of pi!")
else:
    print("Your birthday does not appear in the first million digits of pi.")'''

# --------------------------------
#
# ESCRIBIENDO EN ARCHIVOS DE TEXTO
#
# Para escribir en un archivo, primero hay que decirle a Python que queremos abrir el archivo en modo escritura ('w').
# Hay 4 modos para abrir un archivo:  lectura ('r'), escritura ('w'), append ('a') y lectura-escritura ('r+').
# Esto se pone como 2do argumento de la funcion 'open()', pero si lo omitimos, por defecto lo abrirá en modo lectura (como vimos antes).

filename = 'programming.txt'
with open(filename, 'w') as file_object:
    file_object.write("I love programming.\n") #con este método escribimos en un archivo.
    file_object.write("I love creating new games.\n") #como no agrega saltos de linea extra, debemos escribirlos nosotros si los queremos.

# Nota1: Si el archivo que queremos escribir no existe, se crea en nuestro sistema. Pero si ya existe, lo sobreescribe... ojo...
# Nota2: Solo podemos escribir strings en el archivo, por lo que si queremos escribir algun tipo numerico, primero debemos convertirlo
#        a un string mediante la función 'str()'.

with open(filename, 'a') as file_object:
    file_object.write("I also love finding meaning in large datasets.\n")
    file_object.write("I love creating apps that can run in a browser.")

# Con 'append' abrimos el archivo sin sobreescribir lo que tenga, y lo que escribamos se guardará al final del archivo.
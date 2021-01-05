#NOTA: no se ponen ';' al final de cada sentencia/linea.
#--------------------------------------------------------

# USO DE VARIABLES
# (los tipos se asignan dinamicamente, no hay que declararlos,
# podemos cambiarle sus valores por cualquier tipo de valor en cualquier momento)

# Strings
mensaje = "Que ondaaa"
print(mensaje)

mensaje = "Hello Python Crash Course world!"
print(mensaje)

nombre = "enzo barria"
print(nombre)
print(nombre.title()) #métodos de los strings (hay bastantes muy interesantes, como borrar espacios de los costados)
print(nombre.upper()) #todo en mayus
print(nombre.lower()) #todo en minus

first_name = "ada"
last_name = "lovelace"
full_name = f"{first_name} {last_name}"
print(f"Hello, {full_name.title()}!") #darle formato a un string. Incluimos variables "{var}" en strings.

mensaje2 = "Languages:\n\tPython\n\tC\n\tJavaScript" #uso de "Whitespace's"
print(mensaje2)

texto1 = "hola, cómo estas "
texto2 = "wachin?"
texto2 += " todo piola??" #texto2 = texto2 + "..."
print(texto1 + texto2) #concatenación de strings. (si queremos concatenar otros tipos, fijarse el .html que dejé en "extras")

# Enteros
x = 5
y = 2
print(x+y)
print(x-y)
print(x*y)
print(x/y)
print(4/2) # When you divide any two numbers, even if they are integers, you’ll always get a float.
print(4//2) #division entera
print(x**y) #potencia
print(x%y) #modulo/resto

# Reales
x = 1.5
y = 2.3
print(x + y)

# Booleanos
condicion_1 = True
condicion_2 = False

#---------------

# CONSTANTES
# No hay un tipo predefinido de 'constante', o una forma especial de tratarlas por parte de Python.
# Pero por convencion, si queremos declarar una constante, se hace igual que una variable pero su nombre es todo en mayusculas.
# Y nosotros como programadores debemos respetar no cambiarle el valor a dicha constante
# (ya que como dije, Python no controla esto porque no están implementadas las constantes)
variable = 10
CONSTANTE = 10
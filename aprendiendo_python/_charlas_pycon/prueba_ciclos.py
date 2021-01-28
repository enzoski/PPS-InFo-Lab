# Charla de Ned Batchelder: Loop like a native
# ---------------------
# Todo objeto que sea 'iterable', lo vamos a poder meter en un 'for', e iterar/loopear sobre él.
"""
for name in iterable:
    statements
"""
# ---------------------

# os.walk('/some/dir'): funcion que le dice al sistema operativo que nos devuelva los directorios y archivos que hay en un directorio.
#                       Esto se repite para cada subdirectorio que haya.

import os

ruta = "C:\\Users\\Enzo\\Desktop\\python_projects\\charlas_pycon\\Ned Batchelder"
# pongo doble \ para que lo interprete como tal (una sola). Sino se confunde con los \n, \t, etc...

for root, dirs, files in os.walk(ruta):
    print("---")
    print(root)
    print(dirs)
    print(files)

# ------------------------------------------------------------------------------------
print("\n")
# ------------------------------------------------------------------------------------

# enumerate(iterable): funcion que dada una lista, diccionario, etc, devuelve una lista de tuplas de la forma (indice, valor)

lista = ["hola", "como", "estas"]
print(list(enumerate(lista)))
# realmente es como que enumerate devuelve un objeto (al igual que 'range()' y otros mas), por eso si lo queremos mostrar por pantalla
# hay que convertirlo a una lista. Pero cuando lo usamos en un for, directamente se itera sobre ese objeto.

for i in enumerate(lista):
    print(i)

print(type(i))

for i, v in enumerate(lista):
    print(i, v)

print("")
with open("prueba.txt") as f:
    for linenum, line in enumerate(f, start=1):
        print(linenum, line.rstrip())

print(type(linenum))

# ------------------------------------------------------------------------------------
print("\n")
# ------------------------------------------------------------------------------------

# zip(lista1, lista2): produce una lista de tuplas con pares donde los elementos de la lista1 seran las 'keys' y los de la 2 los 'value'.

planetas = ["jupiter", "marte", "neptuno"]
colores = ["marron", "rojo", "azul"]

print(list(zip(planetas, colores)))

for i in zip(planetas, colores):
    print(i)

print(type(i))

for i, v in zip(planetas, colores):
    print(i, v)

print("")
#tambien podemos convertir el 'zip()' a un diccionario (o cualquier 'stream' de pares, como lo que devuelve 'enumerate()')
print(dict(zip(planetas, colores)))

# ------------------------------------------------------------------------------------
print("\n")
# ------------------------------------------------------------------------------------

# Generadores ('generator')
#
# Se definen como las funciones, pero en vez de devolver un unico valor, devuelven un 'stream' de valores, el cual es 'iterable'
# (puede usarse en un 'for', ya que el 'stream' es un 'iterator'). Se usa la palabra clave 'yield' para devolver valores.

def generador_1():
    yield 1
    yield 2
    yield 3

def generador_2():
    for i in range(1, 4):
        yield i

def generador_3(lista):
    for num in lista:
        if num % 2 == 0:
            yield num


print("GENERATOR_1:")
x = generador_1()
y = generador_1()
print(list(x)) # Si queremos ver el resultado, tenemos que convertirlo a por ejemplo una lista.
print(tuple(y)) # al parecer se puede llamar varias veces al generador y sigue generando sus valores.
# (creo que no es que los vuelva a generar, sino que se queda con los valores del primer llamado)
# (creo que es porque los generators son 'lazy')

print(x,y)
# EDIT: acá lo que pasa es que estamos recibiendo diferentes referencias de iteradores. Por lo cual podemos generar individualmente
#       los valores. Lo que no se puede es volver a generar valores una vez que hayamos generado todos los posibles de un mismo iterador.
#       Los valores se van generando con la funcion 'next(object)'. Cuando generemos todos no podremos hacer mas next, ni volver pa'tras.

numeros = generador_1()
print(next(numeros))
print(list(numeros))
# print(next(numeros)) -> esto tira error porque la funcion list(x) consumió todos los 'next'.

print("GENERATOR_2:")
z = generador_2()
print(list(z))

print("GENERATOR_3:")
w = generador_3([1, 2, 3, 4, 5])
print(list(w))

# Vemos que podemos iterar directamente sobre un 'generator'. Si hubieramos hecho una funcion, dentro de ella tendriamos que retornar
# un objeto 'iterable', como una lista. O sea, tendriamos que armar una lista (usando appends por ejemplo) y retornarla.
for par in generador_3([1, 2, 3, 4, 5]):
    print(f"Este es un número par: {par}")

g = generador_3([1, 2])
for par in g:
    print(f"Este es un número par V2: {par}")
for par in g:
    print(f"Acá no va a entrar porque en el for anterior ya se generaron todos los pares: {par}")

# ---
# Que fuerte jaja, tambien podemos devolver varios elementos a la vez, y los agrupa en una tupla. (vi que una funcion tmb puede :o)
# O sea que por ejemplo el 'enumerate' que vimos antes, quizas haga algo de esto, quizas sea un 'generator'.
def generador_4():
    yield 1, 2, 3

print(list(generador_4()))

for x in generador_4():
    print(x)

print(type(x))

# ------------------------------------------------------------------------------------
print("\n")
# ------------------------------------------------------------------------------------

# Objetos "iterable's"
#
# Nosotros podemos definir que los objetos de nuestras propias clases sean 'iterables'.
# Para que un objeto sea 'iterable', debe estar definido el método '__iter__(self)' en la clase.
# Y para que pueda ser iterado en un for, el objeto debe devolver un 'iterator'. El iterator es lo que devuelve el método iter.

class Libro:
    """docstring for Libro"""
    def __init__(self, lista_paginas):
        self.lista_paginas = lista_paginas

    def __iter__(self):
        """iterator por defecto al querer iterar sobre un objeto tipo Libro."""
        return iter(self.lista_paginas) # devuelvo el iterator de la lista que tenemos como atributo de clase.

    def paginas_pares(self):
        """iterator que devuelve este método para iterar solo sobre las páginas pares de un objeto tipo Libro."""
        return (contenido for pagina, contenido in enumerate(self.lista_paginas, start=1) if pagina % 2 == 0)
        # esto es una 'expresion generator'. Un generador devuelve un iterator, por eso esto es válido. (dejo un .jpg de la sintaxis)
        # combiné el uso de 'enumerate'.

    def paginas_impares(self):
        """iterator que devuelve este método para iterar solo sobre las páginas impares de un objeto tipo Libro."""
        return (contenido for pagina, contenido in enumerate(self.lista_paginas, start=1) if pagina % 2 != 0)

paginas_libro = ["Página 1. Acá comienza todo...", "Página 2. Y acá continua...", "Página 3. Y acá finaliza..."]

libro_1 = Libro(paginas_libro)

for pagina in libro_1:
    print(pagina)

print("")

#creo que internamente el for recibe el iterator, y le va haciendo 'next()' hasta que no haya mas elementos (parecido a Java).
#y cada vez que hace un 'next()', quizas recien ahi se produce un return del valor, queda el for del generator en stand-by,
#y luego sigue en el proximo '.next()'.
for pagina_par in libro_1.paginas_pares():
    print(pagina_par)

print("")

for pagina_impar in libro_1.paginas_impares():
    print(pagina_impar)

# --------------------------------------------
print("")
lista1 = [1,2,3]
iterador_lista1 = lista1.__iter__()
print(iterador_lista1)

for x in iterador_lista1:
    print(f"for_1: {x}")
for x in iterador_lista1:#en este no itera porque ya se hicieron todos los next en el for anterior.
    print(f"for_2: {x}")
for x in lista1:#acá sí, se ve que al iterar directo sobre la lista, el iterador es distinto o algo.
    print(x)
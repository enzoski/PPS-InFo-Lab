# JSON
#
# "The JSON (JavaScript Object Notation) format was originally developed for JavaScript. However, it has since become a common format
# used by many languages, including Python." (podemos almacenar datos en un .json desde Python, y por.ej. un programa en Java lo podrá leer)
#
# JSON es un formato de texto sencillo para el intercambio de datos. Es un formato estandarizado el cual muchos lenguajes de programacion
# saben manejar. Es un archivo de texto (legible por nosotros) donde almacenaremos datos de una manera especial (usando la sintaxis de JSON).
#  -> arreglos: [value1, value2, ...] ;
#  -> objetos: {key1:value1, key2:value2, ...} (las 'key' siempre deben ser strings entre comillas dobles) ;
#  -> valores: números, strings, true, false, null, arreglos u objetos.
# En los archivos .json podemos dejar tantos espacios y saltos de linea como queramos. Por otro lado, no se pueden escribir comentarios.
# Un documento JSON está formado por un gran elemento (un objeto o una matriz que contiene/encierra a todos los demás elementos).

# JSON en Python
# Python tiene un módulo en su libreria estandar llamado 'json' en el cual están implementadas las funciones para trabajar con JSON.

#------------------------
# GENERANDO ARCHIVOS JSON
# -----------------------

import json #importamos la libreria json

numbers = [2, 3, 5, 7, 11, 13] #creamos una lista la cual guardaremos en el archivo json (conservando el tipo de dato lista)

filename = 'numbers.json' #este será el nombre del archivo; la extension debe ser '.json'
with open(filename, 'w') as f: #abrimos comunmente el archivo en modo escritura ('w'). Por convención se pone 'f' como objeto del archivo.
    json.dump(numbers, f)

# La función 'dump()' guarda un lote de datos suministrado en el primer argumento, en el archivo pasado como segundo argumento (le debemos
# pasar el objeto que representa al archivo). La funcion se encargará de que se guarde en el formato JSON.


# -----------------------
# LEYENDO UN ARCHIVO JSON
# -----------------------

import json

filename = 'numbers.json'
with open(filename) as f:
    numbers_2 = json.load(f)

print(numbers_2)
print(type(numbers_2)) #para ver que realmente recuperamos el tipo 'lista' que habiamos guardado antes.

# La funcion 'load()' carga en memoria el contenido del archivo .json pasado como argumento (arg. tipo objeto). Luego retorna los datos
# leidos y se los asignamos a una variable.

#----------------------------------------------------------------------------------------------------------------------------------------
# ACLARACIÓN: como los archivos JSON se componen de una gran arreglo ([]) o un gran objeto ({}) que encierran todo lo demás, siempre que
#             queramos escribir o leer un archivo .json, guardaremos o recuperaremos Listas o Diccionarios, que son los equivalentes en
#             Python a los Arreglos y Objetos de JSON respectivamente. (generalmente debería ser así)
#----------------------------------------------------------------------------------------------------------------------------------------
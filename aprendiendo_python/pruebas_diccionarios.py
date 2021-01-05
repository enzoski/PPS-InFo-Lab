# Estructura de Datos: DICCIONARIOS
# ---------------------------------
# Los diccionarios son colecciones de pares clave-valor (como un hash-map de java)
# Cada clave está asociada a un valor, y a dicho valor se accede mediante su clave.
# Un diccionario puede tener tantos pares como quiera, y tanto la clave como el valor pueden ser de cualquier tipo de datos.
# (incluso listas u otros diccionarios) (tambien podemos armar listas de diccionarios)

alien_0 = {'color': 'green', 'points': 5}

print(alien_0['color']) #obtener el valor de una clave (si no existe la clave, se produce un error y se para la ejecución)
print(alien_0['points'])

print(alien_0.get("color")) #obtener el valor de una clave, mediante el método '.get' (que evita errores de KeyError)
print(alien_0.get("idioma")) #si no se encuentra la clave, por defecto devuelve 'None' (que sería como un 'null')
print(alien_0.get("idioma","Clave 'idioma' no encontrada")) #tambien le podemos poner un mensaje de error.

alien_0["x_pos"] = 0 #agregar un nuevo par clave-valor.
alien_0["y_pos"] = 25

print(alien_0)

alien_0['color'] = "azul" #cambiar el valor asociado a una clave.

print(alien_0)

# NOTA: basicamente la sintaxis para agregar un nuevo par como para modificar un valor, es la misma:
# si la clave existe en el diccionario, cambia su valor, sino, crea dicha clave y le asocia el valor.

del alien_0["points"] #eliminar un par clave-valor del diccionario.

print(alien_0)

# ------------------------------------

# Tambien podemos ver a un diccionario como la definicion de atributos de un objeto (el concepto de POO)
alien_1 = {"color": "verde",
           "puntuacion": 7,
           "x_pos": 0,
           "y_pos": 4}

print(f"Información alien_1: {alien_1}")

# O como la representacion de informacion sobre varios objetos
favorite_languages = {
	'jen': 'python',
	'sarah': 'c',
	'edward': 'ruby',
	'phil': 'python',
	}
# Nota: así sería la convencion de escritura de un diccionario en varias lineas, incluyendo la coma final,
# para dar pie a que se puede seguir agregando pares clave-valor.
print(f"Información sobre lenguajes de programación favoritos: {favorite_languages}")

# -------------------------------------------

# Listas de diccionarios

persona1 = {"nombre": "Enzo", "edad": 22}
persona2 = {"nombre": "Franco", "edad": 22}
persona3 = {"nombre": "CR7", "edad": 35}

personas = [persona1, persona2, persona3]

print(personas)


# Diccionarios dentro de otros diccionarios.

users = {
    'aeinstein': {
        'first': 'albert',
        'last': 'einstein',
        'location': 'princeton',
        },

    'ntesla': {
        'first': 'nikola',
        'last': 'tesla',
        'location': 'nueva york',
        },

    }

print(users)
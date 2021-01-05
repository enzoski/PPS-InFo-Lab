# CICLO 'for' (es como un for-each)
# Podremos recorrer toda la lista (sin necesitar conocer su longitud) e ir guardando cada elemento en una variable.
# for variable in lista:
magos = ["Harry", "Ron", "Hermione"]
for nombre in magos:
	print(nombre)
	print(f"Sos gros@ {nombre}!\n")
print("Terminamos de recorrer la lista de magos :)\n")

#NOTA: no se usan llaves para encerrar el bloque de codigo que se va a repetir,
#eso se marca/detecta directamente con la tabulación, por lo que hay que tener una correcta indentación.

#Nota2: la variable del for mantiene su ultimo valor asignado luego de terminar el ciclo, por lo que lo podemos utilizar.

#----------------------------------------------------

#CICLO 'for' convencional (repite desde x hasta y-1)
for i in range(1,5): #de 1 a 4
	print(i)
#NOTA: cuando llega al ultimo valor, el ciclo se detiene y no lo almacena en la variable 'i'.

for y in range(5): #de 0 a 4
	print(y)

#----------------------------------------------------

#TUPLAS (Listas constantes. Solo se pueden modificar sus valores si redefinimos la tupla completa, osea le asignamos una nueva tupla)
comidas_restaurante = ("milanesa con papas", "hamburguesa", "pancho", "pizza")
print("Las comidas disponibles en el restaurante son:")
for comida in comidas_restaurante:
	print(comida)
print("Oh, hubo un cambio en el menú. Ahora es:")
comidas_restaurante = ("milanesa con puré", "hamburguesa", "nuggets", "pizza")
for comida in comidas_restaurante:
	print(comida)

print("")

#----------------------------------------------------
# DICCIONARIOS (parecidos a las listas pero almacenan pares clave-valor)
#
# Podemos loopear por todo el diccionario (pares clave-valor), solo por las claves, o solo por los valores.

traductor = {
	"hola": "hi",
	"adios": "bye",
	"auto": "car",
	"sol": "sun",
	}

# Loopear por todo el diccionario
for key, value in traductor.items():
	print(f"Clave: {key}\nValor: {value}\n")
# ".items() returns a list of key-value pairs. The for loop then assigns each of these pairs to the two variables provided."
# (podemos llamar a las variables como queramos, no necesariamente "key" y "value")

# Loopear por las claves
for key in traductor.keys():
	print(f"Clave: {key}")
# "Looping through the keys is actually the default behavior when looping through a dictionary,
# so this code would have exactly the same output if you wrote: 'for key in traductor:' " (podemos usar el que nos resulte mas claro)
# .keys() devuelve una lista con todas las claves del diccionario.
if "moto" not in traductor.keys():
	print("No se encuentra la traducción de 'moto'.")
# Tambien podemos ordenar las claves temporalmente y loopear por ellas.
claves_ordenadas = sorted(traductor.keys())
for clave in claves_ordenadas:
	print(clave)
print(traductor)

# Loopear por los valores
for value in traductor.values():
	print(f"Valor: {value}")
# Generalmente las claves son unicas en los diccionarios, pero en cambio los valores podrían repetirse.
# Para loopear sobre los valores sin que haya repetidos, debemos usar la funcion 'set',
# que dada una lista, crea una coleccion de elementos no repetidos. (internamente un set es: s = {valor1, valor2, ..., valorN})
print("")
valores_unicos = set(traductor.values()) #el orden de los valores puede variar.
for valor in valores_unicos:
	print(f"Valor: {valor}")
# "Unlike lists and dictionaries, sets do not retain items in any specific order."
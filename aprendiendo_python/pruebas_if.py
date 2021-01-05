# CONDICIONAL IF
# --------------
# Al igual que el ciclo for, no se usan llaves, se indica el bloque de ejecucion con tabulaciones.
# Tampoco se requieren parentesis para indicar el inicio y fin de la condición (son opcionales).
# Y los 'else' se ponen justo debajo del bloque del 'if' y se le agregan los ":" al final.
# 
# Vemos que todo se estructura mediante las tabulaciones
# (que en realidad deben ser espacios para evitar algun conflicto en el interprete, pero eso viene preconfigurado en sublime text)

autos = ["alfa romeo", "bmw", "chevrolet","vw"] #se pueden comparar "alegremente" los strings je
for auto in autos:
	if auto == "bmw" or auto == "vw":
		print(auto.upper()) #todo mayus
	else:
		print(auto.title()) #solo la primera letra de cada palabra del string en mayus

# Python uses the values 'True' and 'False' to decide whether the code in an if statement should be executed.
# O sea, los valores booleanos se representan con True y False.

# COMPARACIONES
#
# Operadores relacionales:
# ---
# Igualdad:  ==
# Distintos: !=
# Mayor que: >
# Mayor o igual que: >=
# Menor que: <
# Menor o igual que: <=
#
# Operadores lógicos
# ---
# Y: and
# Ó: or
# NO: not
#
# Si queremos podemos usar parentesis para cambiar el orden de evaluación de una expresión.
# Cualquier cosa fijemonos en la Precedencia de Operadores de Python.

# ---
# Tambien hay operadores especiales:
# in: verifica si en una lista se encuentra un determinado valor.
# not in: verifica si en una lista no se encuentra un determinado valor.
nombres = ["enzo", "franco", "ale"]
x = "alfred"
if x in nombres:
	print(f"{x} se encuentra en la lista!")
else:
	print(f"{x} NO se encuentra en la lista!")

# Sentencia 'elif' (para cuando tenemos muchos if-else, asi nos evitamos escribir varios 'niveles' de más)
edad = 22
if edad < 5:
	precio = "Gratis"
elif edad < 10:
	precio = 100
elif edad < 15:
	precio = 200
else:
	precio = 300
print(f"Precio de entrada al museo: ${precio}")
# "The only recommendation PEP 8 provides for styling conditional tests is to use a single space around comparison operators"
# "if age < 4:" is better than: "if age<4:"

# prueba de lista vacia.
lista = []
if lista == []:
	print("La lista está vacía!!!")
else:
	print("La lista no está vacía.")

#prueba numeros ordinales
numeros_ordinales = list(range(1,10)) #creo una lista con los numeros del 1 al 9.
for numero in numeros_ordinales:
	if numero == 1:
		ordinal = "st"
	elif numero == 2:
		ordinal = "nd"
	elif numero == 3:
		ordinal = "rd"
	else:
		ordinal = "th"
	print(f"{numero}{ordinal}")
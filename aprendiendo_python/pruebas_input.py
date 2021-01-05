# PROGRAMAS INTERACTIVOS
#
# Veremos cómo pedirle a un usuario que introduzca datos en el programa, mediante la funcion 'input()'
# " The input() function pauses your program and waits for the user to enter some text.
# Once Python receives the user’s input, it assigns that input to a variable."

#Como argumento del input() podemos poner instrucciones para el usuario, es como un print de un mensaje para que sepa qué debe ingresar.
entrada = input("Ingresa un texto y lo mostraré por pantalla: ")
print(entrada)

#Si queremos armar mensajes largos, podemos armarlos en una variable y despues pasarla como parámetro al 'input()'
indicaciones = "Hola bro, necesito saber tu nombre para fines meramente educativos.\n"
indicaciones += "Por favor, ingresá tu nombre ahora: "
entrada = input(indicaciones)
print(f"Gracias, {entrada}!")

# NOTA: generalmente los editores de codigo no soportan la entrada de datos, por lo que hay que ejecutar el programa en la consola (cmd).

# Para ingresar números, tendremos que hacer un 'cast' (siempre que luego queramos operar con esos numeros),
# ya que el 'input()' siempre interpreta que lo que ingresa un usuario es un string.
# Para esto usaremos la funcion 'int()': "The int() function converts a string representation of a number to a numerical representation"
height = input("How tall are you, in inches? ")
height = int(height)
if height >= 48:
	print("\nYou're tall enough to ride!")
else:
	print("\nYou'll be able to ride when you're a little older.")

# Ejemplo números pares e impares (utilizando el operador módulo '%')
number = input("Enter a number, and I'll tell you if it's even or odd: ")
number = int(number)
if number % 2 == 0:
	print(f"\nThe number {number} is even.")
else:
	print(f"\nThe number {number} is odd.")
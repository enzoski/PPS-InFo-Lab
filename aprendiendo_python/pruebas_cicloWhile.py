# Ciclo while
#
# Es como lo vimos en otros lenguajes, pero sin necesidad de colocarle parentesis a la condición.
i = 1
while i <= 5:
	print(i)
	i = i + 1

# Combinandolo con un input
prompt = "\nTell me something, and I will repeat it back to you:"
prompt += "\nEnter 'quit' to end the program. "
message = "" #inicializamos la variable para que el while pueda compararla.
while message != 'quit':
	message = input(prompt)
	if message != 'quit':
		print(message)

# Usando 'flags' (en vez de hacer la comprobación en la condicion del while, la hacemos en otra parte del codigo,
# y seteamos la bandera en False si corresponde parar la ejecucion. Esto es util cuando tenemos varias condiciones que provoquen parar)
prompt = "\nTell me something, and I will repeat it back to you:"
prompt += "\nEnter 'quit' to end the program. "
active = True
while active:
	message = input(prompt)
	if message.lower() == 'quit':
		active = False
	else:
		print(message)

# Usando 'while(True)' y 'breaks'
# "A loop that starts with while True u will run forever unless it reaches a break statement."
# Un 'break' corta la ejecucion de un ciclo y sale de él (tanto en while's como en for's)
prompt = "\nPlease enter the name of a city you have visited:"
prompt += "\n(Enter 'quit' when you are finished.) "
while True:
	city = input(prompt)
	if city == 'quit':
		break
	else:
		print(f"I'd love to go to {city.title()}!")

# Usando la sentencia 'continue'
# Lo que hace es volver al inicio del ciclo (cabecera del while) y verificar la condicion.
# (en vez de directamente salir del ciclo como 'break')
current_number = 0
while current_number < 10:
	current_number += 1
	if current_number % 2 == 0:
		continue
	print(current_number)

# Ejemplo Pizza Toppings
toppings = []
mensaje = "¿Qué le agregamos a tu pizza? (ingresa 'salir' para terminar): "
condicion = True
while condicion:
	topping = input(mensaje)
	if topping.lower() == "salir":
		condicion = False
	else:
		print(f"Excelente! Le agregaremos {topping}.")
		toppings.append(topping)
print(f"Lista de Toppings: {toppings}")

# Ejemplo mover elementos de una lista a otra (con un 'for' no se podria modificar una lista a medida que se recorre)
unconfirmed_users = ['alice', 'brian', 'candace']
confirmed_users = []

while unconfirmed_users: #mientras haya elementos en la lista
    current_user = unconfirmed_users.pop()
    print(f"Verifying user: {current_user.title()}")
    confirmed_users.append(current_user)

print("\nThe following users have been confirmed:")
for confirmed_user in confirmed_users:
    print(confirmed_user.title())

# Eliminar todas las ocurrencias de un elemento en una lista
pets = ['dog', 'cat', 'dog', 'goldfish', 'cat', 'rabbit', 'cat']
print(pets)
while 'cat' in pets:
	pets.remove('cat')
print(pets)

# Armar un diccionario con datos de entrada
responses = {}
polling_active = True #'polling' es votación/encuesta

while polling_active:
    name = input("\nWhat is your name? ")
    response = input("Which mountain would you like to climb someday? ")
    # Store the response in the dictionary.
    responses[name] = response
    # Find out if anyone else is going to take the poll.
    repeat = input("Would you like to let another person respond? (yes/ no) ")
    if repeat == 'no':
        polling_active = False
        
print("\n--- Poll Results ---")
for name, response in responses.items():
    print(f"{name} would like to climb {response}.")
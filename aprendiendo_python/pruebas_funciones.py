# FUNCIONES
#
# Las funciones en Python se definen con la palabra reservada 'def', seguida del nombre de la funcion y sus argumentos.
# Al igual que en otras ocasiones, el bloque de codigo asociado a la funcion (el cuerpo) se indica con tabulaciones.
#
# De por sí la funcion no se ejecuta cuando el interprete de Python está leyendo el código, solo queda definida.
# Para ejecutarse, hay que escribir en algun momento (posterior a definir la funcion) el nombre de dicha funcion junto con sus parámetros

def saludar():
	"""Funcion que muestra por pantalla un saludo."""
	print("Hola!!!")

saludar()

# Nota: El texto entre triple comillas es un tipo de comentario especial que luego utiliza Python para documentar las funciones.
#       Es como para luego generar onda un JavaDoc de Java, aunque no se si sea posible. Se denominan 'docstrings'.

def saludar2(nombre, apellido):
	"""Funcion que muestra por pantalla un saludo, pasandole 2 argumentos: 'nombre' y 'apellido'."""
	print(f"Hola {nombre} {apellido}!")

saludar2("Enzo", "Barria") #estos argumentos en Python son llamados 'posicionales'*.
saludar2(7,1) #vemos lo poderoso de no declarar tipos para este caso:
# Podemos usar la misma funcion pasandole tipos de datos diferentes, sin necesidad de definir varias funciones.
# Pero también hay que tener cuidado con esto... puede haber errores al intentar manipular un tipo de variable no esperado.

#---------------------------------------
# Argumentos 'clave' (Keyword Arguments)
# A keyword argument is a name-value pair that you pass to a function.
#
# Cuando llamamos comunmente a una funcion, debemos colocar los argumentos en su orden exacto, tal cual fueron definidos en la funcion.
# Porque sino obtendremos resultados inesperados.
# Usando los Keyword Arguments nos despreocupamos de este orden, ya que Python conocerá los valores exactos que deben tener los parámetros

def informar(capital, pais):
	print(f"La capital de {pais.title()} es {capital}.")

# Estas 2 llamadas son equivalentes:
informar(capital="Buenos Aires", pais="Argentina")
informar(pais="Argentina", capital="Buenos Aires")

# Nota1: Los nombres de los argumentos 'clave' deben ser exactamente iguales a los definidos en la funcion.
# Nota2: Podemos usar o no este estilo de llamado a funciones, es una herramienta más que nos ofrece Python.
#        Cuando querramos podemos usarla, y sino seguimos usando el pasaje de parametros "común" (argumentos posicionales).

#---------------------------------------
# Valores por defecto
#
# Los parámetros de una funcion pueden tener valores por defecto, por lo que si cuando llamamos a una no le proveemos todos sus argumentos,
# utilizará los valores por defecto al ejecutar el código.
# "Using default values can simplify your function calls and clarify the ways in which your functions are typically used."
def describe_pet(pet_name, animal_type='dog'):
	"""Display information about a pet."""
	print(f"\nI have a {animal_type}.")
	print(f"My {animal_type}'s name is {pet_name.title()}.")

describe_pet('pancho')
describe_pet(pet_name='willie')
describe_pet(pet_name='harry', animal_type='hamster')

# Nota1: Cuando tenemos solo 1 parametro en la definicion de la funcion que no es por defecto,
#        y justamente hacemos la llamada a la funcion con 1 solo argumento, no hace falta usar un argumento 'clave'.
# Nota2: En la definicion de la funcion, primero debemos poner todos los parámetros que No sean por defecto, y por último los default.
#        ya que de esta manera Python puede seguir interpretando bien las llamadas "comunes" a las funciones (argumentos posicionales*: el orden)

print("")

# Ejemplo
def confeccion_remeras(tamanio='L', mensaje_impreso="I love Python"):
	print(f"Se hará una remera {tamanio.upper()} cuya estampa dirá '{mensaje_impreso}'.")

confeccion_remeras() #se utilizarán ambos parámetros por defecto.
confeccion_remeras(mensaje_impreso="May the code be with you")
confeccion_remeras('m')
confeccion_remeras('s',"Trust me, I'm an Engineer")

print("")

#---------------------------------------
# RETURN
#
# Las funciones en Python no necesitan declararse como 'void' o como que devuelven algun tipo de dato.
# Si queres que tu funcion devuelva algo, le agregamos al final la plabara reservada 'return' seguido de un valor.
# (se puede retornar cualquier cosa: numeros, strings, booleans, listas, diccionarios...)
# Si no colocamos ningun return, la funcion es como 'void' (no devuelve nada, onda un 'procedimiento').

def get_formatted_name(first_name, last_name):
    """Return a full name, neatly formatted."""
    full_name = f"{first_name} {last_name}"
    return full_name.title()

musician = get_formatted_name('matt', 'bellamy')
print(musician)

# Tambien podriamos omitir argumentos (hacerlos opcionales) mediante valores por defecto
def get_formatted_name2(first_name, last_name, middle_name=''):
    if middle_name: #Python interprets non-empty strings as True
        full_name = f"{first_name} {middle_name} {last_name}"
    else:
        full_name = f"{first_name} {last_name}"
    return full_name.title()

musician = get_formatted_name2('jimi', 'hendrix')
print(musician)
musician = get_formatted_name2('john', 'hooker', 'lee')
print(musician)

#---------------------------------------
# Modificando LISTAS en funciones
#
# En las funciones no hace falta especificar si los parametros son por valor o por referencia (salir modificados).
# Los unicos parametros por referencias son las Listas, el resto de valores que le pasemos a una funcion no se modificarán.
# Por lo que dentro de una funcion podremos hacerle modificaciones a una lista, y a la salida los cambios serán permanentes.
# (REVISAR si los diccionarios tambien son por referencia o no)

def print_models(unprinted_designs, completed_models):
    """
    Simulate printing each design, until none are left.
    Move each design to completed_models after printing.
    """
    while unprinted_designs:
        current_design = unprinted_designs.pop()
        print(f"Printing model: {current_design}")
        completed_models.append(current_design)
        
def show_completed_models(completed_models):
    """Show all the models that were printed."""
    print("\nThe following models have been printed:")
    for completed_model in completed_models:
        print(completed_model)
        
unprinted_designs = ['phone case', 'robot pendant', 'dodecahedron']
completed_models = []

print_models(unprinted_designs, completed_models)
show_completed_models(completed_models)

# Nota: si quisieramos evitar que una funcion modifique una lista, tendríamos que mandarle una copia de la lista en cuestión.
#       Esto se hace mendiante la notacion de "slice's", al llamar a la funcion con una lista: function_name(list_name[:])
#       "The slice notation [:] makes a copy of the list to send to the function."
#       En el ejemplo anterior, si no quisieramos vaciar la lista original (unprinted_designs), deberiamos llamar a la funcion así:
#       "print_models(unprinted_designs[:], completed_models)"
# Sin embargo, "you should pass the original list to functions unless you have a specific reason to pass a copy.
# It’s more efficient for a function to work with an existing list to avoid using the time and memory needed to
# make a separate copy, especially when you’re working with large lists."

#-----------------------------------------------
# Número arbitrario de parámetros de una funcion
#
# En Python podemos declarar una funcion que espere recibir una cantidad arbitraria/variable de argumentos cuando la llamen.
# (esto es parecido a la funcion 'printf()' de C, que le podiamos pasar tantas variables para que muestre como queramos)

def make_pizza(*toppings):
    """Print the list of toppings that have been requested."""
    print(toppings)

make_pizza('pepperoni')
make_pizza('mushrooms', 'green peppers', 'extra cheese')

# El asterisco en el nombre del parámetro " *toppings " le dice a Python que cree una TUPLA vacía llamada "toppings"
# y guarde los valores que reciba en esta tupla. toppings = (valor1, valor2, ..., valorN)

# Nosotros llamamos a la funcion normalmente con tantos argumentos como queramos, y Python se encarga de guardarlos en la tupla.
# Si quisieramos agregar parámetros fijos ("comunes"), deben ir antes del parámetro variable: f(p1, p2, ..., *p)
# "You’ll often see the generic parameter name *args, which collects arbitrary positional arguments like this."

def build_profile(first, last, **user_info):
    """Build a dictionary containing everything we know about a user."""
    user_info['first_name'] = first
    user_info['last_name'] = last
    return user_info

user_profile = build_profile('albert', 'einstein',
                             location='princeton',
                             field='physics')
print(user_profile)

# Este es otro tipo de parámetro variable, donde los 2 asteriscos (**user_info) indican que dicho parámetro será un diccionario,
# que almacenará todos los pares clave-valor recibidos cuando llamamos a la funcion (al momento de llamarla se usan los argumentos 'clave')
# "Within the function, you can access the keyvalue pairs in user_info just as you would for any dictionary."

# "You’ll often see the parameter name **kwargs used to collect non-specific keyword arguments."

# ---------
# CONVENCIONES DE DISEÑO/ESTILO
#
# -nombres de funciones y módulos: descriptivos, en letras minusculas y usando guiones bajos para separar palabras.
# -documentacion: cada funcion deberia tener un comentario explicando brevemente qué es lo que hace (en formato docstring """)
# -parámetros por defecto: no debe haber espacios entre el signo de asignacion: def function_name(param_0, param_1='default value')
# -argumentos keyword: lo mismo aplica cuando llamamos a una funcion con argumentos 'clave': function_name(value_0, param_1='value')
# -largo de la definicion de la funcion: si sobrepasa el limite de 79 caracteres dicho por la PEP8, pongamos los parámetros en varias
#                                        lineas, tabulando 2 veces para distinguirlos del cuerpo de la funcion, que estará solo 1.
# -espaciado entre funciones: entre funcion y funcion deberia haber 2 lineas en blanco para remarcar bien cuando termina una y empieza la otra.
# -imports: de usar imports, deben estar al comienzo del archivo (lo unico que podría haber antes son comentarios).
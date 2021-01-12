# Programa que se fija si un usuario se encuentra en un archivo .json, para darle la bienvenida.
# Si no lo encuentra, le pregunta si quiere registrarse (y que quede guardado su nombre de usuario en el archivo)
# La estructura del .json es una lista (arreglo) de diccionarios (objetos): [{"username":"user1", "first_name":"fn1", "last_name":"ln1"}, ...]

import json

def login(nombre_usuario, nombre_archivo):

    usuarios = leer_archivo_json(nombre_archivo)
    
    esta = buscar(nombre_usuario, usuarios)

    if esta:
        print(f"Bienvenido nuevamente, {nombre_usuario}!!!\n")
    else:
        res = input(f"Lo siento, el nick '{nombre_usuario}' no se encuentra. ¿Querés registrarlo? (S/N): ")
        if res.lower() == 's':
            agregar(nombre_usuario, usuarios, nombre_archivo)
            print("Registro completado con éxito!\n")
        else:
            print("Quizás en otra oportunidad, chauu!!!\n")


def leer_archivo_json(nombre_archivo):
    """Función que lee el contenido del archivo .json que contiene a los usuarios"""
    try:
        with open(nombre_archivo) as arch: #intentamos leer el archivo.
            usuarios = json.load(arch)
    except FileNotFoundError:
        with open(nombre_archivo, 'w') as arch: #si no existe, lo creamos con una lista vacía.
            usuarios = []
            json.dump(usuarios,arch)

    return usuarios


def buscar(nombre_usuario, usuarios):
    """Funcion que busca si en la lista de usuarios hay un diccionario con dicho nombre_usuario
        retorna True si lo encuentra, y False si no lo encuentra."""
    longitud = len(usuarios)
    i = 0
    condicion = True
    while i<longitud and condicion:
        usuario = usuarios[i]
        condicion = nombre_usuario != usuario["username"]
        i += 1
    return (not condicion)


def agregar(nombre_usuario, usuarios, nombre_archivo):
    """Función que agrega un nuevo usuario al archivo de usuarios
        nombre_usuario: usuario a agregar
        usuarios: lista de usuarios leida le archivo .json, a la cual agregaremos el nuevo usuario
        nombre_archivo: nombre del archivo .json donde se guardará la lista de usuarios actualizada"""
    print("Por favor, ingrese su nombre y apellido para finalizar el registro.")
    nombre = input("\tNombre: ")
    apellido = input("\tApellido: ")
    user = {"username":nombre_usuario, "first_name":nombre.title(), "last_name":apellido.title()}
    usuarios.append(user)
    with open(nombre_archivo, 'w') as arch:
        json.dump(usuarios,arch)



def iniciar():

    nombre_archivo_json = "lista_usuarios.json"
    
    flag = True
    while flag:
        print("-----------------------------------------")
        print("1. Loguearse.")
        print("2. Limpiar lista de usuarios registrados.")
        print("3. Salir.")
        print("-----------------------------------------")
        res = input("Ingrese un número: ")

        if res == '1':
            username = input("Ingrese su nombre de usuario: ")
            login(username.lower(), nombre_archivo_json) #haremos que por ejemplo el user EnZo sea el mismo que enzo (no distingue mayus de minus)
        elif res == '2':
            warning = input("¡¿SEGURO?! (S/N): ")
            if warning.lower() == 's':
                with open(nombre_archivo_json, 'w') as arch:
                    json.dump([],arch)
                print("Registro limpiado!\n")
            else:
                print("Limpieza de registro CANCELADO!\n")
        else:
            flag = False


# ------------------------------------------------------------------------------

iniciar()

# Para probar que se lea realmente una lista de diccionarios.
with open("lista_usuarios.json") as arch:
    lectura = json.load(arch)

print(type(lectura)) #lista
print(type(lectura[0])) #diccionario

# ------------------------------------------------------------------------------

"""Often, you’ll come to a point where your code will work, but you’ll recognize
that you could improve the code by breaking it up into a series of functions
that have specific jobs. This process is called refactoring. Refactoring
makes your code cleaner, easier to understand, and easier to extend.
   This compartmentalization of work is an essential part of writing
clear code that will be easy to maintain and extend."""

# Refactoring: esto es lo que hicimos en este programa. Subdividimos el login (programa principal) en funciones
# que hacen tareas especificas y claras, cada una tiene su propósito, delegamos responsabilidades.
# Esto nos permite organizar mejor nuestro programa principal, que se vea mas claro.
# Ademas podremos testear y extender el código más fácilmente.
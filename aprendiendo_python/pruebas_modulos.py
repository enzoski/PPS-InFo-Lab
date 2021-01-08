# -------
# MÓDULOS
# -------
# "You can store your functions in a separate file called a module and then importing that module into your main program.
# An import statement tells Python to make the code in a module available in the currently running program file."
# Un modulo es un archivo .py que contiene código que queramos importar en nuestro programa.

def suma(x, y):
    resultado = x + y
    return resultado

def resta(x, y):
    resultado = x - y
    return resultado

# Por ejemplo, este archivo 'pruebas_modulos.py' será un módulo que contiene funciones que realizan operaciones matemáticas.
# Para que este modulo pueda ser importado desde otro archivo, tanto este como el otro deben estar en el mismo directorio/carpeta.

# A continuacion simularemos cómo importar este modulo desde otro archivo y usar sus funciones:

 import pruebas_modulos #aca no se pone el ".py", solo la palabra reservada 'import' seguido del nombre del archivo/modulo a importar.

 respuesta1 = pruebas_modulos.suma(2,2)
 respuesta2 = pruebas_modulos.resta(10,9)

# "When Python reads this file, the line import pruebas_modulos tells Python to open the file pruebas_modulos.py and copy all the functions
# from it into this program. You don’t actually see code being copied between files because Python copies the code behind the scenes
# just before the program runs. All you need to know is that any function defined in the module, will now be available in the file
# that imports it."
#
# Para llamar a las funciones del modulo importado, hay que escribir el nombre del modulo, seguido de un punto (.) y el nombre de la funcion.
# Esta forma de importar un modulo, lo que hace es copiar ABSOLUTAMENTE TODO el archivo del modulo, en el archivo donde importamos.
#
# ------------------------------------------------
# IMPORTAR FUNCIONES ESPECIFICAS
# 
# Otra cosa que podemos hacer es importar unicamente ciertas funciones de un módulo. La sintaxis es:
# from module_name import function_0, function_1, function_2, ..., function_N
# Y de esta manera no hace falta usar la notacion del punto (.) para usar las funciones, directamente se llaman con su nombre.

from pruebas_modulos import suma
respuesta3 = suma(2,2)


# ------------------------------------------------
# IMPORTAR TODAS LAS FUNCIONES DE UN MODULO
#
# A diferencia del 'import' comun que importa todo lo que haya en el modulo (funciones, constantes, etc.), podemos importar solo
# las fuciones y la totalidad de ellas. Ademas de esta forma no se usa la notacion del punto (.) para llamar a las funciones.

from pruebas_modulos import *

respuesta4 = suma(2,2)
respuesta5 = resta(10,9)

# "However, it’s best not to use this approach when you’re working with larger modules that you didn’t write: if the module has a function
# name that matches an existing name in your project, you can get some unexpected results. Python may see several functions or variables
# with the same name, and instead of importing all the functions separately, it will overwrite the functions."
# "The best approach is to import the function or functions you want, or import the entire module and use the dot notation.
# This leads to clear code that’s easy to read and understand."

# ------------------------------------------------
# DARLE UN 'ALIAS' A UNA FUNCION IMPORTADA
#
# Cuando importamos una funcion, tambien podemos asignarle un nombre distinto al original, por si nosotros ya tenemos definida una
# funcion con ese nombre, o si nos parece un nombre demasiado largo o confuso. Esto se hace con la palabra reservada 'as'.

from pruebas_modulos import resta as r
respuesta6 = r(10,9)


# ------------------------------------------------
# DARLE UN 'ALIAS' A UN MODULO IMPORTADO
# 
# De la misma manera, tambien podemos darle un nombre alternativo al modulo que estamos importando para usarlo en nuestro programa.
#
# "Calling the functions by writing p.make_pizza() is not only more concise than writing pizza.make_pizza(),
# but also redirects your attention from the module name and allows you to focus on the descriptive names of its functions."

import pruebas_modulos as pm

respuesta7 = pm.suma(2,2)
respuesta8 = pm.resta(10,9)


# ------------------------------------------------
# RESUMEN
import module_name
from module_name import function_name
from module_name import function_name as fn
import module_name as mn
from module_name import *

# Nota: al principio de cada módulo (la/s primera/s línea/s) deberiamos tener un 'docstring' que diga brevemente qué contiene el modulo (de qué se trata).

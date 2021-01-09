# Programación Orientada a Objetos en Python
#
# La estructura de una clase en Python es la siguiente:

class Dog:
    """A simple attempt to model a dog."""  
  
    def __init__(self, name, age):
        """Initialize name and age attributes."""
        self.name = name
        self.age = age
        
    def sit(self):
        """Simulate a dog sitting in response to a command."""
        print(f"{self.name} is now sitting.")

    def roll_over(self):
        """Simulate rolling over in response to a command."""
        print(f"{self.name} rolled over!")


# -Los nombres de las clases empiezan con mayuscula, y los posibles espacios no los ponemos con '_', directamente ponemos todo junto.
# -Toda la estructura de la clase queda marcada por la indentación.
# -Como los tipos en Python son dinamicos (y por ende no hay declaraciones de variables), no veremos como se estructura el estado
#  de la clase, es decir, no veremos al principio los atributos de clase (salvo cuando haya que asignares un valor inicial).
#  ->en realidad no lo veremos porque es un error sintactico, ya que entre la definicion de la clase y el primer método, no hay ninguna
#    referencia a 'self', y es la unica manera de saber que estamos hablando de una clase/objeto.
#    No es como Java que mantiene esa info en el .class (creo) y siempre podemos usar el .this, en todo momento.
# -Los métodos de la clase se estructuran como las funciones.
# -El método __init__() es el constructor de la clase. Se ejecuta automaticamente al instanciar la clase (crear una nueva instancia).
#  siempre debe tener ese nombre para que python sepa que es el constructor, y deberiamos evitar escribir metodos propios con ese nombre.
# -La palabra reservada 'self' es como una variable que contiene la referencia del objeto resultante de la instanciacion de la clase.
# -'self' siempre debe ir como primer parámetro del constructor (y de los métodos), ya que Python lo usa y necesita para mantener la
#  referencia del objeto particular y poder acceder a sus atributos y métodos. De todas formas, cuando creamos el objeto
#  (o cuando llamamos métodos) el 'self' se pasa automaticamente por argumento, no lo tenemos que poner nosotros al llamar al constructor.
#  O sea, en la definicion de métodos, se pone como primer parámetro 'self'. Pero al llamar a esos métodos, No se pasa ese 'self' por argumento.
# -toda variable "self.variable" será un atributo de clase.

# --------------------------------------------------------
# INSTANCIAR UNA CLASE
#
# Para crear un objeto de una clase, llamamos a su constructor (pero en vez de llamar a '__init()__', ponemos el nombre de la clase).
# La instancia se guardará en la variable que asignemos.

my_dog = Dog('Willie', 6)

# Para acceder a los atributos del objeto, usamos la notacion del punto (.).
# Nota: por ahora no se menciona nada de atributos privados.

print(f"My dog's name is {my_dog.name}.")
print(f"My dog is {my_dog.age} years old.")

# Para llamar a los métodos del objeto, también se utiliza la notacion del punto (.).

my_dog.sit()
my_dog.roll_over()

# Nota: como siempre, al ser un lenguaje interpretado (y no es procedural), no hace falta tenener una funcion 'main' para ejecutar
# nuestro programa. Podemos tener como en este caso definida una clase y justo debajo estar el codigo que utiliza a dicha clase.

# --------------------------------------------------------

class Car:
    """A simple attempt to represent a car."""

    # self.prueba = 7 -> Esto no se puede hacer en Python, es un error sintáctico, porque 'self' no está definido en este ámbito.

    def __init__(self, make, model, year):
        """Initialize attributes to describe a car."""
        self.make = make
        self.model = model
        self.year = year
        self.odometer_reading = 0
        
    def get_descriptive_name(self):
        """Return a neatly formatted descriptive name."""
        long_name = f"{self.year} {self.make} {self.model}"
        return long_name.title()

    def read_odometer(self):
        """Print a statement showing the car's mileage."""
        print(f"This car has {self.odometer_reading} miles on it.")

    def update_odometer(self, mileage):
        """Set the odometer reading to the given value."""
        self.odometer_reading = mileage

    def increment_odometer(self, miles):
        """Add the given amount to the odometer reading."""
        self.odometer_reading += miles

# Para definir valores de atributos por defecto, se los inicializa en el metodo __init__(). Recordemos que la parte conceptual del
# constructor es inicializar correctamente el estado del objeto (sus atributos).

my_new_car = Car('audi', 'a4', 2019)

print(my_new_car.get_descriptive_name())

my_new_car.read_odometer()

# MODIFICAR VALORES DE ATRIBUTOS

my_new_car.odometer_reading = 50 # Accediendo directamente al atributo mediante la instancia.
my_new_car.read_odometer()

my_new_car.update_odometer(100) # Llamando a un método que se encargue de modificar el atributo (setter -> recomendado).
my_new_car.read_odometer()

my_new_car.increment_odometer(70) # Incrementando su valor.
my_new_car.read_odometer()

# "You can use methods like this to control how users of your program update values such as an odometer reading,
# but anyone with access to the program can set the odometer reading to any value by accessing the attribute directly.
# Effective security takes extreme attention to detail in addition to basic checks like those shown here."

# --------------------------------------------------------

# HERENCIA
#
# Las clases hijas (subclases) en Python se definen colocando el nombre de la clase padre (superclase) entre parentesis.
# La clase hija heredará todos los atributos y métodos de la clase padre (por lo cual tendrá acceso a ellos).

class ElectricCar(Car):
    """Represent aspects of a car, specific to electric vehicles."""
    
    def __init__(self, make, model, year):
        #constructor
        super().__init__(make, model, year) #inicializamos los atributos del padre.
        self.battery_size = 75 #inicializamos los atributos propios.

    def describe_battery(self):
        """Print a statement describing the battery size. (método propio)"""
        print(f"This car has a {self.battery_size}-kWh battery.")

my_tesla = ElectricCar('tesla', 'model s', 2019)
print(my_tesla.get_descriptive_name())
my_tesla.describe_battery()

# Si tenemos una clase padre y otra hija en el mismo archivo, el padre debe estar escrito antes que el hijo.
# (en general, siempre que desde una clase hagamos referencia a otra, esa otra debe estar definida antes)
# Para hacer referencia a los atributos y métodos del padre, usamos la funcion 'super()' seguido de un punto (.)
# Tambien podemos sobrescribir atributos o metodos, escribiendoles el mismo nombre que tienen en la clase padre.

# --------------------------------------------------------
# Atributos que contienen objetos
#
# Cuando vemos que una clase se nos está haciendo muy grande porque especificamos muchas cosas, por ahi conviene tener un atributo
# que contenga un objeto donde en su clase se defina todo su comportamiento, en vez de hacerlo en esta otra gran clase.
#
# Por ejemplo, hacer una clase Bateria que tenga todos los atributos y metodos referidos de un auto electrico.
# En la clase ElectricCar, en el constructor deberiamos poner esto: self.battery = Battery() y sacar el atributo battery_size y el metodo
# y accedemos a este metodo mediante la Bateria, le delegamos la responsabilidad de describir una bateria "battery.describe_battery()"

class Battery:
    """A simple attempt to model a battery for an electric car."""
    
    def __init__(self, battery_size=75): #esto de los parámetros opcionales, en Java lo haciamos haciendo más de un constructor.
        """Initialize the battery's attributes."""
        self.battery_size = battery_size

    def describe_battery(self):
        """Print a statement describing the battery size."""
        print(f"This car has a {self.battery_size}-kWh battery.")

    def get_range(self):
        """Print a statement about the range this battery provides."""
        if self.battery_size == 75:
            range = 260
        elif self.battery_size == 100:
            range = 315
            
        print(f"This car can go about {range} miles on a full charge.")

# --------------------------------------------------------
#
# IMPORTANDO CLASES
#
# Al igual que las funciones, podemos escribir las clases que queramos dentro de un modulo, y luego desde otro archivo importar el modulo
# ya sea completo, o importando solo las clases que queramos. Esto nos permite tener el archivo de nuestro programa principal más limpio.
#
# Se recomienda que las clases que se relacionen entre sí de alguna manera (por ejemplo las clases padre e hijas, o que una esté
# como atributo de la otra, etc), esten en el mismo módulo (en el mismo archivo .py).
#
# La sintaxis para importar clases es la misma que vimos con funciones:

import module_name                            # importamos un módulo completo.
from module_name import ClassName             # importamos una clase específica de un módulo (o varias separadas por comas).
from module_name import ClassName as CN       # importamos una clase específica de un módulo, y le damos un alias.
import module_name as mn                      # importamos un módulo completo, y le damos un alias.
from module_name import *                     # importamos unicamente la totalidad de las clases de un módulo.

# "When you’re starting out, keep your code structure simple. Try doing everything in one file and moving your classes to separate modules
# once everything is working. If you like how modules and files interact, try storing your classes in modules when you start a project.
# Find an approach that lets you write code that works, and go from there."

# --------------------------------------------------------
#
# CONVENCIONES DE DISEÑO/ESTILO DE CLASES:
#
# -Nombres de Clases: deben ser escritas en CamelCase.
# -Nombres de Instancias: deben ser escritas en minusculas y usando guiones bajos para separar palabras.
# -Documentacion: cada clase debería tener un 'docstring' justo despues de su definicion (luego de la cabecera).
# -Lineas en blanco: entre método y método de una clase, se deja una linea en blanco; y entre clase y clase, dos líneas en blanco.

# TESTING
#
# En Python contamos con un módulo ('unittest') que nos permite hacer casos de prueba. Con el testing se busca probar nuestro código
# (verificar que funciona como esperabamos o no) de una forma automatizada, la cual nos permitirá agilizar el proceso de prueba.
# Haremos programas que probarán el funcionamiento de otro programa, los cuales prodremos ejecutar todas las veces que queramos.

""" A unit test verifies that one specific aspect of a function’s
behavior is correct. A test case is a collection of unit tests that together prove
that a function behaves as it’s supposed to, within the full range of situations
you expect it to handle.
    A test case with full coverage includes a full range of unit
tests covering all the possible ways you can use a function.
(cosa que no siempre es necesario hacer, o directamente no se puede por ciertos
comportamientos del lenguaje en que estemos testeando)"""

import unittest
from funcion_a_probar import get_formatted_name

class NamesTestCase(unittest.TestCase):
    """Tests for 'name_function.py'."""
    
    def test_first_last_name(self):
        """Do names like 'Janis Joplin' work?"""
        formatted_name = get_formatted_name('janis', 'joplin')
        self.assertEqual(formatted_name, 'Janis Joplin')
        # si se cumple la igualdad, veremos un OK en consola, sino veremos un 'traceback' (con un 'FAIL', que nos indica un error
        # en el funcionamiento esperado de la función). (y si hay un error sintáctico en el código, nos mostrará un 'ERROR').

    def test_first_last_middle_name(self):
        """Do names like 'Wolfgang Amadeus Mozart' work?"""
        formatted_name = get_formatted_name(
            'wolfgang', 'mozart', 'amadeus')
        self.assertEqual(formatted_name, 'Wolfgang Amadeus Mozart')


if __name__ == '__main__': # *
    unittest.main()


# Para hacer un caso de prueba debemos importar 'unittest' y la funcion o clase que queramos testear.
# Luego debemos hacer una clase Test que herede de 'unittest.TestCase', con esto, entre otras cosas, tendremos acceso a los 'assert', que
# son el mismo concepto que vimos en Java (comprobar que un componenete/función haga lo que debería hacer; y si algo falla, se lanzará una excepcion
# del assert; de todas formas se ejecutará la totalidad de los métodos de prueba y luego se verá cuales fallaron y cuales no).
# Cada método de prueba (que representa una prueba unitaria) debe comenzar con el nombre 'test_', para que Python lo ejecute automaticamente
# cuando ejecutemos este archivo ('pruebas_testing.py').

# * Este 'if' es algo más bien técnico. Todos nuestros programas de Python, tienen varias variables 'ocultas'.
#   Una de ellas, es '__name__', la cual toma el valor de "__main__" cuando ejecutamos DIRECTAMENTE un archivo en cuestión.
#   Si nosotros por ejemplo importaramos ESTE archivo desde otro programa, cuando ejecutaramos ese otro programa, la variable __name__
#   de ESTE archivo no sería __main__, no sería el archivo 'principal'. Entonces el 'if' daría 'false'. Haciendo esto evitamos que se
#   ejecute 'unittest.main()' cuando importamos este archivo (ya que hay frameworks de testing que importan clases de prueba y las ejecutan
#   de otra manera, desde su archivo principal).
#   'unittest.main()' lo que hace es ejecutar todos los métodos de prueba de nuestra clase de prueba (ejecuta el caso de prueba).

# No está mal tener nombres de métodos de prueba bien descriptivos, por mas que sean largos. Asi si alguno falla, veremos claramente
# en la consola qué comportamiento de la función falló. Ademas tampoco es que tengamos que escribir el nombre de los métodos para llamarlos,
# ya que eso lo hace Python automáticamente.

# Métodos Assert provistos por el módulo 'unittest' de Python:
"""
Method                  Use
assertEqual(a, b)       Verify that a == b
assertNotEqual(a, b)    Verify that a != b
assertTrue(x)           Verify that x is True
assertFalse(x)          Verify that x is False
assertIn(item, list)    Verify that item is in list
assertNotIn(item, list) Verify that item is not in list
"""

# --------------------------------------------------------
# Testeando CLASES
# --------------------------------------------------------
#
# Hasta recien principalmente vimos como testear funciones concretas, pero también podemos testear una clase completa.
# La metodología es la misma, solo que en vez de importar una función puntual, importaremos una clase.
# Ahora lo que haremos será testear los métodos de una clase. Para ello, en cada método de prueba (prueba unitaria), haremos uso de una
# instancia de la clase que estamos testeando, para poder acceder a sus métodos.
#
# Método setUp()
#
# El módulo 'unittest' también cuenta con el método 'setUp()', el cual se ejecuta antes de ejecutarse cada método de prueba, o sea, se
# ejecutara el setUp() tantas veces como métodos de prueba tengamos. Esto nos permite armar 'escenarios' para nuestro caso de prueba,
# por ejemplo instanciar la clase y rellenarle alguna lista que tenga.

""" NOTA: When a test case is running, Python prints one character for each unit test as it is
completed. A passing test prints a dot, a test that results in an error prints an E, and
a test that results in a failed assertion prints an F. This is why you’ll see a different
number of dots and characters on the first line of output when you run your test cases.
If a test case takes a long time to run because it contains many unit tests, you can
watch these results to get a sense of how many tests are passing. """

# --------------------------------------------------------------------------------------------

# Ejemplo:

class AnonymousSurvey:
    """Collect anonymous answers to a survey question."""
    
    def __init__(self, question):
        """Store a question, and prepare to store responses."""
        self.question = question
        self.responses = []
        
    def show_question(self):
        """Show the survey question."""
        print(self.question)
        
    def store_response(self, new_response):
        """Store a single response to the survey."""
        self.responses.append(new_response)
        
    def show_results(self):
        """Show all the responses that have been given."""
        print("Survey results:")
        for response in self.responses:
            print(f"- {response}")


# Caso de prueba

"""import unittest
from survey import AnonymousSurvey"""

class TestAnonymousSurvey(unittest.TestCase):
    """Tests for the class AnonymousSurvey"""
    
    def setUp(self):
        """
        Create a survey and a set of responses for use in all test methods.
        """
        question = "What language did you first learn to speak?"
        self.my_survey = AnonymousSurvey(question) #cada vez que se ejecute el setUp(), habrá una nueva instancia.
        self.responses = ['English', 'Spanish', 'Mandarin']

    def test_store_single_response(self):
        """Test that a single response is stored properly."""
        self.my_survey.store_response(self.responses[0])
        self.assertIn(self.responses[0], self.my_survey.responses) # yo haría un getter de la lista, en la clase AnonymousSurvey.

    def test_store_three_responses(self):
        """Test that three individual responses are stored properly."""
        for response in self.responses:
            self.my_survey.store_response(response)
        for response in self.responses:
            self.assertIn(response, self.my_survey.responses)

"""if __name__ == '__main__':
    unittest.main()"""

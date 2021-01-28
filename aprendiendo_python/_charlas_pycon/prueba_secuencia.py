# Charla de Raymond Hettinger: Beyond PEP 8
# ---------------------
# Al definir los métodos dunder/mágicos '__len__()' y '__getitem__()' en una clase, estamos definiendo una 'secuencia'.
# Y toda secuencia es 'iterable'. Entonces esta es una forma de hacer iterable una clase, sin necesidad de definir '__iter__()'.
# Igualmente, si definimos '__iter__()' y devolvemos un 'iterator', Python usará esta forma para iterar, en vez de ir haciendo '.__getitem__()'

class Libro:
    """docstring for Libro"""
    def __init__(self, lista_paginas):
        self.lista_paginas = lista_paginas
        #self.prueba = {1: "asdasd", 2: "qwerty"}

    def __len__(self):
        return len(self.lista_paginas) #defino que el tamaño/longitud de un objeto tipo Libro, será la cant. de páginas del mismo.

    def __getitem__(self, index): #defino que los objetos tipo Libro podran usar la notacion de indice "objeto[i]" para obtener valores.
        if index >= len(self):
            raise IndexError #lanzo una excepcion.
        return self.lista_paginas[index]

    #def __iter__(self):
        #return iter(self.prueba.values())


# ---

libro_1 = Libro(["Página 1. Introducción...", "Página 2. Desarrollo...", "Página 3. Conclusión..."])

print(len(libro_1))

print(libro_1[0])
print(libro_1[1])
print(libro_1[2])

print("------------------------------")

#vemos que podemos iterar sobre el objeto tipo Libro.
for pagina in libro_1:
    print(pagina)
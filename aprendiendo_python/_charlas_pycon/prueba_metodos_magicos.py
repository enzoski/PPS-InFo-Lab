# Charla de Nina Zakharenko: Elegant solutions...
# ---------------------
# Pondremos en práctica los llamados 'métodos mágicos'.

class Triangulo:
    """Clase que representa a un triángulo."""
    def __init__(self, lado1, lado2, lado3):
        self.lado1 = lado1
        self.lado2 = lado2
        self.lado3 = lado3

    def __len__(self): # redefinidmos el método predefinido de Python 'len()' (o mas bien le damos una implementacion para el tipo Triangulo).
        return 3

    def __add__(self, otro_triangulo): # implementamos la suma '+' entre objetos tipo Triangulo.
        l1 = self.lado1 + otro_triangulo.lado1
        l2 = self.lado2 + otro_triangulo.lado2
        l3 = self.lado3 + otro_triangulo.lado3
        return Triangulo(l1, l2, l3)

    def __str__(self): # redefinimos la representacion de objetos tipo Triangulo en pantalla (y tambien la funcion 'str()').
        return f"<L1={self.lado1} ; L2={self.lado2} ; L3={self.lado3}>"


# ---- MAIN ----
t1 = Triangulo(1,1,1)
t2 = Triangulo(2,2,2)

print(t1)
print(str(t1))
print(len(t1))

print(t2)
print(len(t2))

print("Suma de los lados de los 2 triangulos:")
print(t1 + t2)
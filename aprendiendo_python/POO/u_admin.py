# Importamos del archivo usuario.py la clase Usuario, ya que será la superclase (padre) de Admin.
from usuario import Usuario

class Admin(Usuario):
    """Clase que representa a un tipo especial de Usuario, por lo cual hereda de él."""

    def __init__(self, nombre, apellido, email, gustos=[], rango_privilegios=1):
        """Inicializa los atributos de la clase"""
        super().__init__(nombre, apellido, email, gustos) #atributos del padre
        self.rango_privilegios = rango_privilegios #atributos especificos de los admins
        self.lista_privilegios = self.asignar_privilegios(self.rango_privilegios)

    def asignar_privilegios(self, rp): #aunque no hagamos referencia a self, hay que ponerlo, sino tira error sintáctico.
        """Método 'privado' que devuelve una lista con las acciones que podrá
        hacer el admin en base a su rango de privilegios."""
        lista = []

        if rp >= 1:
            lista.append("can add post")
        if rp >=2:
            lista.append("can delete post")
        if rp >=3:
            lista.append("can ban user")

        return lista

    def mostrar_privilegios(self):
        """Método que muestra por pantalla los privilegios del admin."""
        print(f"Privilegios del administrador {self.nombre} (nivel {self.rango_privilegios}):")
        for p in self.lista_privilegios:
            print(f"\t-{p}")

    def saludar_usuario(self):
        """Método que sobreescribe al método heredado del padre para agregarle un print más, especial para admins."""
        super().saludar_usuario()
        print("A administrar se ha dicho !\n")


# --------------------------------------------------
print("------------------------------------------")

# Creo una instancia de un admin
admin_1 = Admin("Enzo", "Barria", "enzo@admin.com")

# Prueba de usar un método heredado
admin_1.describir_usuario()

# Prueba de usar un método sobreescrito
admin_1.saludar_usuario()

# Prueba de usar el método propio del admin
admin_1.mostrar_privilegios()

# ------

admin_1 = Admin("Enzo", "Barria", "enzo@admin.com", rango_privilegios=2)
admin_1.mostrar_privilegios()

admin_1 = Admin("Enzo", "Barria", "enzo@admin.com", rango_privilegios=3)
admin_1.mostrar_privilegios()
class Usuario:
    """Clase que representa a un usuario de una página web."""

    def __init__(self, nombre, apellido, email, gustos=[]):
        """Inicializa los atributos de la clase"""
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.gustos = gustos
        self.intentos_logueo = 1 # atributo por defecto

    def saludar_usuario(self):
        """Método que imprime un mensaje de bienvenida al usuario"""
        print(f"Bienvenid@ {self.nombre.title()}!!!")

    def describir_usuario(self):
        """Método que muestra por pantalla el estado del objeto"""
        u = f"{self.nombre} {self.apellido}"
        mensaje = f"Usuario: {u.title()}\nEmail: {self.email}\nGustos:"
        
        if self.gustos: # como el atributo 'gustos' es opcional, si no se ingresa quedará vacío por defecto.
            gustos = f"{self.gustos}"
        else:
            gustos = "Omitidos."
        
        print(f"{mensaje} {gustos}\n")

    def mostrar_intentos_logueo(self):
        print(f"Intentos de logueo de {self.nombre}: {self.intentos_logueo}")

    def incrementar_intentos_logueo(self):
        self.intentos_logueo += 1

    def resetear_intentos_logueo(self):
        self.intentos_logueo = 0


# ---------------------------------------------------------------------------------------

# Creo 3 instancias/objetos de Usuario
usuario_1 = Usuario("Enzo", "Barria", "enzo@enzo.com", ["futbol", "bajo", "tecnología"])
usuario_2 = Usuario("Bernardo", "Díaz", "diazb@hotmail.com")
usuario_3 = Usuario(email="bromero@yahoo.com.ar", nombre="Bianca", apellido="Romero")

lista_de_usuarios = [usuario_1, usuario_2, usuario_3]

# Saludo a los 3 usuarios
for user in lista_de_usuarios:
    user.saludar_usuario()

print("")

# Describo a los 3 usuarios
for user in lista_de_usuarios:
    user.describir_usuario()

# Pruebo los métodos referidos al logueo
usuario_1.mostrar_intentos_logueo()

for i in range(3):
    usuario_1.incrementar_intentos_logueo() #incremento 3 veces

usuario_1.mostrar_intentos_logueo()

usuario_1.resetear_intentos_logueo()

usuario_1.mostrar_intentos_logueo()
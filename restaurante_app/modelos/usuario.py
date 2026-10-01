class Usuario:
    def __init__(self, usuario, password, nombre="", rol="Cliente", id=None):
        self.id = id
        self.nombre = nombre
        self.usuario = usuario
        self.password = password
        self.rol = rol if rol else "Cliente"

    def __str__(self):
        return f"Usuario: {self.usuario} ({self.rol})"

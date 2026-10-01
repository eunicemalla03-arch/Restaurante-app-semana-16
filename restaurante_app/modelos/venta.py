class Venta:
    def __init__(self, id, producto_id, producto_nombre, cantidad, total, usuario="No registrado", fecha="Fecha no disponible"):
        self.id = id
        self.usuario = usuario
        self.producto_id = producto_id
        self.producto_nombre = producto_nombre
        self.cantidad = cantidad
        self.total = total
        self.fecha = fecha

    def __str__(self):
        return f"Venta #{self.id}: {self.usuario} - {self.producto_nombre} - {self.fecha}"

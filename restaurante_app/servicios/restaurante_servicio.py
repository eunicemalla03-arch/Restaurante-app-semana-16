from datetime import datetime

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio


class RestauranteServicio:

    def __init__(self):
        self.ruta_productos = "datos/productos.json"
        self.ruta_usuarios = "datos/usuarios.json"
        self.ruta_ventas = "datos/ventas.json"
        self.productos = []
        self.usuarios = []
        self.ventas = []
        self.cargar_datos()

    def cargar_datos(self):
        productos_data = ArchivoServicio.cargar_datos(self.ruta_productos)
        usuarios_data = ArchivoServicio.cargar_datos(self.ruta_usuarios)
        ventas_data = ArchivoServicio.cargar_datos(self.ruta_ventas)

        self.productos = [Producto(**p) for p in productos_data]
        self.usuarios = [Usuario(**u) for u in usuarios_data]
        self.ventas = [Venta(**venta) for venta in ventas_data] if isinstance(ventas_data, list) else []

    def _serializar_producto(self, producto):
        return {
            "id": producto.id,
            "nombre": producto.nombre,
            "precio": producto.precio,
            "cantidad": producto.cantidad
        }

    def _serializar_usuario(self, usuario):
        return {
            "id": usuario.id,
            "nombre": usuario.nombre,
            "usuario": usuario.usuario,
            "password": usuario.password,
            "rol": usuario.rol,
        }

    def _guardar_productos(self):
        datos = [self._serializar_producto(producto) for producto in self.productos]
        ArchivoServicio.guardar_datos(self.ruta_productos, datos)

    def _guardar_usuarios(self):
        datos = [self._serializar_usuario(usuario) for usuario in self.usuarios]
        ArchivoServicio.guardar_datos(self.ruta_usuarios, datos)

    def _guardar_ventas(self):
        datos = [
            {
                "id": venta.id,
                "usuario": venta.usuario,
                "producto_id": venta.producto_id,
                "producto_nombre": venta.producto_nombre,
                "cantidad": venta.cantidad,
                "total": venta.total,
                "fecha": venta.fecha,
            }
            for venta in self.ventas
        ]
        ArchivoServicio.guardar_datos(self.ruta_ventas, datos)

    def validar_acceso(self, usuario, password):
        return self.obtener_usuario_por_credenciales(usuario, password) is not None

    def obtener_usuario_por_credenciales(self, usuario, password):
        usuario = str(usuario).strip()
        password = str(password).strip()

        for u in self.usuarios:
            if u.usuario == usuario and u.password == password:
                return u

        return None

    def usuario_es_administrador(self, usuario):
        if isinstance(usuario, Usuario):
            return usuario.rol == "Administrador"

        usuario_id = str(usuario).strip()
        return any(u.usuario == usuario_id and u.rol == "Administrador" for u in self.usuarios)

    def listar_productos(self):
        return self.productos

    def listar_usuarios(self):
        return self.usuarios

    def obtener_usuario_por_id(self, usuario_id):
        try:
            usuario_id = int(usuario_id)
        except (TypeError, ValueError):
            return None

        for usuario in self.usuarios:
            if usuario.id == usuario_id:
                return usuario
        return None

    def obtener_usuario_por_usuario(self, usuario):
        usuario = str(usuario).strip()
        for u in self.usuarios:
            if u.usuario == usuario:
                return u
        return None

    def obtener_producto_por_id(self, producto_id):
        for producto in self.productos:
            if producto.id == int(producto_id):
                return producto
        return None

    def registrar_producto(self, datos):
        if not isinstance(datos, dict):
            raise ValueError("Los datos del producto deben venir en un diccionario.")

        campos_requeridos = ["id", "nombre", "precio", "cantidad"]
        for campo in campos_requeridos:
            if campo not in datos:
                raise ValueError(f"Falta el campo requerido: {campo}")

        producto_id = int(datos["id"])
        nombre = str(datos["nombre"]).strip()
        precio = float(datos["precio"])
        cantidad = int(datos["cantidad"])

        if not nombre:
            raise ValueError("El nombre del producto no puede estar vacío.")

        if self.obtener_producto_por_id(producto_id) is not None:
            raise ValueError(f"Ya existe un producto con el id {producto_id}.")

        producto = Producto(
            id=producto_id,
            nombre=nombre,
            precio=precio,
            cantidad=cantidad
        )

        self.productos.append(producto)
        self._guardar_productos()
        return producto

    def actualizar_producto(self, producto_id, datos):
        producto = self.obtener_producto_por_id(producto_id)

        if producto is None:
            raise ValueError(f"No existe un producto con el id {producto_id}.")

        if not isinstance(datos, dict):
            raise ValueError("Los datos del producto deben venir en un diccionario.")

        if "nombre" in datos:
            nombre = str(datos["nombre"]).strip()
            if not nombre:
                raise ValueError("El nombre del producto no puede estar vacío.")
            producto.nombre = nombre

        if "precio" in datos:
            producto.precio = float(datos["precio"])

        if "cantidad" in datos:
            producto.cantidad = int(datos["cantidad"])

        self._guardar_productos()
        return producto

    def eliminar_producto(self, producto_id):
        producto = self.obtener_producto_por_id(producto_id)

        if producto is None:
            raise ValueError(f"No existe un producto con el id {producto_id}.")

        self.productos = [p for p in self.productos if p.id != int(producto_id)]
        self._guardar_productos()
        return True

    def registrar_usuario(self, datos):
        if not isinstance(datos, dict):
            raise ValueError("Los datos del usuario deben venir en un diccionario.")

        nombre = str(datos.get("nombre", "")).strip()
        usuario = str(datos.get("usuario", "")).strip()
        password = str(datos.get("password", "")).strip()
        rol = str(datos.get("rol", "Cliente")).strip()

        if not nombre:
            raise ValueError("El nombre del usuario no puede estar vacío.")
        if not usuario:
            raise ValueError("El nombre de usuario no puede estar vacío.")
        if not password:
            raise ValueError("La contraseña no puede estar vacía.")

        roles_validos = {"Administrador", "Empleado", "Cliente"}
        if rol not in roles_validos:
            raise ValueError("El rol debe ser Administrador, Empleado o Cliente.")
        if self.obtener_usuario_por_usuario(usuario) is not None:
            raise ValueError(f"Ya existe un usuario con el nombre '{usuario}'.")

        nuevo_id = max((u.id for u in self.usuarios if u.id is not None), default=0) + 1
        nuevo_usuario = Usuario(
            id=nuevo_id,
            nombre=nombre,
            usuario=usuario,
            password=password,
            rol=rol,
        )
        self.usuarios.append(nuevo_usuario)
        self._guardar_usuarios()
        return nuevo_usuario

    def actualizar_usuario(self, usuario_id, datos):
        usuario = self.obtener_usuario_por_id(usuario_id)
        if usuario is None:
            raise ValueError(f"No existe un usuario con el id {usuario_id}.")

        if not isinstance(datos, dict):
            raise ValueError("Los datos del usuario deben venir en un diccionario.")

        if "nombre" in datos:
            nombre = str(datos["nombre"]).strip()
            if not nombre:
                raise ValueError("El nombre del usuario no puede estar vacío.")
            usuario.nombre = nombre

        if "usuario" in datos:
            nuevo_usuario = str(datos["usuario"]).strip()
            if not nuevo_usuario:
                raise ValueError("El nombre de usuario no puede estar vacío.")
            if nuevo_usuario != usuario.usuario and self.obtener_usuario_por_usuario(nuevo_usuario) is not None:
                raise ValueError(f"Ya existe un usuario con el nombre '{nuevo_usuario}'.")
            usuario.usuario = nuevo_usuario

        if "password" in datos:
            password = str(datos["password"]).strip()
            if not password:
                raise ValueError("La contraseña no puede estar vacía.")
            usuario.password = password

        if "rol" in datos:
            rol = str(datos["rol"]).strip()
            if rol not in {"Administrador", "Empleado", "Cliente"}:
                raise ValueError("El rol debe ser Administrador, Empleado o Cliente.")
            usuario.rol = rol

        self._guardar_usuarios()
        return usuario

    def eliminar_usuario(self, usuario_id):
        usuario = self.obtener_usuario_por_id(usuario_id)
        if usuario is None:
            raise ValueError(f"No existe un usuario con el id {usuario_id}.")

        if usuario.rol == "Administrador":
            raise ValueError("No se puede eliminar un usuario con rol Administrador.")

        self.usuarios = [u for u in self.usuarios if u.id != int(usuario_id)]
        self._guardar_usuarios()
        return True

    def registrar_venta(self, usuario, producto_id, cantidad=1):
        usuario = str(usuario).strip()
        if not any(u.usuario == usuario for u in self.usuarios):
            raise ValueError("Seleccione un usuario registrado.")

        producto = self.obtener_producto_por_id(producto_id)
        if producto is None:
            raise ValueError(f"No existe un producto con el id {producto_id}.")

        cantidad = int(cantidad)
        if cantidad <= 0:
            raise ValueError("La cantidad de la venta debe ser mayor a cero.")

        if producto.cantidad < cantidad:
            raise ValueError(f"No hay stock suficiente para {producto.nombre}. Stock disponible: {producto.cantidad}.")

        total = producto.precio * cantidad
        producto.cantidad -= cantidad

        venta = Venta(
            id=max((venta.id for venta in self.ventas), default=0) + 1,
            usuario=usuario,
            producto_id=producto.id,
            producto_nombre=producto.nombre,
            cantidad=cantidad,
            total=total,
            fecha=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )

        self.ventas.append(venta)
        self._guardar_productos()
        self._guardar_ventas()
        return venta

    def listar_ventas(self):
        return self.ventas

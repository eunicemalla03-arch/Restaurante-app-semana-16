import tkinter as tk
from pathlib import Path
from tkinter import ttk


class MenuComponent(ttk.Frame):
    def __init__(self, master, mostrar_usuarios, mostrar_productos, mostrar_ventas, cerrar_sesion, usuario_actual=None):
        super().__init__(master, padding=(10, 10, 10, 10))
        self.iconos = {}
        assets_dir = Path(__file__).resolve().parent.parent / "assets"
        for nombre in ("logotipo", "usuarios", "productos", "ventas"):
            ruta = assets_dir / f"{nombre}.xbm"
            if ruta.is_file():
                self.iconos[nombre] = tk.BitmapImage(
                    file=str(ruta),
                    foreground="#1e7069",
                    background="#f4f6fb",
                )

        logo = self.iconos.get("logotipo")
        ttk.Label(self, text="Restaurante", image=logo, compound="top", font=("Segoe UI", 12, "bold")).pack(pady=(0, 12))

        if usuario_actual is not None:
            ttk.Label(self, text=f"Usuario: {usuario_actual.usuario}", font=("Segoe UI", 9, "bold")).pack(pady=(0, 8))
            ttk.Label(self, text=f"Rol: {usuario_actual.rol}", font=("Segoe UI", 9)).pack(pady=(0, 10))

        self._crear_boton("Usuarios", "usuarios", mostrar_usuarios, habilitado=(usuario_actual is not None and usuario_actual.rol == "Administrador"))
        self._crear_boton("Productos", "productos", mostrar_productos)
        self._crear_boton("Ventas", "ventas", mostrar_ventas)
        ttk.Button(self, text="Cerrar sesión", command=cerrar_sesion, width=22).pack(pady=(18, 0))

    def _crear_boton(self, texto, icono, comando, habilitado=True):
        ttk.Button(
            self,
            text=texto,
            image=self.iconos.get(icono),
            compound="left",
            command=comando if habilitado else None,
            width=22,
            state="normal" if habilitado else "disabled",
        ).pack(pady=5)


class UsuarioFormComponent(ttk.Frame):
    def __init__(self, master, registrar, actualizar, eliminar, limpiar, cambiar_rol):
        super().__init__(master, padding=10)
        self.id_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        self.usuario_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.rol_var = tk.StringVar(value="Cliente")

        ttk.Label(self, text="ID:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(self, textvariable=self.id_var, width=14, state="readonly").grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(self, text="Nombre:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        ttk.Entry(self, textvariable=self.nombre_var, width=24).grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(self, text="Usuario:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(self, textvariable=self.usuario_var, width=14).grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(self, text="Contraseña:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        ttk.Entry(self, textvariable=self.password_var, width=24, show="*").grid(row=1, column=3, padx=5, pady=5)

        ttk.Label(self, text="Rol:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.rol_combo = ttk.Combobox(self, textvariable=self.rol_var, state="readonly", width=16, values=["Administrador", "Empleado", "Cliente"])
        self.rol_combo.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.rol_combo.bind("<<ComboboxSelected>>", cambiar_rol)

        ttk.Button(self, text="Registrar", command=registrar).grid(row=3, column=0, padx=5, pady=(12, 5), sticky="ew")
        ttk.Button(self, text="Actualizar", command=actualizar).grid(row=3, column=1, padx=5, pady=(12, 5), sticky="ew")
        ttk.Button(self, text="Eliminar", command=eliminar).grid(row=3, column=2, padx=5, pady=(12, 5), sticky="ew")
        ttk.Button(self, text="Limpiar", command=limpiar).grid(row=3, column=3, padx=5, pady=(12, 5), sticky="ew")


class UsuarioTableComponent(ttk.Treeview):
    def __init__(self, master):
        super().__init__(master, columns=("id", "nombre", "usuario", "rol"), show="headings", height=12)
        for columna, texto, ancho in (
            ("id", "ID", 60),
            ("nombre", "Nombre", 220),
            ("usuario", "Usuario", 150),
            ("rol", "Rol", 140),
        ):
            self.heading(columna, text=texto)
            self.column(columna, width=ancho, anchor="center")


class ProductoFormComponent(ttk.Frame):
    def __init__(self, master, registrar, cargar, actualizar, eliminar, limpiar):
        super().__init__(master, padding=10)
        self.id_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        self.precio_var = tk.StringVar()
        self.cantidad_var = tk.StringVar()

        ttk.Label(self, text="ID:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(self, textvariable=self.id_var, width=18).grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(self, text="Nombre:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        ttk.Entry(self, textvariable=self.nombre_var, width=22).grid(row=0, column=3, padx=5, pady=5)
        ttk.Label(self, text="Precio:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(self, textvariable=self.precio_var, width=18).grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(self, text="Cantidad:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        ttk.Entry(self, textvariable=self.cantidad_var, width=22).grid(row=1, column=3, padx=5, pady=5)
        ttk.Button(self, text="Registrar", command=registrar).grid(row=2, column=0, padx=5, pady=(12, 5), sticky="ew")
        ttk.Button(self, text="Cargar", command=cargar).grid(row=2, column=1, padx=5, pady=(12, 5), sticky="ew")
        ttk.Button(self, text="Actualizar", command=actualizar).grid(row=2, column=2, padx=5, pady=(12, 5), sticky="ew")
        ttk.Button(self, text="Eliminar", command=eliminar).grid(row=2, column=3, padx=5, pady=(12, 5), sticky="ew")
        ttk.Button(self, text="Limpiar", command=limpiar).grid(row=3, column=0, columnspan=4, pady=(8, 0), sticky="ew")


class ProductoTableComponent(ttk.Treeview):
    def __init__(self, master):
        super().__init__(master, columns=("id", "nombre", "precio", "cantidad"), show="headings", height=12)
        for columna, texto, ancho in (("id", "ID", 70), ("nombre", "Nombre", 220), ("precio", "Precio", 120), ("cantidad", "Cantidad", 110)):
            self.heading(columna, text=texto)
            self.column(columna, width=ancho, anchor="center")


class VentaFormComponent(ttk.Frame):
    def __init__(self, master, usuarios, productos, registrar):
        super().__init__(master, padding=10)
        self.usuario_var = tk.StringVar()
        self.producto_var = tk.StringVar()
        self.cantidad_var = tk.StringVar()
        self.productos_por_opcion = {}
        ttk.Label(self, text="Usuario:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.usuario_combo = ttk.Combobox(self, textvariable=self.usuario_var, state="readonly", width=22)
        self.usuario_combo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(self, text="Producto:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.producto_combo = ttk.Combobox(self, textvariable=self.producto_var, state="readonly", width=30)
        self.producto_combo.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        ttk.Label(self, text="Cantidad:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(self, textvariable=self.cantidad_var, width=12).grid(row=1, column=1, padx=5, pady=5, sticky="w")
        ttk.Button(self, text="Registrar venta", command=registrar).grid(row=1, column=2, columnspan=2, padx=5, pady=(10, 0), sticky="ew")
        self.actualizar_opciones(usuarios, productos)

    def actualizar_opciones(self, usuarios, productos):
        usuarios_actuales = [usuario.usuario for usuario in usuarios]
        self.usuario_combo["values"] = usuarios_actuales
        if self.usuario_var.get() not in usuarios_actuales:
            self.usuario_var.set(usuarios_actuales[0] if usuarios_actuales else "")

        self.productos_por_opcion = {
            f"{producto.id} | {producto.nombre} | ${producto.precio:.2f} | Stock: {producto.cantidad}": producto.id
            for producto in productos
        }
        opciones = list(self.productos_por_opcion)
        self.producto_combo["values"] = opciones
        if self.producto_var.get() not in opciones:
            self.producto_var.set(opciones[0] if opciones else "")


class VentaTableComponent(ttk.Treeview):
    def __init__(self, master):
        super().__init__(master, columns=("id", "usuario", "producto", "cantidad", "fecha", "total"), show="headings", height=14)
        for columna, texto, ancho in (
            ("id", "ID", 55),
            ("usuario", "Usuario", 110),
            ("producto", "Producto", 165),
            ("cantidad", "Cantidad", 75),
            ("fecha", "Fecha", 155),
            ("total", "Total", 100),
        ):
            self.heading(columna, text=texto)
            self.column(columna, width=ancho, anchor="center")
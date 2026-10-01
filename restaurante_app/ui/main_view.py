import tkinter as tk
from tkinter import ttk, messagebox

from ui.componentes import (
    MenuComponent,
    ProductoFormComponent,
    ProductoTableComponent,
    UsuarioFormComponent,
    UsuarioTableComponent,
    VentaFormComponent,
    VentaTableComponent,
)


class MainView(tk.Frame):
    def __init__(self, master, servicio, cambiar_vista, usuario_actual=None):
        super().__init__(master, bg="#f4f6fb")
        self.servicio = servicio
        self.cambiar_vista = cambiar_vista
        self.usuario_actual = usuario_actual
        self.usuario_seleccionado_id = None

        self.configure(padx=12, pady=12)

        self.nav_frame = MenuComponent(
            self,
            self.mostrar_usuarios,
            self.mostrar_productos,
            self.mostrar_ventas,
            lambda: self.cambiar_vista("login"),
            usuario_actual=self.usuario_actual,
        )
        self.nav_frame.pack(side="left", fill="y")

        self.content_frame = ttk.Frame(self)
        self.content_frame.pack(side="left", fill="both", expand=True)

        self.mostrar_productos()

    def limpiar_contenido(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def mostrar_ventas(self):
        self.limpiar_contenido()

        titulo = ttk.Label(self.content_frame, text="Registro de ventas", font=("Segoe UI", 14, "bold"))
        titulo.pack(anchor="w", pady=(0, 10))

        formulario = VentaFormComponent(
            self.content_frame,
            self.servicio.listar_usuarios(),
            self.servicio.listar_productos(),
            self.registrar_venta,
        )
        formulario.pack(fill="x", pady=(0, 10))

        self.formulario_venta = formulario
        self.venta_usuario_var = formulario.usuario_var
        self.venta_producto_var = formulario.producto_var
        self.venta_cantidad_var = formulario.cantidad_var
        tabla = VentaTableComponent(self.content_frame)
        tabla.pack(fill="both", expand=True)

        self.tabla_ventas = tabla
        self.cargar_tabla_ventas()

    def cargar_tabla_ventas(self):
        if hasattr(self, "tabla_ventas"):
            for item in self.tabla_ventas.get_children():
                self.tabla_ventas.delete(item)

            for venta in self.servicio.listar_ventas():
                self.tabla_ventas.insert(
                    "",
                    tk.END,
                    values=(venta.id, venta.usuario, venta.producto_nombre, venta.cantidad, venta.fecha, f"${venta.total:.2f}")
                )

    def registrar_venta(self):
        usuario = self.venta_usuario_var.get().strip()
        opcion_producto = self.venta_producto_var.get()
        producto_id = self.formulario_venta.productos_por_opcion.get(opcion_producto)
        cantidad = self.venta_cantidad_var.get().strip()

        if not usuario or producto_id is None or not cantidad:
            messagebox.showwarning("Advertencia", "Seleccione un usuario y un producto e indique la cantidad.")
            return

        try:
            venta = self.servicio.registrar_venta(usuario, producto_id, cantidad)
            messagebox.showinfo(
                "Venta registrada",
                f"Venta #{venta.id} registrada para {venta.usuario}: {venta.producto_nombre} x{venta.cantidad} - Total ${venta.total:.2f}",
            )
            self.venta_cantidad_var.set("")
            self.cargar_tabla_ventas()
            self.formulario_venta.actualizar_opciones(
                self.servicio.listar_usuarios(),
                self.servicio.listar_productos(),
            )
        except ValueError as error:
            messagebox.showerror("Error en la venta", str(error))

    def mostrar_usuarios(self):
        if self.usuario_actual is None or not self.servicio.usuario_es_administrador(self.usuario_actual.usuario):
            messagebox.showwarning("Acceso restringido", "Solo el administrador puede gestionar usuarios.")
            self.mostrar_productos()
            return

        self.limpiar_contenido()

        titulo = ttk.Label(self.content_frame, text="Gestión de usuarios", font=("Segoe UI", 14, "bold"))
        titulo.pack(anchor="w", pady=(0, 10))

        formulario = UsuarioFormComponent(
            self.content_frame,
            self.registrar_usuario,
            self.actualizar_usuario,
            self.eliminar_usuario,
            self.limpiar_formulario_usuario,
            self.on_rol_cambiado,
        )
        formulario.pack(fill="x", pady=(0, 10))

        self.usuario_form = formulario
        self.usuario_id_var = formulario.id_var
        self.usuario_nombre_var = formulario.nombre_var
        self.usuario_usuario_var = formulario.usuario_var
        self.usuario_password_var = formulario.password_var
        self.usuario_rol_var = formulario.rol_var
        self.usuario_rol_combo = formulario.rol_combo

        self.usuario_form.bind("<Return>", self.on_enter_registrar)
        self.usuario_form.bind("<Escape>", self.on_escape_limpiar)

        self.tabla_usuarios = UsuarioTableComponent(self.content_frame)
        self.tabla_usuarios.bind("<<TreeviewSelect>>", self.cargar_usuario_en_formulario)
        self.tabla_usuarios.pack(fill="both", expand=True)

        self.cargar_tabla_usuarios()

    def cargar_tabla_usuarios(self):
        if hasattr(self, "tabla_usuarios"):
            for item in self.tabla_usuarios.get_children():
                self.tabla_usuarios.delete(item)

            for usuario in self.servicio.listar_usuarios():
                self.tabla_usuarios.insert(
                    "",
                    tk.END,
                    values=(usuario.id, usuario.nombre, usuario.usuario, usuario.rol),
                )

    def limpiar_formulario_usuario(self):
        if hasattr(self, "usuario_id_var"):
            self.usuario_id_var.set("")
        if hasattr(self, "usuario_nombre_var"):
            self.usuario_nombre_var.set("")
        if hasattr(self, "usuario_usuario_var"):
            self.usuario_usuario_var.set("")
        if hasattr(self, "usuario_password_var"):
            self.usuario_password_var.set("")
        if hasattr(self, "usuario_rol_var"):
            self.usuario_rol_var.set("Cliente")
        if hasattr(self, "tabla_usuarios"):
            self.tabla_usuarios.selection_remove(self.tabla_usuarios.selection())
        self.usuario_seleccionado_id = None

    def on_enter_registrar(self, event=None):
        self.registrar_usuario()

    def on_escape_limpiar(self, event=None):
        self.limpiar_formulario_usuario()

    def on_rol_cambiado(self, event=None):
        if hasattr(self, "usuario_rol_var"):
            self.usuario_rol_var.set(self.usuario_rol_var.get())

    def cargar_usuario_en_formulario(self, event=None):
        if not hasattr(self, "tabla_usuarios"):
            return

        seleccion = self.tabla_usuarios.selection()
        if not seleccion:
            return

        fila = seleccion[0]
        valores = self.tabla_usuarios.item(fila, "values")
        if not valores:
            return

        usuario_id = valores[0]
        usuario = self.servicio.obtener_usuario_por_id(usuario_id)
        if usuario is None:
            return

        self.usuario_seleccionado_id = usuario.id
        self.usuario_id_var.set(usuario.id)
        self.usuario_nombre_var.set(usuario.nombre)
        self.usuario_usuario_var.set(usuario.usuario)
        self.usuario_password_var.set(usuario.password)
        self.usuario_rol_var.set(usuario.rol)

    def registrar_usuario(self):
        try:
            usuario = self.servicio.registrar_usuario({
                "nombre": self.usuario_nombre_var.get(),
                "usuario": self.usuario_usuario_var.get(),
                "password": self.usuario_password_var.get(),
                "rol": self.usuario_rol_var.get(),
            })
            messagebox.showinfo("Usuario registrado", f"Se registró correctamente a {usuario.nombre}.")
            self.limpiar_formulario_usuario()
            self.cargar_tabla_usuarios()
        except ValueError as error:
            messagebox.showerror("Error al registrar usuario", str(error))

    def actualizar_usuario(self):
        if self.usuario_seleccionado_id is None:
            messagebox.showwarning("Advertencia", "Seleccione un usuario de la tabla para actualizar.")
            return

        try:
            usuario = self.servicio.actualizar_usuario(self.usuario_seleccionado_id, {
                "nombre": self.usuario_nombre_var.get(),
                "usuario": self.usuario_usuario_var.get(),
                "password": self.usuario_password_var.get(),
                "rol": self.usuario_rol_var.get(),
            })
            messagebox.showinfo("Usuario actualizado", f"Se actualizó a {usuario.nombre}.")
            self.limpiar_formulario_usuario()
            self.cargar_tabla_usuarios()
        except ValueError as error:
            messagebox.showerror("Error al actualizar usuario", str(error))

    def eliminar_usuario(self):
        if self.usuario_seleccionado_id is None:
            messagebox.showwarning("Advertencia", "Seleccione un usuario para eliminar.")
            return

        usuario = self.servicio.obtener_usuario_por_id(self.usuario_seleccionado_id)
        if usuario is None:
            messagebox.showwarning("No encontrado", "El usuario ya no existe.")
            return

        if usuario.rol == "Administrador":
            messagebox.showwarning("Acción restringida", "No se puede eliminar a un usuario administrador.")
            return

        confirmar = messagebox.askyesno("Confirmar eliminación", f"¿Desea eliminar a {usuario.nombre} ({usuario.usuario})?")
        if not confirmar:
            return

        try:
            self.servicio.eliminar_usuario(self.usuario_seleccionado_id)
            messagebox.showinfo("Usuario eliminado", f"Se eliminó a {usuario.nombre}.")
            self.limpiar_formulario_usuario()
            self.cargar_tabla_usuarios()
        except ValueError as error:
            messagebox.showerror("Error al eliminar usuario", str(error))

    def mostrar_productos(self):
        self.limpiar_contenido()

        titulo = ttk.Label(self.content_frame, text="Gestión de productos", font=("Segoe UI", 14, "bold"))
        titulo.pack(anchor="w", pady=(0, 10))

        formulario = ProductoFormComponent(
            self.content_frame,
            self.registrar_producto,
            self.cargar_producto_por_id,
            self.actualizar_producto,
            self.eliminar_producto,
            self.limpiar_campos_producto,
        )
        formulario.pack(fill="x", pady=(0, 10))

        self.producto_id_var = formulario.id_var
        self.producto_nombre_var = formulario.nombre_var
        self.producto_precio_var = formulario.precio_var
        self.producto_cantidad_var = formulario.cantidad_var
        self.tabla_productos = ProductoTableComponent(self.content_frame)
        self.tabla_productos.pack(fill="both", expand=True)

        self.cargar_tabla_productos()

    def cargar_tabla_productos(self):
        for item in self.tabla_productos.get_children():
            self.tabla_productos.delete(item)

        for producto in self.servicio.listar_productos():
            self.tabla_productos.insert(
                "",
                tk.END,
                values=(producto.id, producto.nombre, producto.precio, producto.cantidad)
            )

    def limpiar_campos_producto(self):
        self.producto_id_var.set("")
        self.producto_nombre_var.set("")
        self.producto_precio_var.set("")
        self.producto_cantidad_var.set("")

    def registrar_producto(self):
        try:
            producto = self.servicio.registrar_producto({
                "id": self.producto_id_var.get(),
                "nombre": self.producto_nombre_var.get(),
                "precio": self.producto_precio_var.get(),
                "cantidad": self.producto_cantidad_var.get()
            })
            messagebox.showinfo("Registro exitoso", f"Producto registrado: {producto.nombre}")
            self.limpiar_campos_producto()
            self.cargar_tabla_productos()
        except ValueError as error:
            messagebox.showerror("Error", str(error))

    def cargar_producto_por_id(self):
        producto_id = self.producto_id_var.get().strip()
        if not producto_id:
            messagebox.showwarning("Advertencia", "Ingrese un identificador para buscar el producto.")
            return

        producto = self.servicio.obtener_producto_por_id(producto_id)
        if producto is None:
            messagebox.showwarning("No encontrado", f"No existe un producto con el id {producto_id}.")
            return

        self.producto_nombre_var.set(producto.nombre)
        self.producto_precio_var.set(producto.precio)
        self.producto_cantidad_var.set(producto.cantidad)

    def actualizar_producto(self):
        producto_id = self.producto_id_var.get().strip()
        if not producto_id:
            messagebox.showwarning("Advertencia", "Ingrese un identificador para actualizar.")
            return

        try:
            producto = self.servicio.actualizar_producto(producto_id, {
                "nombre": self.producto_nombre_var.get(),
                "precio": self.producto_precio_var.get(),
                "cantidad": self.producto_cantidad_var.get()
            })
            messagebox.showinfo("Actualización exitosa", f"Producto actualizado: {producto.nombre}")
            self.cargar_tabla_productos()
        except ValueError as error:
            messagebox.showerror("Error", str(error))

    def eliminar_producto(self):
        producto_id = self.producto_id_var.get().strip()
        if not producto_id:
            messagebox.showwarning("Advertencia", "Ingrese un identificador para eliminar.")
            return

        try:
            self.servicio.eliminar_producto(producto_id)
            messagebox.showinfo("Eliminación exitosa", f"Se eliminó el producto con id {producto_id}.")
            self.limpiar_campos_producto()
            self.cargar_tabla_productos()
        except ValueError as error:
            messagebox.showerror("Error", str(error))

import tkinter as tk
from tkinter import messagebox, ttk


class LoginView(tk.Frame):
    def __init__(self, master, servicio, cambiar_vista):
        super().__init__(master, bg="#eef2f7")
        self.servicio = servicio
        self.cambiar_vista = cambiar_vista

        container = ttk.Frame(self, padding=30)
        container.pack(expand=True)

        card = ttk.Frame(container, padding=25)
        card.pack(expand=True)

        ttk.Label(card, text="Restaurante App", font=("Segoe UI", 18, "bold")).grid(
            row=0, column=0, columnspan=2, pady=(0, 20)
        )
        ttk.Label(card, text="Usuario:").grid(row=1, column=0, padx=10, pady=8, sticky="w")
        self.usuario_entry = ttk.Entry(card, width=25)
        self.usuario_entry.grid(row=1, column=1, padx=10, pady=8)

        ttk.Label(card, text="Contraseña:").grid(row=2, column=0, padx=10, pady=8, sticky="w")
        self.password_entry = ttk.Entry(card, width=25, show="*")
        self.password_entry.grid(row=2, column=1, padx=10, pady=8)

        ttk.Button(card, text="Ingresar", command=self.ingresar).grid(
            row=3, column=0, columnspan=2, pady=(15, 0), sticky="ew"
        )

        self.password_entry.bind("<Return>", lambda event: self.ingresar())
        self.usuario_entry.focus_set()

    def ingresar(self):
        usuario = self.usuario_entry.get()
        password = self.password_entry.get()
        usuario_actual = self.servicio.obtener_usuario_por_credenciales(usuario, password)
        if usuario_actual is not None:
            self.cambiar_vista("main", usuario_actual)
        else:
            messagebox.showerror("Error de acceso", "Credenciales incorrectas")

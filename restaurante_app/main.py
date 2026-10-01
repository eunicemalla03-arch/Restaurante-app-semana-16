import tkinter as tk
from pathlib import Path

from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView
from ui.main_view import MainView


class App(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Restaurante App")
        self.geometry("1100x700")
        self.minsize(900, 600)
        self.resizable(True, True)

        assets = Path(__file__).resolve().parent / "assets"
        for nombre in ("logo.png", "logotipo.png", "icono.png"):
            ruta_logo = assets / nombre
            if ruta_logo.is_file():
                try:
                    self._logo = tk.PhotoImage(file=str(ruta_logo))
                    self.iconphoto(True, self._logo)
                    break
                except tk.TclError:
                    continue

        self.servicio = RestauranteServicio()
        self.vista_actual = None
        self.cambiar_vista("login")

    def cambiar_vista(self, vista, usuario_actual=None):
        if vista == "login":
            nueva_vista = LoginView(
                self,
                self.servicio,
                self.cambiar_vista
            )
        elif vista == "main":
            nueva_vista = MainView(
                master=self,
                servicio=self.servicio,
                cambiar_vista=self.cambiar_vista,
                usuario_actual=usuario_actual,
            )
        else:
            raise ValueError(f"Vista no reconocida: {vista}")

        if self.vista_actual is not None:
            self.vista_actual.destroy()

        self.vista_actual = nueva_vista
        self.vista_actual.pack(fill="both", expand=True)


if __name__ == "__main__":
    app = App()
    app.mainloop()
   
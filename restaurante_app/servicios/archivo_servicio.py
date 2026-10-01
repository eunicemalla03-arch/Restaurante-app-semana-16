import json
import os


class ArchivoServicio:
    @staticmethod
    def _resolver_ruta(ruta):
        ruta_relativa = os.path.abspath(ruta)
        if os.path.exists(ruta_relativa):
            return ruta_relativa

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.abspath(os.path.join(base_dir, ruta))

    @staticmethod
    def cargar_datos(ruta):
        """Lee un archivo JSON y devuelve su contenido como lista o diccionario."""
        ruta_absoluta = ArchivoServicio._resolver_ruta(ruta)

        if not os.path.exists(ruta_absoluta):
            return []

        with open(ruta_absoluta, "r", encoding="utf-8") as archivo:
            return json.load(archivo)

    @staticmethod
    def guardar_datos(ruta, datos):
        """Guarda datos en formato JSON en la ruta indicada."""
        ruta_absoluta = ArchivoServicio._resolver_ruta(ruta)
        os.makedirs(os.path.dirname(ruta_absoluta), exist_ok=True)

        with open(ruta_absoluta, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=2)

    @staticmethod
    def guardar_ventas(ruta, ventas):
        ruta_absoluta = ArchivoServicio._resolver_ruta(ruta)
        os.makedirs(os.path.dirname(ruta_absoluta), exist_ok=True)

        with open(ruta_absoluta, "w", encoding="utf-8") as archivo:
            json.dump(ventas, archivo, ensure_ascii=False, indent=2)

import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from servicios.restaurante_servicio import RestauranteServicio


class RestauranteServicioTests(unittest.TestCase):
    def test_producto_crud_y_persistencia(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            datos_dir = os.path.join(tmp_dir, "datos")
            os.makedirs(datos_dir)

            with open(os.path.join(datos_dir, "productos.json"), "w", encoding="utf-8") as archivo:
                json.dump([
                    {"id": 1, "nombre": "Hamburguesa", "precio": 5.0, "cantidad": 20}
                ], archivo)

            with open(os.path.join(datos_dir, "usuarios.json"), "w", encoding="utf-8") as archivo:
                json.dump([
                    {"usuario": "admin", "password": "admin"}
                ], archivo)

            with open(os.path.join(datos_dir, "ventas.json"), "w", encoding="utf-8") as archivo:
                json.dump([], archivo)

            cwd_actual = os.getcwd()
            os.chdir(tmp_dir)
            try:
                servicio = RestauranteServicio()

                self.assertTrue(servicio.validar_acceso("admin", "admin"))
                self.assertEqual(servicio.obtener_producto_por_id(1).nombre, "Hamburguesa")

                servicio.registrar_producto({"id": 2, "nombre": "Pizza", "precio": 10.0, "cantidad": 8})
                self.assertEqual(len(servicio.listar_productos()), 2)

                servicio.actualizar_producto(2, {"nombre": "Pizza especial", "precio": 12.5, "cantidad": 10})
                actualizado = servicio.obtener_producto_por_id(2)
                self.assertEqual(actualizado.nombre, "Pizza especial")

                servicio.eliminar_producto(1)
                self.assertIsNone(servicio.obtener_producto_por_id(1))

                with open(os.path.join(datos_dir, "productos.json"), "r", encoding="utf-8") as archivo:
                    data = archivo.read()

                self.assertIn('"nombre": "Pizza especial"', data)
            finally:
                os.chdir(cwd_actual)

    def test_registrar_venta_descuenta_stock_y_persiste(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            datos_dir = os.path.join(tmp_dir, "datos")
            os.makedirs(datos_dir)

            with open(os.path.join(datos_dir, "productos.json"), "w", encoding="utf-8") as archivo:
                json.dump([
                    {"id": 1, "nombre": "Hamburguesa", "precio": 5.0, "cantidad": 20}
                ], archivo)

            with open(os.path.join(datos_dir, "usuarios.json"), "w", encoding="utf-8") as archivo:
                json.dump([
                    {"usuario": "admin", "password": "admin"}
                ], archivo)

            with open(os.path.join(datos_dir, "ventas.json"), "w", encoding="utf-8") as archivo:
                json.dump([], archivo)

            cwd_actual = os.getcwd()
            os.chdir(tmp_dir)
            try:
                servicio = RestauranteServicio()
                venta = servicio.registrar_venta("admin", 1, 2)

                self.assertEqual(venta.producto_id, 1)
                self.assertEqual(venta.usuario, "admin")
                self.assertEqual(venta.cantidad, 2)
                self.assertEqual(venta.total, 10.0)
                self.assertNotEqual(venta.fecha, "Fecha no disponible")
                self.assertEqual(servicio.obtener_producto_por_id(1).cantidad, 18)

                with open(os.path.join(datos_dir, "ventas.json"), "r", encoding="utf-8") as archivo:
                    ventas = json.load(archivo)

                self.assertEqual(len(ventas), 1)
                self.assertEqual(ventas[0]["usuario"], "admin")
                self.assertIn("fecha", ventas[0])

                servicio_recargado = RestauranteServicio()
                venta_recargada = servicio_recargado.listar_ventas()[0]
                self.assertEqual(venta_recargada.usuario, "admin")
                self.assertEqual(venta_recargada.producto_nombre, "Hamburguesa")
                self.assertEqual(venta_recargada.fecha, venta.fecha)
            finally:
                os.chdir(cwd_actual)

    def test_usuarios_con_roles_y_crud(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            datos_dir = os.path.join(tmp_dir, "datos")
            os.makedirs(datos_dir)

            with open(os.path.join(datos_dir, "productos.json"), "w", encoding="utf-8") as archivo:
                json.dump([], archivo)

            with open(os.path.join(datos_dir, "usuarios.json"), "w", encoding="utf-8") as archivo:
                json.dump([
                    {"id": 1, "nombre": "Admin General", "usuario": "admin", "password": "admin", "rol": "Administrador"},
                    {"id": 2, "nombre": "Luis Mesa", "usuario": "luis", "password": "123", "rol": "Empleado"}
                ], archivo)

            with open(os.path.join(datos_dir, "ventas.json"), "w", encoding="utf-8") as archivo:
                json.dump([], archivo)

            cwd_actual = os.getcwd()
            os.chdir(tmp_dir)
            try:
                servicio = RestauranteServicio()

                self.assertTrue(servicio.validar_acceso("admin", "admin"))
                self.assertTrue(servicio.usuario_es_administrador("admin"))
                self.assertFalse(servicio.usuario_es_administrador("luis"))

                usuario = servicio.registrar_usuario({
                    "nombre": "Ana Cliente",
                    "usuario": "ana",
                    "password": "456",
                    "rol": "Cliente"
                })
                self.assertEqual(usuario.rol, "Cliente")
                self.assertEqual(servicio.obtener_usuario_por_id(usuario.id).usuario, "ana")

                servicio.actualizar_usuario(usuario.id, {"nombre": "Ana García", "rol": "Cliente"})
                self.assertEqual(servicio.obtener_usuario_por_id(usuario.id).nombre, "Ana García")

                servicio.eliminar_usuario(usuario.id)
                self.assertIsNone(servicio.obtener_usuario_por_id(usuario.id))

                with open(os.path.join(datos_dir, "usuarios.json"), "r", encoding="utf-8") as archivo:
                    usuarios = json.load(archivo)

                self.assertIn("rol", usuarios[0])
                self.assertEqual(len(usuarios), 2)
            finally:
                os.chdir(cwd_actual)


if __name__ == "__main__":
    unittest.main()

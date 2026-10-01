# Restaurante App - Semana 16
Estudiante:Eunice Belen Malla Coro

Aplicación de escritorio desarrollada en Python con Tkinter para gestionar la operación del restaurante, manteniendo la arquitectura modular y ampliando la sección de usuarios con eventos, validación por roles y persistencia en JSON.

## Objetivo de la Semana 16

Se conserva la base del proyecto anterior y se evoluciona la gestión de usuarios con:

- Registro, consulta, actualización y eliminación desde la interfaz.
- Atributo `rol` en el modelo `Usuario` con valores `Administrador`, `Empleado` y `Cliente`.
- Restricción para que solo el administrador pueda acceder a la gestión administrativa de usuarios.
- Uso de `Treeview` con selección y carga automática del usuario al formulario.
- Manejo de eventos `bind()` para `<<TreeviewSelect>>`, `<Return>` y `<Escape>`.
- Uso de `Combobox` con evento `<<ComboboxSelected>>` para cambiar el rol.
- Botones con `command=` para registrar, actualizar, eliminar y limpiar.
- Persistencia y validaciones centralizadas en `RestauranteServicio`.

## Estructura del proyecto

```text
restaurante_app/
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
├── ui/
│   ├── __init__.py
│   ├── componentes.py
│   ├── login_view.py
│   └── main_view.py
├── assets/
│   ├── logotipo.xbm
│   ├── productos.xbm
│   ├── usuarios.xbm
│   └── ventas.xbm
├── tests/
│   └── test_restaurante_servicio.py
├── main.py
├── README.md
└── __pycache__/
```

## Arquitectura y responsabilidades

### Modelos
Los modelos representan entidades del dominio:

- `Usuario` con `id`, `nombre`, `usuario`, `password` y `rol`.
- `Producto` con información del inventario.
- `Venta` con registro de movimiento comercial.

### Servicios
Se mantiene la lógica de negocio en `RestauranteServicio`, y la escritura/lectura JSON en `ArchivoServicio`.

Esto evita que la interfaz lea o escriba archivos directamente y conserva la separación de responsabilidades.

### Interfaz
La capa visual responde a eventos y coordina la interacción del usuario:

- `LoginView` valida el acceso con `RestauranteServicio`.
- `MainView` administra la navegación y la vista activa.
- `UsuarioFormComponent` y `UsuarioTableComponent` gestionan el formulario y la tabla de usuarios.
- `Treeview` y `Combobox` usan `bind()` para responder a selecciones y cambios.
- Los callbacks reusan la lógica del servicio, sin duplicar operaciones dentro de la interfaz.

## Flujo de interacción implementado

El flujo principal de la Semana 16 sigue este patrón:

1. El usuario interactúa con la vista.
2. Se dispara un evento (`<<TreeviewSelect>>`, `<Return>`, `<Escape>`, `<<ComboboxSelected>>`).
3. El callback ejecuta `bind()` para atender la acción.
4. La interfaz consulta o envía datos a `RestauranteServicio`.
5. El servicio valida reglas de negocio y persiste en `usuarios.json`.
6. La vista actualiza la tabla y responde visualmente al usuario.

## Gestión de usuarios

La sección de usuarios permite:

- crear usuarios con nombre, usuario, contraseña y rol
- listar usuarios en un `Treeview`
- seleccionar una fila para cargar los datos al formulario
- actualizar la información del usuario seleccionado
- eliminar un usuario con confirmación previa
- impedir la eliminación del usuario administrador
- reutilizar el registro al presionar `Enter`
- limpiar el formulario con `Escape`

## Ejecución

```bash
python main.py
```

## Credenciales de ejemplo

La aplicación incluye usuarios con roles iniciales en `datos/usuarios.json`:

- `admin / admin` → Administrador
- `cajero / cajero` → Empleado
- `cliente / cliente` → Cliente

## Validación

Se incluye una prueba unitaria para verificar la lógica del servicio:

```bash
python -m unittest discover -s tests -v
```

La validación cubre:

- acceso autenticado
- gestión de usuarios con roles
- actualización y eliminación de registros
- persistencia de los datos en JSON
- continuidad con productos y ventas

## Observación

La aplicación mantiene la separación clara entre interfaz, negocio y persistencia, integrando la evolución de la Semana 16 sin reemplazar la estructura modular desarrollada en semanas anteriores.

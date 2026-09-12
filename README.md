# FarmaDelivery

[![Django](https://img.shields.io/badge/Django-5.2.7-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Estado](https://img.shields.io/badge/Estado-en%20desarrollo-important)]()

Plataforma web de venta y entrega de medicamentos. Permite buscar productos, subir recetas médicas, hacer pedidos y realizar el seguimiento en tiempo real de la entrega.

Proyecto académico de la materia **Ingeniería de Software (2025)**. Desarrollado con **Django** y desplegable en cualquier entorno local.

---

## Funcionalidades

- **Clientes**
  - Búsqueda y filtrado de medicamentos (por nombre, categoría, farmacia y obra social).
  - Filtro de cercanía: solo farmacias a menos de 2 km de tu dirección.
  - Compra con retiro en farmacia o envío a domicilio.
  - Subida de recetas médicas para medicamentos controlados.
  - Descuentos automáticos por obra social.
  - Seguimiento del pedido en tiempo real (ubicación del repartidor).

- **Farmacias**
  - Panel de gestión de pedidos, inventario, precios y cuenta.
  - Confirmación de recetas y preparación de pedidos.
  - Envío de estados a repartidores.
  - Alta y baja de productos con imagen y código de barras.

- **Repartidores**
  - Panel con pedidos cercanos disponibles (radio de 2 km).
  - Aceptar, rechazar o marcar pedidos como entregados.
  - Actualización de ubicación en tiempo real y modo "ubicación fija" para pruebas.

- **Administración**
  - Panel de Django admin (`/admin/`) para aprobar farmacias y repartidores, gestionar obras sociales, descuentos y todo el catálogo.

## Stack tecnológico

| Tecnología | Uso |
| --- | --- |
| [Django](https://www.djangoproject.com/) 5.2.7 | Framework web |
| [SQLite](https://www.sqlite.org/) | Base de datos (desarrollo) |
| [Bootstrap](https://getbootstrap.com/) 5.3 | Estilos e interfaz |
| [Font Awesome](https://fontawesome.com/) | Iconografía |
| [Nominatim / OpenStreetMap](https://nominatim.openstreetmap.org/) | Geocodificación de direcciones (sin API key) |
| `requests` / `Pillow` | HTTP y manejo de imágenes |

## Estructura del proyecto

```
proyecto-web-facultad-2025/
├── core/                        # Aplicación principal del negocio
│   ├── migrations/              # Migraciones de la base de datos
│   ├── templates/               # Plantillas HTML (core/ y registration/)
│   ├── admin.py                 # Configuración del panel de administración
│   ├── auth_backends.py         # Login con DNI como username
│   ├── auth_views.py            # Vista de login personalizada
│   ├── forms.py                 # Formularios (búsquedas, registros, direcciones)
│   ├── models.py                # Modelos (Cliente, Farmacia, Repartidor, Pedido, ...)
│   ├── tests.py                 # Tests automatizados
│   ├── urls.py                  # Rutas de la aplicación
│   ├── utils.py                 # Utilidades (geocodificación)
│   └── views.py                 # Vistas
├── FarmaDeliveryProject/        # Configuración del proyecto Django
│   └── settings.py              # Ajustes del proyecto
├── static/                      # Archivos estáticos (CSS y JS)
├── media/                       # Archivos subidos por usuarios (imágenes, recetas)
├── crear_datos_la_plata.py      # Script de datos de prueba (limpia la BD)
├── manage.py                    # Punto de entrada de Django
└── requirements.txt             # Dependencias del proyecto
```

> `staticfiles/` y `db.sqlite3` se generan en tiempo de ejecución y están excluidos del repositorio.

## Requisitos previos

- **Python 3.10 o superior** (recomendado 3.12 / 3.13)
- `git`

## Puesta en marcha

Desde la raíz del repositorio:

```bash
# 1. Crear y activar un entorno virtual
python -m venv venv

# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Aplicar migraciones (crea la base de datos)
python manage.py migrate

# 4. Crear un usuario administrador
python manage.py createsuperuser

# 5. (Opcional) Cargar datos de ejemplo
python crear_datos_la_plata.py

# 6. Levantar el servidor de desarrollo
python manage.py runserver
```

Abrí `http://127.0.0.1:8000/` en tu navegador.

### Datos de ejemplo

El script `crear_datos_la_plata.py` limpia por completo la base de datos y crea:

- 3 farmacias en direcciones de **La Plata** con productos.
- Un cliente y un repartidor de prueba.
- Usuarios y contraseñas de acceso, que se imprimen por consola.

> Ojo: el script **borra todos los datos existentes** antes de cargar los nuevos.
> En Windows, si aparece un error de codificación (emojis/acentos), correrlo con `PYTHONIOENCODING=utf-8`:
> `set PYTHONIOENCODING=utf-8 && python crear_datos_la_plata.py`

## Roles y flujo de referencia

| Rol | Acceso | Alta |
| --- | --- | --- |
| Cliente | `/accounts/signup/cliente/` | Inmediata |
| Farmacia | `/accounts/signup/farmacia/` | Requiere aprobación del admin |
| Repartidor | `/accounts/signup/repartidor/` | Requiere aprobación del admin |
| Admin | `/admin/` | `createsuperuser` |

- El **login** se realiza con el **DNI** como nombre de usuario.
- Las farmacias y repartidores quedan **pendientes de aprobación** hasta que un administrador los habilite desde `/admin/`.

## Pruebas

```bash
python manage.py test core
```

Los tests cubren el modelo `Direccion` (cálculo de distancias, `__str__`), el flujo de login (acceso a `/`, login válido e inválido) y la configuración de farmacia (vistas de precios/descuentos y cuenta).

## Configuración

- **Email**: por defecto se usa el *console backend* (los correos se muestran en consola). Para enviar mails reales, configurar `EMAIL_HOST`, `EMAIL_HOST_USER` y `EMAIL_HOST_PASSWORD` en `FarmaDeliveryProject/settings.py`.
- **Geocodificación**: se usa el servicio gratuito de Nominatim (OpenStreetMap), sin necesidad de API key.
- **Seguridad**: la configuración se lee de variables de entorno, con valores por defecto aptos para desarrollo:

| Variable | Por defecto | Descripción |
| --- | --- | --- |
| `DJANGO_SECRET_KEY` | (obligatoria en producción) | Clave secreta de Django |
| `DJANGO_DEBUG` | `True` | Habilita/deshabilita el modo debug |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1` | Hosts permitidos (separados por coma) |

> Para producción: definir `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False` y `DJANGO_ALLOWED_HOSTS` con el dominio. Si `DJANGO_DEBUG=False` y no se define `DJANGO_SECRET_KEY`, la app **no arranca** (protección contra claves por defecto).

Ejemplo:

```bash
# Windows (PowerShell)
$env:DJANGO_SECRET_KEY = "clave-secreta"
$env:DJANGO_DEBUG = "False"
$env:DJANGO_ALLOWED_HOSTS = "midominio.com,www.midominio.com"

# Linux / macOS
export DJANGO_SECRET_KEY="clave-secreta"
export DJANGO_DEBUG="False"
export DJANGO_ALLOWED_HOSTS="midominio.com,www.midominio.com"
```

## Notas de desarrollo

- Las coordenadas de las direcciones se autocompletan contra Nominatim cuando el cliente guarda su perfil.
- Los cambios en el esquema requieren generar la migración correspondiente: `python manage.py makemigrations core`.
- Los paneles de farmacia/repartidor son páginas independientes (layout propio con `farmacia.css`/`repartidor.css`). Se prevé integrarlos a `base.html` en una iteración futura; en ese momento se definirá cómo condicionar el head/navbar por rol.
- No commitear `media/`, `staticfiles/`, `db.sqlite3` ni archivos `.env`.

## Licencia

Proyecto con fines académicos. Uso libre para fines educativos.
# GA7-220501096-AA2-EV02 — TallerExpress

**Módulo Orden de Servicio**, implementado en Django siguiendo el patrón
Modelo–Plantilla–Vista (MTV), como evidencia GA7-220501096-AA2-EV02 del
programa Análisis y Desarrollo de Software (ADSO) — SENA.

## Descripción

Aplicación web para gestionar órdenes de servicio de un taller: creación,
listado, edición y eliminación de órdenes, asociadas a un cliente, un
vehículo (que debe pertenecer a ese cliente) y opcionalmente un mecánico.

## Funcionalidades

- Listado de órdenes con paginación (10 por página).
- Creación de órdenes (formulario con validación del lado del servidor).
- Edición de órdenes existentes.
- Eliminación mediante página de confirmación en el servidor (GET
  confirma, POST con CSRF elimina).
- Validación: el vehículo debe pertenecer al cliente seleccionado.
- Número de orden generado automáticamente (`OS-101`, `OS-102`, ...).
- Mensajes de éxito/error visibles tras cada operación.
- Pruebas automatizadas de modelo, formulario, vistas y del comando de
  datos de prueba.
- Comando `generar_datos_prueba` para poblar la base de datos con datos
  realistas (100 órdenes por defecto), útil para demostrar la paginación
  con volumen real.

## Requisitos

- Python 3.11 o superior.
- pip (incluido con Python).
- Git (para el versionamiento y la publicación en GitHub).
- MySQL/Laragon **solo** si se desea probar con MySQL (opcional, ver más
  abajo). No es necesario para SQLite.

## Instalación y ejecución (resumen)

```bat
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py test
python manage.py runserver
```

Abrir en el navegador: `http://127.0.0.1:8000/ordenes/`

Para instrucciones detalladas paso a paso en Windows (incluyendo qué hacer
si algo falla), ver `DOCUMENTOS/GUIA_INSTALACION_WINDOWS.md`.

## Entorno virtual

Se recomienda usar siempre un entorno virtual (`.venv`) para no mezclar
dependencias con otros proyectos de Python instalados en el equipo. El
entorno virtual **no** se incluye en el repositorio ni en el ZIP de
entrega (ver `.gitignore`).

## Instalación de dependencias

`requirements.txt` instala únicamente `Django`, suficiente para ejecutar
el proyecto con SQLite (configuración por defecto). El paquete
`mysqlclient` está separado en `requirements-mysql.txt` porque solo se
necesita si se va a usar MySQL, y en Windows puede requerir herramientas
adicionales (ver sección MySQL).

## Migraciones

```bat
python manage.py makemigrations
python manage.py migrate
```

El proyecto ya incluye la migración inicial (`ordenes/migrations/0001_initial.py`).
Si el modelo no ha cambiado, `makemigrations` no debería generar nada
nuevo — eso es correcto y no indica ningún error.

## Pruebas automatizadas

```bat
python manage.py test
```

La suite cubre: generación del número de orden, validaciones del
formulario (campos obligatorios, vehículo de otro cliente), el flujo CRUD
completo, la confirmación de eliminación, la paginación y el comando de
datos de prueba.

## Datos de prueba

```bat
python manage.py generar_datos_prueba
```

Crea 30 clientes, sus vehículos, 8 mecánicos y **100 órdenes de servicio**
de forma reproducible (útil para probar la paginación con volumen real).
Ver más opciones (`--ordenes`, `--reset`) en
`DOCUMENTOS/GUIA_INSTALACION_WINDOWS.md`.

## Estructura del proyecto

```
DIEGOBARBOSA_AA2_EV02/
├── manage.py
├── requirements.txt              # Dependencia mínima (Django) para SQLite
├── requirements-mysql.txt        # Dependencia opcional para MySQL
├── ejecutar_proyecto.bat         # Script de arranque rápido en Windows
├── .gitignore
├── tallerexpress/                # Configuración del proyecto Django
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py / asgi.py
├── ordenes/                      # App principal (módulo Orden de Servicio)
│   ├── models.py                 # Cliente, Vehiculo, Mecanico, OrdenServicio
│   ├── forms.py                  # Formulario con validación cliente–vehículo
│   ├── views.py                  # CRUD (listar, crear, editar, eliminar)
│   ├── urls.py
│   ├── tests.py                  # Pruebas automatizadas
│   ├── migrations/
│   ├── management/commands/
│   │   └── generar_datos_prueba.py   # Comando para poblar datos de prueba
│   └── templates/ordenes/
│       ├── base.html
│       ├── lista.html
│       ├── formulario.html
│       └── eliminar_confirmar.html
└── DOCUMENTOS/
    ├── Documento_Entrega.md
    ├── Plan_de_Pruebas.md
    ├── GUIA_INSTALACION_WINDOWS.md
    ├── GUIA_EVIDENCIAS.md
    ├── CHECKLIST_FINAL.md
    └── Estado_Construccion.txt
```

## Configuración SQLite (por defecto)

No requiere configuración adicional. Al ejecutar `python manage.py migrate`
se crea automáticamente `db.sqlite3` en la raíz del proyecto (ignorado por
Git).

## Configuración MySQL (opcional, con Laragon)

1. Instalar la dependencia opcional:
   ```bat
   pip install -r requirements-mysql.txt
   ```
2. Definir estas variables de entorno antes de ejecutar `manage.py`:
   ```text
   DB_ENGINE=mysql
   DB_NAME=tallerexpress
   DB_USER=root
   DB_PASSWORD=
   DB_HOST=127.0.0.1
   DB_PORT=3306
   ```
3. Ejecutar `python manage.py migrate` normalmente.

Si `DB_ENGINE` no está definido (o es distinto de `mysql`), el proyecto
usa SQLite automáticamente. Ver detalle completo, incluyendo qué hacer si
`mysqlclient` falla al instalarse, en
`DOCUMENTOS/GUIA_INSTALACION_WINDOWS.md`.

## Comandos Git

```bat
git init
git add .
git commit -m "GA7-220501096-AA2-EV02 - modulo ordenes de servicio"
git branch -M main
git remote add origin URL_REAL_DEL_REPOSITORIO
git push -u origin main
```

Reemplaza `URL_REAL_DEL_REPOSITORIO` por el enlace real del repositorio
creado en GitHub. Ese enlace también debe copiarse en
`DOCUMENTOS/Documento_Entrega.md`.

## Documentación relacionada

- `DOCUMENTOS/GUIA_INSTALACION_WINDOWS.md` — instalación paso a paso desde cero.
- `DOCUMENTOS/Plan_de_Pruebas.md` — casos de prueba manuales.
- `DOCUMENTOS/GUIA_EVIDENCIAS.md` — lista de capturas a tomar.
- `DOCUMENTOS/CHECKLIST_FINAL.md` — checklist de entrega.
- `DOCUMENTOS/Documento_Entrega.md` — documento formal de entrega.

## Importante

El enlace de GitHub, los resultados de `python manage.py test` y las
capturas de pantalla deben ser reales, obtenidos ejecutando el proyecto en
el equipo del aprendiz. Este documento no incluye ningún dato inventado.
# DiegoBabosa_GA7-220501096-AA2-EV02

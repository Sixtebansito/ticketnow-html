# TicketNow - Python Flask Backend & Frontend

Este repositorio contiene la versión dinámica y conectada a base de datos de TicketNow. A diferencia del prototipo inicial estático, esta aplicación cuenta con un backend completo construido en **Python / Flask** y se conecta a una base de datos **Microsoft SQL Server**.

## 🚀 Requisitos

- Python 3.10+
- Docker (para correr la base de datos SQL Server)
- Node.js (opcional, para reconstruir los estilos de TailwindCSS de ser necesario)

## 📦 Instalación

1. **Clonar o descargar el proyecto** y navegar al directorio raíz.
2. **Crear y activar un entorno virtual**:
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Instalar dependencias de Python**:
   ```sh
   pip install -r requirements.txt
   ```
   *(Si `pymssql` da problemas de instalación en macOS, asegúrate de tener `FreeTDS` instalado, p.ej. con `brew install freetds`)*

## 🗄️ Base de Datos

El proyecto asume que estás corriendo una base de datos SQL Server en Docker usando los parámetros especificados en tu script `app.py`.

Para inicializar las tablas de la base de datos (si la base de datos ya está corriendo y accesible en `localhost:1433`):
Abre el shell de python en el entorno virtual (`python3`), e interactúa con SQLAlchemy para crear todo:
```python
from app import app, db
with app.app_context():
    db.create_all()
```

*(Opcional)*: Hay un script de utilidad incluido (`update_images.py`) que puedes usar para poblar datos base en caso de requerirlo.

## 🛠️ Ejecución (Desarrollo)

Para arrancar el servidor web de Flask en modo de desarrollo, simplemente corre:

```sh
python3 app.py
```

El servidor arrancará en `http://localhost:5000` con el modo Debug activado.

## 📁 Estructura del Proyecto

```text
Proyecto_tickets_python
├── app.py                # Lógica del backend, definición de rutas y conexión a BDD
├── models.py             # Modelos de base de datos de SQLAlchemy
├── static/
│   └── css/              # Archivos de salida de Tailwind CSS
├── templates/            # Plantillas HTML dinámicas procesadas por Jinja2
│   ├── admin/            # Paneles de gestión para administradores
│   └── *.html            # Páginas públicas (index, perfil, tienda, etc.)
└── tailwind.config.js    # Configuración de los estilos del framework CSS
```

## 🎨 Modificaciones Principales al Frontend

1. **Dashboard de Administrador**: Gestión de Activar/Desactivar/Agregar eventos, noticias y mercancía.
2. **Temas**: Modo oscuro / claro persistente, modificado nativamente a través de JavaScript y adaptado para Tailwind.
3. **Página de Detalle de Evento**: Renderizado dinámico (`/detalle-evento/<id>`) para mostrar información en vivo de la base de datos.
# ticketnow-html

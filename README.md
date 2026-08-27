# TicketNow - Python Flask Backend & Frontend

Este repositorio contiene la versión dinámica y conectada a base de datos de TicketNow. A diferencia del prototipo inicial estático, esta aplicación cuenta con un backend completo construido en **Python / Flask** y se conecta a una base de datos **PostgreSQL**.

## 🚀 Requisitos

- Python 3.10+
- Base de datos PostgreSQL (p. ej., Neon)

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

## 🗄️ Base de Datos y Configuración

El proyecto está diseñado para conectarse a una base de datos de PostgreSQL (como **Neon** o cualquier instancia local).

1. Crea una base de datos en Postgres.
2. Edita `app.py` para reemplazar la variable `DATABASE_URL` (o exporta la variable de entorno correspondiente) si es necesario (el código usa una cadena predeterminada a un Postgres en `localhost` si no se configura de otra forma o la que está en `app.py`).

Para inicializar la base de datos con las tablas y datos semilla iniciales:
```sh
python seed.py
```
Esto creará las tablas necesarias (Usuarios, Eventos, TipoBoleto, Mercancia, InventarioMercancia, Pedido, SolicitudVip, Noticia, FAQ) y llenará los datos de prueba.

### 🔑 Credenciales de Prueba

Al ejecutar `seed.py`, se crearán automáticamente los siguientes usuarios para pruebas:

- **Administrador**:
  - Email: `admin@ticketnow.com`
  - Contraseña: `admin123`
- **Usuario Normal**:
  - Email: `user@ticketnow.com`
  - Contraseña: `user123`

## 🛠️ Ejecución (Desarrollo)

Para arrancar el servidor web de Flask en modo local:

```sh
python3 app.py
```
El servidor arrancará en `http://localhost:5000` con el modo Debug activado.

## 🚀 Despliegue en Vercel

Este proyecto incluye la configuración necesaria (`vercel.json` y `requirements.txt`) para ser desplegado fácilmente en **Vercel** como funciones sin servidor (Serverless Functions).

### Instrucciones de despliegue:

1. Crea una cuenta gratuita en una base de datos Postgres (ej. [Neon](https://neon.tech/)) y obtén tu **Connection String** (URL de base de datos).
2. Asegúrate de tener una cuenta en [Vercel](https://vercel.com) y conecta tu repositorio de GitHub.
3. Al importar el proyecto en Vercel, ve a **Environment Variables** en la configuración y añade:
   - `DATABASE_URL`: *(pega tu URL de Postgres de Neon)*
4. Haz clic en **Deploy**. Vercel instalará las dependencias y el proyecto estará disponible.
5. *(Opcional)*: Puedes conectarte a tu base de datos de Neon localmente y ejecutar `python seed.py` asegurándote de usar la misma cadena de conexión para inicializar los datos en producción.

## 📁 Estructura del Proyecto

```text
Proyecto_tickets_python
├── app.py                # Aplicación Flask, backend y base de datos
├── models.py             # Definición de tablas SQLAlchemy
├── requirements.txt      # Dependencias
├── seed.py               # Script para poblar la BDD
├── vercel.json           # Configuración para Vercel
├── static/               # Archivos estáticos
└── templates/            # Plantillas HTML
```

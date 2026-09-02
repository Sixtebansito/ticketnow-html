<div align="center">
  <h1>🎟️ TicketNow</h1>
  <p><strong>La plataforma integral para venta de boletos y mercancía oficial de eventos.</strong></p>
</div>

---

## 📖 Sobre el Proyecto

**TicketNow** es una aplicación web moderna diseñada para transformar la experiencia de compra en la industria del entretenimiento. Permite a los usuarios descubrir eventos, comprar boletos, adquirir mercancía oficial (con control de tallas y stock) y gestionar sus compras en un único carrito unificado. 

Originalmente desarrollado en Python con **Flask**, el proyecto cuenta con una sólida arquitectura cliente-servidor, un diseño responsivo impulsado por **Tailwind CSS**, y una base de datos segura en la nube gracias a **Neon (PostgreSQL)**.

> **Nota:** Esta es la versión monolítica original y estable (Backend + Frontend integrado).

## ✨ Características Principales

### Para el Usuario (Cliente)
- 🛒 **Carrito Unificado:** Compra de boletos y mercancía simultáneamente.
- 📱 **Diseño Responsivo:** UI/UX moderna que soporta de forma nativa *Dark Mode*.
- 🛡️ **Seguridad:** Manejo seguro de sesiones y flujos de recuperación de contraseñas vía correo electrónico.
- 🌟 **TicketNow Premium:** Sistema de lealtad para usuarios VIP.

### Para el Administrador
- 📊 **Dashboard Centralizado:** Vista general de operaciones y transacciones.
- 👥 **Gestión de Usuarios:** Panel para consultar clientes, asignar roles de administrador o estados VIP.
- ✔️ **Aprobaciones en Tiempo Real:** Interfaz para validar compras manuales o por transferencia.
- 📅 **Gestión de Contenido:** Publicación dinámica de nuevos Eventos y Noticias.

## 🛠️ Stack Tecnológico

- **Frontend:** HTML5, CSS3, Tailwind CSS, Vanilla JavaScript.
- **Backend:** Python 3.x, Flask, Jinja2.
- **Base de Datos:** PostgreSQL (Neon Tech Serverless).
- **ORM:** SQLAlchemy.
- **Despliegue Recomendado:** Vercel (con variables de entorno nativas).

---

## 🚀 Instalación y Uso Local

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/ticketnow.git
cd ticketnow
```

### 2. Entorno Virtual (Recomendado)
Crea y activa un entorno virtual para aislar las dependencias:
```bash
# Mac/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar Dependencias
Instala todas las librerías necesarias ejecutando:
```bash
pip install -r requirements.txt
```

### 4. Variables de Entorno (`.env`)
Debes configurar las variables de entorno para que la aplicación pueda conectarse a la base de datos y enviar correos. Crea un archivo llamado `.env` en la raíz del proyecto y agrega lo siguiente:

```env
# Clave secreta para la sesión de Flask
SECRET_KEY=una_clave_larga_y_segura_aqui

# Conexión a la base de datos PostgreSQL (Neon)
DATABASE_URL=postgresql://usuario:contraseña@servidor.neon.tech/neondb

# Configuración de Servidor de Correo (Ejemplo: Gmail)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=tu_correo@gmail.com
MAIL_PASSWORD=tu_contraseña_de_aplicacion
```
*(Asegúrate de **nunca** subir este archivo `.env` a GitHub. Ya está incluido en el `.gitignore`).*

### 5. Iniciar la Aplicación
Una vez configurado todo, arranca el servidor de desarrollo:
```bash
python app.py
```
El servidor estará corriendo en: `http://localhost:5001`.

---

## 🔒 Seguridad
- Nunca compartas ni subas tu cadena de conexión a la base de datos (Neon) en archivos públicos. Si sospechas que tu clave ha sido expuesta en el historial de Git, ve a tu panel de Neon y **rota la contraseña** inmediatamente.
- Las contraseñas de los usuarios en la base de datos están encriptadas.

## 📄 Licencia
Este proyecto es de uso privativo y sus derechos pertenecen a sus respectivos creadores.

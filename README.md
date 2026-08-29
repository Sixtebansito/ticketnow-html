# TicketNow - Backend / Legacy Project (Python + Flask)

Este es el proyecto backend original de TicketNow, desarrollado con Flask, SQLite y TailwindCSS. Actualmente, su interfaz de usuario y frontend están siendo migrados a un proyecto moderno con **Astro**.

## Características
- Autenticación de usuarios y roles (VIP, Admin)
- Manejo de Eventos y Entradas (Stock y categorías)
- Gestión de Noticias y Novedades
- API endpoints para chat e integraciones

## Instalación

1. Clona el repositorio y navega a este directorio.
2. Crea un entorno virtual (opcional pero recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Mac/Linux
   ```
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Inicializa la base de datos:
   ```bash
   python init_db.py
   python seed.py
   ```
5. Ejecuta la aplicación:
   ```bash
   python app.py
   ```

El servidor iniciará en `http://localhost:5001`.

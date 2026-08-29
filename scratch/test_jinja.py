import sys
sys.path.insert(0, '/Users/esteban/Library/CloudStorage/OneDrive-Personal/Documents/vs/Segundo Semestre/Desarrollo/Proyecto_tickets_python')
from app import app
from flask import render_template_string

template = """
{{ stats.usuarios }}
{{ stats.ventas }}
{{ stats.pedidos_pendientes }}
"""

with app.app_context():
    try:
        stats = { 'usuarios': 2, 'ventas': 100 }
        print(render_template_string(template, stats=stats))
    except Exception as e:
        print("Template error:", e)

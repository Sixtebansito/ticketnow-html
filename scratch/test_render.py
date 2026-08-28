import sys
sys.path.insert(0, '/Users/esteban/Library/CloudStorage/OneDrive-Personal/Documents/vs/Segundo Semestre/Desarrollo/Proyecto_tickets_python')
import os
os.environ['DATABASE_URL'] = "postgresql://neondb_owner:npg_7qhEI2nvQTzC@ep-proud-firefly-au93oo0y-pooler.c-10.us-east-1.aws.neon.tech/neondb?channel_binding=require&sslmode=require"

from app import app, db
from models import Usuario, Pedido, Evento, TipoBoleto
from flask import render_template

with app.test_request_context('/admin'):
    try:
        user = Usuario.query.first()
        stats = {
            'usuarios': Usuario.query.count(),
            'ventas': sum([p.total for p in Pedido.query.all()]),
            'eventos': Evento.query.count()
        }
        res = render_template('admin/dashboard.html', usuario=user, stats=stats)
        print("Template rendered successfully! Length:", len(res))
    except Exception as e:
        import traceback
        traceback.print_exc()

import sys
sys.path.insert(0, '/Users/esteban/Library/CloudStorage/OneDrive-Personal/Documents/vs/Segundo Semestre/Desarrollo/Proyecto_tickets_python')
import os
os.environ['DATABASE_URL'] = "postgresql://neondb_owner:npg_7qhEI2nvQTzC@ep-proud-firefly-au93oo0y-pooler.c-10.us-east-1.aws.neon.tech/neondb?channel_binding=require&sslmode=require"

from app import app, db
from models import Usuario, Pedido, Evento, TipoBoleto

with app.app_context():
    try:
        print("Testing Usuario count:", Usuario.query.count())
        print("Testing Pedido sum:", sum([p.total for p in Pedido.query.all()]))
        print("Testing Evento count:", Evento.query.count())
        
        # Test getting all events (for /)
        print("Testing Evento all:", len(Evento.query.all()))
        
        # Check admin_eventos logic
        categorias = [r[0] for r in db.session.query(Evento.categoria).distinct().filter(Evento.categoria != None, Evento.categoria != '').all()]
        print("Categorias:", categorias)
        
    except Exception as e:
        print("Error:", e)

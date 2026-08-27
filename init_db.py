import os
from flask import Flask
from models import db, Usuario, Evento, TipoBoleto, Noticia, Mercancia, InventarioMercancia, PreguntaFrecuente, Suscripcion, SolicitudVip, CarritoItem, Pedido, PedidoItem, Auditoria, MensajeChat

app = Flask(__name__)
database_url = os.environ.get('DATABASE_URL', 'sqlite:///local_db.sqlite')
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def init():
    with app.app_context():
        print("Eliminando tablas existentes...")
        db.drop_all()
        print("Creando tablas nuevamente...")
        db.create_all()
        print("Base de datos reiniciada con éxito. Ahora puedes ejecutar seed.py.")

if __name__ == '__main__':
    init()

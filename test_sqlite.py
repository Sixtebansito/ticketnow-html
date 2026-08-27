from app import app, db
from models import Evento, Mercancia

with app.app_context():
    try:
        e = Evento.query.first()
        print("Evento table OK")
        m = Mercancia.query.first()
        print("Mercancia table OK")
    except Exception as ex:
        print("Error:", ex)

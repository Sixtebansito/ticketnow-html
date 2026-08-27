import os
from datetime import datetime, timedelta
from flask import Flask
from models import db, Usuario, Evento, TipoBoleto, Noticia, Mercancia, InventarioMercancia, PreguntaFrecuente

app = Flask(__name__)
# Usar base de datos temporal si no hay URL, o conectarse a neon
database_url = os.environ.get('DATABASE_URL', 'sqlite:///local_db.sqlite')
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def seed():
    with app.app_context():
        db.create_all()

        # Admin user
        if not Usuario.query.filter_by(username='admin').first():
            admin = Usuario(nombre='Admin Master', username='admin', email='admin@ticketnow.com', password='admin123', rol='admin', esVip=True)
            db.session.add(admin)
        
        # Test user
        if not Usuario.query.filter_by(username='user').first():
            user = Usuario(nombre='Test User', username='user', email='user@ticketnow.com', password='user123', rol='cliente', esVip=False)
            db.session.add(user)

        # Eventos y Tipos de Boleto
        if not Evento.query.first():
            e1 = Evento(titulo='Coldplay - Music of the Spheres', descripcion='La banda británica llega con su gira mundial.', fecha=datetime.utcnow() + timedelta(days=30), lugar='Estadio Olímpico Atahualpa', imagenUrl='https://images.unsplash.com/photo-1540039155732-d68b20163351?w=800')
            e2 = Evento(titulo='El Fantasma de la Ópera', descripcion='El musical clásico de teatro en vivo.', fecha=datetime.utcnow() + timedelta(days=15), lugar='Teatro Nacional Sucre', imagenUrl='https://images.unsplash.com/photo-1507676184212-d0330a151f84?w=800')
            e3 = Evento(titulo='Final de la Liga Pro - Independiente vs LDU', descripcion='El partido decisivo por el campeonato de fútbol ecuatoriano.', fecha=datetime.utcnow() + timedelta(days=10), lugar='Estadio Rodrigo Paz Delgado', imagenUrl='https://images.unsplash.com/photo-1518605368461-1e1e38ce71cb?w=800')
            
            db.session.add_all([e1, e2, e3])
            db.session.flush()

            t1 = TipoBoleto(evento_id=e1.id, nombre='General', precio=35.0)
            t2 = TipoBoleto(evento_id=e1.id, nombre='Preferencia', precio=45.0)
            t3 = TipoBoleto(evento_id=e1.id, nombre='VIP', precio=80.0)
            
            t4 = TipoBoleto(evento_id=e2.id, nombre='Luneta', precio=20.0)
            t5 = TipoBoleto(evento_id=e2.id, nombre='Platea', precio=50.0)
            
            t6 = TipoBoleto(evento_id=e3.id, nombre='General Norte', precio=12.0)
            t7 = TipoBoleto(evento_id=e3.id, nombre='Tribuna', precio=25.0)
            t8 = TipoBoleto(evento_id=e3.id, nombre='Palco', precio=40.0)

            db.session.add_all([t1, t2, t3, t4, t5, t6, t7, t8])

        # Noticias
        if not Noticia.query.first():
            n1 = Noticia(titulo='Coldplay agota entradas en 24h', resumen='Locura total por las entradas de Coldplay en Quito.', contenido='La banda británica ha roto récords de ventas en Ecuador. En menos de 24 horas, las entradas VIP y Front Stage se han agotado por completo. Se está gestionando una segunda fecha, mantente atento a nuestras redes oficiales para más información. Agradecemos a todos los fans por la inmensa acogida y recuerden no comprar a revendedores para evitar estafas.', imagenUrl='https://images.unsplash.com/photo-1470229722913-7c090be5f524?w=800')
            n2 = Noticia(titulo='Nueva App Oficial', resumen='Descarga nuestra app para llevar tus tickets digitales.', contenido='Estamos emocionados de lanzar nuestra nueva app oficial para iOS y Android. Ahora podrás llevar todos tus boletos directamente en tu celular, comprar merch exclusiva desde la fila del concierto, y recibir notificaciones en tiempo real sobre accesos, parqueaderos y sorpresas VIP. Inicia sesión con la misma cuenta que usas en TicketNow.', imagenUrl='https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?w=800')
            db.session.add_all([n1, n2])

        # Mercancia
        if not Mercancia.query.first():
            m1 = Mercancia(titulo='Hoodie Oficial', descripcion='Buzo de algodón premium.', precio=45.0, categoria='Ropa', colores='#000000', imagenUrl='https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=800')
            m2 = Mercancia(titulo='Gorra TicketNow', descripcion='Gorra oficial para eventos.', precio=18.5, categoria='Accesorios', colores='#000000,#ffffff', imagenUrl='https://images.unsplash.com/photo-1521369909029-2afed882ba28?w=800')
            m3 = Mercancia(titulo='Póster Firmado', descripcion='Póster de edición limitada firmado por los artistas.', precio=25.0, categoria='Coleccionables', colores='', imagenUrl='https://images.unsplash.com/photo-1578309139632-15f0eb981609?w=800')
            db.session.add_all([m1, m2, m3])
            db.session.flush()

            # Inventario (M1 tiene algo de stock, M2 está por agotarse, M3 tiene stock suficiente)
            inv1 = InventarioMercancia(mercancia_id=m1.id, talla='S', stock=10)
            inv2 = InventarioMercancia(mercancia_id=m1.id, talla='M', stock=5)
            inv3 = InventarioMercancia(mercancia_id=m1.id, talla='L', stock=20)
            
            inv4 = InventarioMercancia(mercancia_id=m2.id, talla='Única', stock=3) # < 5 para mostrar mensaje
            
            inv5 = InventarioMercancia(mercancia_id=m3.id, talla='Única', stock=50)

            db.session.add_all([inv1, inv2, inv3, inv4, inv5])

        # FAQ
        if not PreguntaFrecuente.query.first():
            faq1 = PreguntaFrecuente(pregunta='¿Cómo recibo mis entradas?', respuesta='Tus entradas digitales se generarán inmediatamente tras la aprobación del pago. Podrás verlas en tu Perfil.')
            faq2 = PreguntaFrecuente(pregunta='¿Cómo me hago VIP?', respuesta='Solicita ser VIP desde tu perfil o haciendo click en TicketAPP. Un administrador revisará tu cuenta y la aprobará.')
            db.session.add_all([faq1, faq2])

        db.session.commit()
        print("Base de datos inicializada y con datos de prueba.")

if __name__ == '__main__':
    seed()

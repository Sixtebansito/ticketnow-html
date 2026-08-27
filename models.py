from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'Usuario'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(50), default='cliente')
    esVip = db.Column(db.Boolean, default=False)
    fechaRegistro = db.Column(db.DateTime, default=datetime.utcnow)

    suscripciones = db.relationship('Suscripcion', backref='usuario', lazy=True)
    carritoItems = db.relationship('CarritoItem', backref='usuario', lazy=True)
    pedidos = db.relationship('Pedido', backref='usuario', lazy=True)
    mensajesChat = db.relationship('MensajeChat', backref='usuario', lazy=True)
    solicitudesVip = db.relationship('SolicitudVip', backref='usuario', lazy=True)


class Evento(db.Model):
    __tablename__ = 'Evento'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)
    lugar = db.Column(db.String(255), nullable=False)
    activo = db.Column(db.Boolean, default=True)
    imagenUrl = db.Column(db.String(255), nullable=True)
    categoria = db.Column(db.String(100), default='Evento', nullable=True)

    tiposBoleto = db.relationship('TipoBoleto', backref='evento', lazy=True)
    carritoItems = db.relationship('CarritoItem', backref='evento', lazy=True)
    pedidoItems = db.relationship('PedidoItem', backref='evento', lazy=True)

    @property
    def precio_desde(self):
        if not self.tiposBoleto:
            return 0
        return min([t.precio for t in self.tiposBoleto])


class TipoBoleto(db.Model):
    __tablename__ = 'TipoBoleto'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    evento_id = db.Column(db.Integer, db.ForeignKey('Evento.id'), nullable=False)
    nombre = db.Column(db.String(255), nullable=False)
    precio = db.Column(db.Float, nullable=False)


class Noticia(db.Model):
    __tablename__ = 'Noticia'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(255), nullable=False)
    resumen = db.Column(db.String(255), nullable=True)
    contenido = db.Column(db.Text, nullable=False)
    imagenUrl = db.Column(db.String(255), nullable=True)
    activo = db.Column(db.Boolean, default=True)
    fechaPub = db.Column(db.DateTime, default=datetime.utcnow)


class Mercancia(db.Model):
    __tablename__ = 'Mercancia'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    categoria = db.Column(db.String(255), nullable=False)
    colores = db.Column(db.String(255), nullable=True)
    imagenUrl = db.Column(db.String(255), nullable=True)
    activo = db.Column(db.Boolean, default=True)

    inventario = db.relationship('InventarioMercancia', backref='mercancia', lazy=True)
    carritoItems = db.relationship('CarritoItem', backref='mercancia', lazy=True)
    pedidoItems = db.relationship('PedidoItem', backref='mercancia', lazy=True)


class InventarioMercancia(db.Model):
    __tablename__ = 'InventarioMercancia'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mercancia_id = db.Column(db.Integer, db.ForeignKey('Mercancia.id'), nullable=False)
    talla = db.Column(db.String(50), nullable=False)
    stock = db.Column(db.Integer, default=0)


class PreguntaFrecuente(db.Model):
    __tablename__ = 'PreguntaFrecuente'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pregunta = db.Column(db.String(255), nullable=False)
    respuesta = db.Column(db.Text, nullable=False)
    activo = db.Column(db.Boolean, default=True)


class MensajeChat(db.Model):
    __tablename__ = 'MensajeChat'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    texto = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    usuarioId = db.Column(db.Integer, db.ForeignKey('Usuario.id'), nullable=False)


class Suscripcion(db.Model):
    __tablename__ = 'Suscripcion'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo = db.Column(db.String(255), nullable=False)
    fechaInicio = db.Column(db.DateTime, default=datetime.utcnow)
    fechaFin = db.Column(db.DateTime, nullable=True)
    usuarioId = db.Column(db.Integer, db.ForeignKey('Usuario.id'), nullable=False)


class SolicitudVip(db.Model):
    __tablename__ = 'SolicitudVip'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuarioId = db.Column(db.Integer, db.ForeignKey('Usuario.id'), nullable=False)
    estado = db.Column(db.String(50), default='Pendiente') # Pendiente, Aprobado, Rechazado
    fecha = db.Column(db.DateTime, default=datetime.utcnow)


class CarritoItem(db.Model):
    __tablename__ = 'CarritoItem'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cantidad = db.Column(db.Integer, default=1)
    usuarioId = db.Column(db.Integer, db.ForeignKey('Usuario.id'), nullable=False)
    
    eventoId = db.Column(db.Integer, db.ForeignKey('Evento.id'), nullable=True)
    tipoBoletoId = db.Column(db.Integer, db.ForeignKey('TipoBoleto.id'), nullable=True)
    
    mercanciaId = db.Column(db.Integer, db.ForeignKey('Mercancia.id'), nullable=True)
    talla = db.Column(db.String(50), nullable=True)
    
    tipo_boleto = db.relationship('TipoBoleto', foreign_keys=[tipoBoletoId])


class Pedido(db.Model):
    __tablename__ = 'Pedido'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    total = db.Column(db.Float, nullable=False)
    estado = db.Column(db.String(50), default='Pendiente') # Pendiente, Aprobado, Rechazado
    usuarioId = db.Column(db.Integer, db.ForeignKey('Usuario.id'), nullable=False)
    items = db.relationship('PedidoItem', backref='pedido', lazy=True)


class PedidoItem(db.Model):
    __tablename__ = 'PedidoItem'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cantidad = db.Column(db.Integer, nullable=False)
    precioUn = db.Column(db.Float, nullable=False)
    pedidoId = db.Column(db.Integer, db.ForeignKey('Pedido.id'), nullable=False)
    
    eventoId = db.Column(db.Integer, db.ForeignKey('Evento.id'), nullable=True)
    tipoBoletoId = db.Column(db.Integer, db.ForeignKey('TipoBoleto.id'), nullable=True)
    
    mercanciaId = db.Column(db.Integer, db.ForeignKey('Mercancia.id'), nullable=True)
    talla = db.Column(db.String(50), nullable=True)
    
    tipo_boleto = db.relationship('TipoBoleto', foreign_keys=[tipoBoletoId])


class Auditoria(db.Model):
    __tablename__ = 'Auditoria'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    accion = db.Column(db.String(255), nullable=False)
    tabla = db.Column(db.String(100), nullable=True)
    detalle = db.Column(db.Text, nullable=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    usuarioId = db.Column(db.Integer, db.ForeignKey('Usuario.id'), nullable=False)
    usuario = db.relationship('Usuario', backref='auditorias', lazy=True)

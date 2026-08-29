import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from models import db, Usuario, Evento, Noticia, Mercancia, PreguntaFrecuente, CarritoItem, Pedido, PedidoItem, Auditoria, MensajeChat, TipoBoleto, SolicitudVip, InventarioMercancia, Configuracion

from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer
from email_utils import enviar_correo

app = Flask(__name__)
app.secret_key = 'ticketnow_secret_key_flask'

database_url = os.environ.get('DATABASE_URL', 'sqlite:///local_db.sqlite')
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pymssql://sa:MiloOreo06@localhost:1433/TicketsDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def get_current_user():
    if 'userId' in session:
        return Usuario.query.get(session['userId'])
    return None

@app.route('/initdb-secret')
def initdb():
    try:
        db.create_all()
        return "Tablas creadas exitosamente."
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/seed-more-secret')
def seed_more():
    try:
        from datetime import datetime, timedelta
        
        # 5 Eventos
        e1 = Evento(titulo='Festival de Música Urbana', descripcion='El mayor festival de reggaeton y trap.', fecha=datetime.utcnow() + timedelta(days=20), lugar='Arena Coliseo', imagenUrl='https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=800')
        e2 = Evento(titulo='Concierto Sinfónico Rock', descripcion='Clásicos del rock interpretados por la orquesta sinfónica.', fecha=datetime.utcnow() + timedelta(days=45), lugar='Teatro Nacional', imagenUrl='https://images.unsplash.com/photo-1549834125-82d3c48159a3?w=800')
        e3 = Evento(titulo='Torneo E-Sports Final', descripcion='La gran final de League of Legends.', fecha=datetime.utcnow() + timedelta(days=12), lugar='Centro de Convenciones', imagenUrl='https://images.unsplash.com/photo-1542751371-adc38448a05e?w=800')
        e4 = Evento(titulo='Stand Up Comedy Night', descripcion='Noche de risas con los mejores comediantes del país.', fecha=datetime.utcnow() + timedelta(days=5), lugar='Bar Comedy Club', imagenUrl='https://images.unsplash.com/photo-1585699324551-f6c309eedeca?w=800')
        e5 = Evento(titulo='Exhibición de Arte Moderno', descripcion='Galería con artistas emergentes de Latinoamérica.', fecha=datetime.utcnow() + timedelta(days=60), lugar='Museo de Arte Contemporáneo', imagenUrl='https://images.unsplash.com/photo-1536924940846-227afb31e2a5?w=800')
        db.session.add_all([e1, e2, e3, e4, e5])
        db.session.flush()

        t1 = TipoBoleto(evento_id=e1.id, nombre='General', precio=30.0)
        t2 = TipoBoleto(evento_id=e1.id, nombre='VIP', precio=75.0)
        t3 = TipoBoleto(evento_id=e2.id, nombre='Platea', precio=40.0)
        t4 = TipoBoleto(evento_id=e3.id, nombre='General', precio=15.0)
        t5 = TipoBoleto(evento_id=e4.id, nombre='Mesa', precio=20.0)
        t6 = TipoBoleto(evento_id=e5.id, nombre='Pase Libre', precio=10.0)
        db.session.add_all([t1, t2, t3, t4, t5, t6])

        # 5 Mercancías
        m1 = Mercancia(titulo='Camiseta Oficial Real Madrid', descripcion='Camiseta temporada 2025.', precio=85.0, categoria='Ropa', imagenUrl='https://images.unsplash.com/photo-1583316174775-bd6dc0e9f298?w=800')
        m2 = Mercancia(titulo='Camiseta FC Barcelona', descripcion='Camiseta oficial visitante.', precio=80.0, categoria='Ropa', imagenUrl='https://images.unsplash.com/photo-1579952363873-27f3bade9f55?w=800')
        m3 = Mercancia(titulo='Póster Concierto Coldplay', descripcion='Póster gigante autografiado.', precio=25.0, categoria='Accesorios', imagenUrl='https://images.unsplash.com/photo-1584680239088-728b7e283204?w=800')
        m4 = Mercancia(titulo='Póster El Fantasma de la Ópera', descripcion='Edición de colección.', precio=20.0, categoria='Accesorios', imagenUrl='https://images.unsplash.com/photo-1580136607993-df77229e6125?w=800')
        m5 = Mercancia(titulo='Camiseta Evento E-Sports', descripcion='Talla M edición especial.', precio=30.0, categoria='Ropa', imagenUrl='https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=800')
        db.session.add_all([m1, m2, m3, m4, m5])
        db.session.flush()

        inv1 = InventarioMercancia(mercancia_id=m1.id, talla='L', stock=50)
        inv2 = InventarioMercancia(mercancia_id=m2.id, talla='M', stock=30)
        inv3 = InventarioMercancia(mercancia_id=m3.id, talla='Única', stock=100)
        inv4 = InventarioMercancia(mercancia_id=m4.id, talla='Única', stock=150)
        inv5 = InventarioMercancia(mercancia_id=m5.id, talla='S', stock=20)
        db.session.add_all([inv1, inv2, inv3, inv4, inv5])

        # 2 FAQ
        f1 = PreguntaFrecuente(pregunta='¿Cómo descargo mis boletos electrónicos?', respuesta='Puedes descargar tus boletos desde la sección "Mis Pedidos" en tu Dashboard.')
        f2 = PreguntaFrecuente(pregunta='¿Qué hago si mi pago es rechazado?', respuesta='Intenta con otra tarjeta de crédito o contacta a soporte mediante nuestro chat.')
        db.session.add_all([f1, f2])

        # 2 Noticias
        n1 = Noticia(titulo='Nuevos conciertos anunciados para 2026', contenido='Prepárate para la mayor gira de artistas internacionales en el país.', imagenUrl='https://images.unsplash.com/photo-1459749411175-04bf5292ceea?w=800')
        n2 = Noticia(titulo='Descuentos VIP en Tienda', contenido='Los clientes VIP ahora cuentan con un 20% de descuento en mercadería.', imagenUrl='https://images.unsplash.com/photo-1607082348824-0a96f2a4b9da?w=800')
        db.session.add_all([n1, n2])

        db.session.commit()
        return "Nuevos registros creados exitosamente."
    except Exception as e:
        db.session.rollback()
        return f"Error: {str(e)}"

@app.route('/')
def index():
    user = get_current_user()
    
    # Obtener configuración del GIF
    try:
        conf_gif = Configuracion.query.filter_by(clave='landing_gif').first()
        landing_gif = conf_gif.valor if conf_gif and conf_gif.valor else 'https://www.image2url.com/r2/default/gifs/1787878685830-94dc7db9-4f10-4216-87d5-c1a594f53291.gif'
    except Exception:
        db.session.rollback()
        landing_gif = 'https://www.image2url.com/r2/default/gifs/1787878685830-94dc7db9-4f10-4216-87d5-c1a594f53291.gif'
    
    eventos_db = Evento.query.filter_by(activo=True).order_by(Evento.fecha.asc()).limit(3).all()
    import json
    eventos = []
    colores = [
        {"bg": "from-purple-800 to-purple-400", "txt": "text-purple-600 dark:text-purple-400", "tag": "bg-purple-100 dark:bg-purple-600/20"},
        {"bg": "from-blue-800 to-blue-400", "txt": "text-blue-600 dark:text-blue-400", "tag": "bg-blue-100 dark:bg-blue-600/20"},
        {"bg": "from-orange-800 to-orange-400", "txt": "text-orange-700 dark:text-orange-400", "tag": "bg-orange-100 dark:bg-orange-500/20"}
    ]
    for i, e in enumerate(eventos_db):
        c = colores[i % len(colores)]
        boletos_json = json.dumps([{'id': b.id, 'nombre': b.nombre, 'precio': float(b.precio)} for b in e.tiposBoleto])
        eventos.append({
            'id': e.id,
            'cat': e.categoria or 'Evento',
            'tit': e.titulo,
            'precio': f'${e.precio_desde:.2f}',
            'boletos_json': boletos_json,
            'fecha': e.fecha.strftime('%d %b %Y') if e.fecha else 'Por confirmar',
            'lugar': e.lugar,
            'bg': c['bg'],
            'txt': c['txt'],
            'tag': c['tag'],
            'imagen': e.imagenUrl
        })

    noticias = Noticia.query.filter_by(activo=True).order_by(Noticia.fechaPub.desc()).limit(3).all()

    mercancia_db = Mercancia.query.filter_by(activo=True).limit(3).all()
    mercancia = [{
        'id': m.id,
        'cat': m.categoria,
        'tit': m.titulo,
        'precio': f'${m.precio:.2f}',
        'precio_raw': m.precio,
        'desc': m.descripcion,
        'tallas': [
            {'talla': inv.talla, 'stock': inv.stock}
            for inv in m.inventario
        ],
        'total_stock': sum(inv.stock for inv in m.inventario),
        'imagen': m.imagenUrl
    } for m in mercancia_db]

    # Dummy mercancia si DB está vacía para probar
    if not mercancia:
        mercancia = [
            { 'cat': "Ropa", 'tit': "Hoodie Oficial - Coldplay", 'precio': "$45.00", 'desc': "Buzo de algodón premium con capucha de la gira mundial.", 'tallas': ["M", "L"], 'col': ["#000"] },
            { 'cat': "Accesorios", 'tit': "Gorra TicketNow Snapback", 'precio': "$18.50", 'desc': "Protege tu estilo en cada concierto con visera plana.", 'tallas': ["Única"], 'col': ["#000", "#fff"] },
            { 'cat': "Coleccionables", 'tit': "Termo de Acero - Quito en Vivo", 'precio': "$22.00", 'desc': "Termo oficial de doble capa térmica de 500ml.", 'tallas': [], 'col': ["#7c3aed"] }
        ]

    return render_template('index.html', usuario=user, eventos=eventos, noticias=noticias, mercancia=mercancia, landing_gif=landing_gif)

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    user = get_current_user()
    if user:
        return redirect(url_for('perfil'))
        
    error = None
    if request.method == 'POST':
        action = request.form.get('action')
        password = request.form.get('password')
        
        if action == 'login':
            username = request.form.get('username')
            usuario = Usuario.query.filter_by(username=username).first()
            if usuario:
                valid = False
                if usuario.password and usuario.password.startswith('scrypt:'):
                    valid = check_password_hash(usuario.password, password)
                else:
                    valid = (usuario.password == password)
                    if valid:
                        usuario.password = generate_password_hash(password)
                        db.session.commit()

                if valid:
                    session['userId'] = usuario.id
                    
                    # Send email
                    from email_utils import enviar_correo
                    from datetime import datetime
                    mensaje = f"""
                    <h2>Hola {usuario.nombre},</h2>
                    <p>Se ha detectado un nuevo inicio de sesión en tu cuenta de TicketNow.</p>
                    <p>Fecha y Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    <p>Si no fuiste tú, te recomendamos cambiar tu contraseña inmediatamente.</p>
                    """
                    enviar_correo(usuario.email, "Nuevo inicio de sesión - TicketNow", mensaje)

                    return redirect(url_for('perfil'))
                else:
                    error = "Credenciales incorrectas"
            else:
                error = "Credenciales incorrectas"
                
        elif action == 'register':
            nombre = request.form.get('nombre')
            username = request.form.get('username')
            email = request.form.get('email')
            
            if Usuario.query.filter_by(email=email).first():
                error = "El correo ya está registrado"
            elif Usuario.query.filter_by(username=username).first():
                error = "El usuario ya está registrado"
            else:
                is_admin = (email == 'admin@ticketnow.com' or email == 'admin@admin.com')
                nuevo_usuario = Usuario(
                    nombre=nombre,
                    username=username,
                    email=email,
                    password=generate_password_hash(password),
                    rol="admin" if is_admin else "cliente",
                    esVip=is_admin
                )
                db.session.add(nuevo_usuario)
                db.session.commit()
                session['userId'] = nuevo_usuario.id
                return redirect(url_for('perfil'))
                
    return render_template('auth.html', usuario=None, error=error)

@app.route('/logout')
def logout():
    session.pop('userId', None)
    return redirect(url_for('index'))

@app.route('/olvide-password', methods=['GET', 'POST'])
def olvide_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = Usuario.query.filter_by(email=email).first()
        if user:
            s = URLSafeTimedSerializer(app.secret_key)
            token = s.dumps(user.email, salt='password-reset-salt')
            reset_url = url_for('reset_password', token=token, _external=True)
            
            html = f'''
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #6b21a8;">Restablecer tu contraseña</h2>
                <p>Hola {user.nombre},</p>
                <p>Has solicitado restablecer tu contraseña. Haz clic en el siguiente enlace para crear una nueva:</p>
                <p style="text-align: center; margin: 30px 0;">
                    <a href="{reset_url}" style="background-color: #9333ea; color: white; padding: 12px 24px; text-decoration: none; border-radius: 8px; font-weight: bold;">Restablecer Contraseña</a>
                </p>
                <p>Si no fuiste tú quien solicitó esto, simplemente ignora este correo.</p>
                <p>El enlace caducará en 1 hora.</p>
                <hr style="border: 1px solid #eee; margin: 30px 0;" />
                <p style="color: #888; font-size: 12px; text-align: center;">El equipo de TicketNow</p>
            </div>
            '''
            enviar_correo(user.email, "Restablecer contraseña - TicketNow", html)
            
        flash('Si el correo está registrado, recibirás un enlace para restablecer tu contraseña.', 'info')
        return redirect(url_for('auth'))
        
    return render_template('olvide_password.html')

@app.route('/recuperar-usuario', methods=['GET', 'POST'])
def recuperar_usuario():
    if request.method == 'POST':
        email = request.form.get('email')
        user = Usuario.query.filter_by(email=email).first()
        if user:
            html = f'''
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #6b21a8;">Recuperación de Usuario</h2>
                <p>Hola {user.nombre},</p>
                <p>Has solicitado recuperar tu nombre de usuario de TicketNow.</p>
                <p style="text-align: center; margin: 30px 0; padding: 20px; background: #f3f4f6; border-radius: 8px;">
                    Tu nombre de usuario es: <strong style="font-size: 1.2em; color: #9333ea;">{user.username}</strong>
                </p>
                <p>Si no fuiste tú quien solicitó esto, simplemente ignora este correo.</p>
                <hr style="border: 1px solid #eee; margin: 30px 0;" />
                <p style="color: #888; font-size: 12px; text-align: center;">El equipo de TicketNow</p>
            </div>
            '''
            enviar_correo(user.email, "Tu nombre de usuario - TicketNow", html)
            
        flash('Si el correo está registrado, recibirás un mensaje con tu nombre de usuario.', 'info')
        return redirect(url_for('auth'))
        
    return render_template('recuperar_usuario.html')


@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    s = URLSafeTimedSerializer(app.secret_key)
    try:
        email = s.loads(token, salt='password-reset-salt', max_age=3600)
    except Exception:
        flash('El enlace para restablecer la contraseña es inválido o ha expirado.', 'error')
        return redirect(url_for('auth'))
        
    if request.method == 'POST':
        password = request.form.get('password')
        user = Usuario.query.filter_by(email=email).first()
        if user:
            user.password = generate_password_hash(password)
            db.session.commit()
            flash('Tu contraseña ha sido actualizada correctamente. Ya puedes iniciar sesión.', 'success')
            return redirect(url_for('auth'))
            
    return render_template('reset_password.html', token=token)


@app.route('/eventos')
def eventos():
    user = get_current_user()
    eventos_db = Evento.query.filter_by(activo=True).all()
    eventos = []
    colores = [
        {"bg": "from-purple-800 to-purple-400", "txt": "text-purple-600 dark:text-purple-400", "tag": "bg-purple-100 dark:bg-purple-600/20"},
        {"bg": "from-blue-800 to-blue-400", "txt": "text-blue-600 dark:text-blue-400", "tag": "bg-blue-100 dark:bg-blue-600/20"},
        {"bg": "from-orange-800 to-orange-400", "txt": "text-orange-700 dark:text-orange-400", "tag": "bg-orange-100 dark:bg-orange-500/20"}
    ]
    import json
    for i, e in enumerate(eventos_db):
        c = colores[i % len(colores)]
        boletos_json = json.dumps([{'id': b.id, 'nombre': b.nombre, 'precio': float(b.precio)} for b in e.tiposBoleto])
        eventos.append({
            'id': e.id,
            'cat': e.categoria or 'Evento',
            'tit': e.titulo,
            'precio': f'${e.precio_desde:.2f}',
            'boletos_json': boletos_json,
            'bg': c['bg'],
            'txt': c['txt'],
            'tag': c['tag'],
            'imagen': e.imagenUrl,
            'fecha': e.fecha.strftime('%d %b %Y') if e.fecha else 'Por confirmar',
            'lugar': e.lugar
        })
        
    # Obtener categorías únicas de eventos
    categorias_eventos = [r[0] for r in db.session.query(Evento.categoria).distinct().filter(Evento.categoria != None, Evento.categoria != '').all()]
    
    return render_template('eventos.html', usuario=user, eventos=eventos, categorias=categorias_eventos)

@app.route('/noticias')
def noticias():
    user = get_current_user()
    noticias_db = Noticia.query.filter_by(activo=True).order_by(Noticia.fechaPub.desc()).all()
    return render_template('noticias.html', usuario=user, noticias=noticias_db)

@app.route('/noticia/<int:id>')
def noticia_detalle(id):
    user = get_current_user()
    noticia = Noticia.query.get_or_404(id)
    return render_template('noticia_detalle.html', usuario=user, noticia=noticia)

@app.route('/tienda')
def tienda():
    user = get_current_user()
    
    eventos_db = Evento.query.filter_by(activo=True).order_by(Evento.fecha.asc()).all()
    eventos = []
    colores = [
        {"bg": "from-purple-800 to-purple-400", "txt": "text-purple-600 dark:text-purple-400", "tag": "bg-purple-100 dark:bg-purple-600/20"},
        {"bg": "from-blue-800 to-blue-400", "txt": "text-blue-600 dark:text-blue-400", "tag": "bg-blue-100 dark:bg-blue-600/20"},
        {"bg": "from-orange-800 to-orange-400", "txt": "text-orange-700 dark:text-orange-400", "tag": "bg-orange-100 dark:bg-orange-500/20"}
    ]
    for i, e in enumerate(eventos_db):
        c = colores[i % len(colores)]
        eventos.append({
            'id': e.id,
            'cat': e.categoria,
            'tit': e.titulo,
            'precio': f'${e.precio_desde:.2f}',
            'bg': c['bg'],
            'txt': c['txt'],
            'tag': c['tag'],
            'imagen': e.imagenUrl
        })

    mercancia_db = Mercancia.query.filter_by(activo=True).all()
    mercancia = [{
        'id': m.id,
        'cat': m.categoria,
        'tit': m.titulo,
        'precio': f'${m.precio:.2f}',
        'precio_raw': m.precio,
        'desc': m.descripcion,
        'tallas': [
            {'talla': inv.talla, 'stock': inv.stock}
            for inv in m.inventario
        ],
        'total_stock': sum(inv.stock for inv in m.inventario),
        'imagen': m.imagenUrl
    } for m in mercancia_db]

    # Obtener categorías únicas de mercancía y eventos
    categorias_mercancia = [r[0] for r in db.session.query(Mercancia.categoria).distinct().filter(Mercancia.categoria != None, Mercancia.categoria != '').all()]
    categorias_eventos = [r[0] for r in db.session.query(Evento.categoria).distinct().filter(Evento.categoria != None, Evento.categoria != '').all()]

    return render_template('tienda.html', usuario=user, eventos=eventos, mercancia=mercancia, categorias_mercancia=categorias_mercancia, categorias_eventos=categorias_eventos)

@app.route('/detalle-evento/<int:id>')
def detalle_evento(id):
    user = get_current_user()
    evento_db = Evento.query.get_or_404(id)
    ev = {
        'id': evento_db.id,
        'cat': 'Concierto',
        'tit': evento_db.titulo,
        'precio': f'${evento_db.precio_desde:.2f}',
        'precio_raw': evento_db.precio_desde,
        'desc': evento_db.descripcion,
        'fecha': evento_db.fecha.strftime('%d %B %Y') if evento_db.fecha else '15 Agosto 2026',
        'hora': evento_db.fecha.strftime('%H:%M') if evento_db.fecha else '20:00',
        'lugar': evento_db.lugar,
        'imagen': evento_db.imagenUrl,
        'tipos': evento_db.tiposBoleto
    }
    return render_template('detalle_evento.html', usuario=user, evento=ev)


@app.route('/setup-db')
def setup_db():
    try:
        from sqlalchemy import text
        # Intentar añadir columnas a las tablas si no existen. Las comillas dobles aseguran que respete las mayúsculas en PostgreSQL
        db.session.execute(text('ALTER TABLE "Evento" ADD COLUMN IF NOT EXISTS categoria VARCHAR(255);'))
        db.session.execute(text('ALTER TABLE "Mercancia" ADD COLUMN IF NOT EXISTS categoria VARCHAR(255);'))
        
        # También asegurar que imagenUrl esté en mercancia si no estaba
        db.session.execute(text('ALTER TABLE "Mercancia" ADD COLUMN IF NOT EXISTS "imagenUrl" VARCHAR(255);'))
        
        db.session.commit()
        return "Base de datos actualizada correctamente. <a href='/'>Volver al inicio</a>"
    except Exception as e:
        db.session.rollback()
        return f"Error actualizando la base de datos: {str(e)}"

@app.route('/debug-db')
def debug_db():
    try:
        from sqlalchemy import text
        db_url = os.environ.get('DATABASE_URL', 'NOT SET (usando local_db.sqlite)')
        
        # Test connection
        res = db.session.execute(text("SELECT 1")).scalar()
        
        # Test Evento schema
        try:
            ev_count = Evento.query.count()
            ev_status = f"Evento count: {ev_count}"
        except Exception as e:
            ev_status = f"Evento query failed: {str(e)}"
            
        return f"DB URL: {db_url[:15]}... | Connection: OK ({res}) | {ev_status}"
    except Exception as e:
        import traceback
        return f"DB Connection ERROR: {str(e)} <br><pre>{traceback.format_exc()}</pre>"

@app.route('/precios-vip')
def precios_vip():
    user = get_current_user()
    if user and user.esVip:
        return redirect(url_for('ticketapp'))
    return render_template('precios_vip.html', usuario=user)

@app.route('/solicitar-vip', methods=['POST'])
def solicitar_vip():
    user = get_current_user()
    if not user:
        flash("Debes iniciar sesión para solicitar ser VIP.", "error")
        return redirect(url_for('auth'))
    
    # Check if a pending or approved request already exists
    existing = SolicitudVip.query.filter_by(usuarioId=user.id).order_by(SolicitudVip.fecha.desc()).first()
    if existing and existing.estado in ['Pendiente', 'Aprobado', 'aprobada', 'pendiente']:
        flash("Ya tienes una solicitud VIP en proceso o aprobada.", "warning")
        return redirect(url_for('perfil'))
        
    nueva_solicitud = SolicitudVip(usuarioId=user.id, estado='pendiente')
    db.session.add(nueva_solicitud)
    db.session.commit()
    flash("Tu solicitud VIP ha sido enviada con éxito.", "success")
    return redirect(url_for('perfil'))

@app.route('/ayuda')
def ayuda():
    user = get_current_user()
    faqs = PreguntaFrecuente.query.filter_by(activo=True).all()
    return render_template('ayuda.html', usuario=user, faqs=faqs)

@app.route('/perfil')
def perfil():
    user = get_current_user()
    if not user:
        return redirect(url_for('auth'))
    pedidos = Pedido.query.filter_by(usuarioId=user.id).order_by(Pedido.fecha.desc()).limit(5).all()
    return render_template('perfil.html', usuario=user, pedidos=pedidos)

@app.route('/pedido/<int:id>')
def detalle_pedido(id):
    user = get_current_user()
    if not user:
        return redirect(url_for('auth'))
    pedido = Pedido.query.get_or_404(id)
    if pedido.usuarioId != user.id and user.rol != 'admin':
        flash('No tienes permiso para ver este pedido.', 'error')
        return redirect(url_for('perfil'))
    return render_template('detalle_pedido.html', usuario=user, pedido=pedido)

@app.route('/carrito', methods=['GET', 'POST'])
def carrito():
    user = get_current_user()
    success = False
    error = None

    if request.method == 'POST':
        cart_str = request.form.get('cart')
        if cart_str:
            import json
            try:
                cart = json.loads(cart_str)
                if cart:
                    if not user:
                        return redirect(url_for('auth'))

                    subtotal = 0
                    has_vip = False
                    for item in cart:
                        subtotal += item.get('price', 0) * item.get('quantity', 1)
                        if item.get('type') == 'membresia':
                            has_vip = True
                    
                    total = subtotal * 1.10

                    event_items = [item for item in cart if 'id' in item and str(item['id']).isdigit() and item.get('type') == 'evento']

                    nuevo_pedido = Pedido(total=total, usuarioId=user.id)
                    db.session.add(nuevo_pedido)
                    db.session.flush()

                    for item in event_items:
                        nuevo_item = PedidoItem(
                            cantidad=item.get('quantity', 1),
                            precioUn=item.get('price', 0),
                            pedidoId=nuevo_pedido.id,
                            eventoId=int(item['id'])
                        )
                        db.session.add(nuevo_item)
                    
                    if has_vip:
                        user_db = Usuario.query.get(user.id)
                        if user_db:
                            user_db.esVip = True
                    
                    db.session.commit()
                    success = True

                    # Send purchase receipt email
                    from email_utils import enviar_correo
                    from datetime import datetime
                    
                    detalles_html = ""
                    for item in cart:
                        detalles_html += f"<li>{item.get('quantity', 1)}x {item.get('name', 'Item')} - ${item.get('price', 0)}</li>"
                    
                    mensaje = f"""
                    <h2>¡Gracias por tu compra, {user.nombre}!</h2>
                    <p>Tu pedido <strong>#ORD-{nuevo_pedido.id}</strong> ha sido confirmado.</p>
                    <p><strong>Fecha:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    <br>
                    <h3>Detalles de la compra:</h3>
                    <ul>
                        {detalles_html}
                    </ul>
                    <p><strong>Total pagado:</strong> ${"%.2f" % total}</p>
                    <br>
                    <p>Puedes ver el detalle completo en tu <a href="https://ticketnow-html.vercel.app/pedido/{nuevo_pedido.id}">perfil de TicketNow</a>.</p>
                    """
                    enviar_correo(user.email, f"Confirmación de Pedido #ORD-{nuevo_pedido.id}", mensaje)


            except Exception as e:
                print(e)
                error = "Hubo un error al procesar tu pago."

    return render_template('carrito.html', usuario=user, success=success, error=error)

@app.route('/admin/configuracion', methods=['GET', 'POST'])
def admin_configuracion():
    user = get_current_user()
    if not user or user.rol != 'admin':
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        landing_gif = request.form.get('landing_gif')
        if landing_gif:
            conf = Configuracion.query.filter_by(clave='landing_gif').first()
            if not conf:
                conf = Configuracion(clave='landing_gif', valor=landing_gif)
                db.session.add(conf)
            else:
                conf.valor = landing_gif
            db.session.commit()
            log_auditoria("Actualizar Configuracion", "Configuracion", "Landing GIF actualizado")
            flash("Configuración actualizada", "success")
        return redirect(url_for('admin_configuracion'))
        
    conf = Configuracion.query.filter_by(clave='landing_gif').first()
    current_gif = conf.valor if conf else ''
    
    return render_template('admin/configuracion.html', usuario=user, current_gif=current_gif)

@app.route('/ticketapp')
def ticketapp():
    user = get_current_user()
    if not user:
        return redirect(url_for('auth'))
    
    user_db = Usuario.query.get(user.id)
    if not user_db or not user_db.esVip:
        flash('Necesitas ser Miembro VIP para acceder al dashboard de TicketApp.', 'warning')
        return redirect(url_for('precios_vip'))
    
    mensajes = MensajeChat.query.order_by(MensajeChat.fecha.asc()).limit(50).all()
    return render_template('ticketapp.html', usuario=user, mensajes=mensajes, isVip=True)

@app.route('/api/chat', methods=['GET', 'POST'])
def api_chat():
    user = get_current_user()
    if not user or not user.esVip:
        return jsonify({'error': 'No autorizado'}), 401
        
    if request.method == 'POST':
        data = request.json
        texto = data.get('texto')
        if texto:
            msg = MensajeChat(texto=texto, usuarioId=user.id)
            db.session.add(msg)
            db.session.commit()
            return jsonify({'success': True, 'msg': {'id': msg.id, 'texto': msg.texto, 'fecha': msg.fecha.isoformat(), 'usuario': {'nombre': user.nombre}}})
        return jsonify({'error': 'Texto vacío'}), 400
        
    mensajes = MensajeChat.query.order_by(MensajeChat.fecha.desc()).limit(50).all()
    mensajes.reverse()
    return jsonify([{
        'id': m.id,
        'texto': m.texto,
        'fecha': m.fecha.isoformat(),
        'usuario': {'nombre': m.usuario.nombre}
    } for m in mensajes])

def log_auditoria(accion, tabla=None, detalle=None):
    user = get_current_user()
    if user:
        aud = Auditoria(accion=accion, tabla=tabla, detalle=detalle, usuarioId=user.id)
        db.session.add(aud)
        db.session.commit()

@app.route('/perfil/info', methods=['GET', 'POST'])
def perfil_info():
    user = get_current_user()
    if not user: return redirect(url_for('auth'))
    
    if request.method == 'POST':
        password_actual = request.form.get('password_actual')
        nueva_password = request.form.get('nueva_password')
        if password_actual and nueva_password:
            valid_actual = False
            if user.password and user.password.startswith('scrypt:'):
                valid_actual = check_password_hash(user.password, password_actual)
            else:
                valid_actual = (user.password == password_actual)
                
            if valid_actual:
                user.password = generate_password_hash(nueva_password)
                db.session.commit()
                flash("Contraseña actualizada exitosamente.", "success")
            else:
                flash("La contraseña actual es incorrecta.", "error")
            
        return redirect(url_for('perfil_info'))
        
    return render_template('perfil_info.html', usuario=user)

@app.route('/perfil/pagos')
def perfil_pagos():
    user = get_current_user()
    if not user: return redirect(url_for('auth'))
    return render_template('perfil_pagos.html', usuario=user)

@app.route('/admin')
def admin_dashboard():
    user = get_current_user()
    if not user or user.rol != 'admin': return redirect(url_for('index'))
    stats = {
        'usuarios': Usuario.query.count(),
        'ventas': sum([p.total for p in Pedido.query.all()]),
        'eventos': Evento.query.count(),
        'pedidos_pendientes': Pedido.query.filter(Pedido.estado.in_(['Pendiente', 'pendiente'])).count(),
        'solicitudes_vip': SolicitudVip.query.filter(SolicitudVip.estado.in_(['Pendiente', 'pendiente'])).count()
    }
    return render_template('admin/dashboard.html', usuario=user, stats=stats)

@app.route('/admin/aprobaciones', methods=['GET', 'POST'])
def admin_aprobaciones():
    user = get_current_user()
    if not user or user.rol != 'admin': return redirect(url_for('index'))
    
    if request.method == 'POST':
        action = request.form.get('action')
        solicitud_id = request.form.get('id')
        req_type = request.form.get('type')
        
        if req_type == 'vip' and solicitud_id:
            solicitud = SolicitudVip.query.get(solicitud_id)
            if solicitud:
                if action == 'aprobar':
                    solicitud.estado = 'aprobada'
                    if solicitud.usuario:
                        solicitud.usuario.esVip = True
                    flash('Solicitud VIP aprobada correctamente.', 'success')
                elif action == 'rechazar':
                    solicitud.estado = 'rechazada'
                    flash('Solicitud VIP rechazada.', 'success')
                db.session.commit()
                
        elif req_type == 'pedido' and solicitud_id:
            pedido = Pedido.query.get(solicitud_id)
            if pedido:
                if action == 'aprobar':
                    pedido.estado = 'Aprobado'
                    flash('Pedido aprobado correctamente.', 'success')
                elif action == 'rechazar':
                    pedido.estado = 'Rechazado'
                    flash('Pedido rechazado.', 'success')
                db.session.commit()
                
        return redirect(url_for('admin_aprobaciones'))

    solicitudes = SolicitudVip.query.filter(SolicitudVip.estado.in_(['Pendiente', 'pendiente'])).all()
    pedidos = Pedido.query.filter(Pedido.estado.in_(['Pendiente', 'pendiente'])).all()
    return render_template('admin/aprobaciones.html', usuario=user, solicitudes=solicitudes, pedidos=pedidos)

@app.route('/admin/eventos', methods=['GET', 'POST'])
def admin_eventos():
    user = get_current_user()
    if not user or user.rol != 'admin': return redirect(url_for('index'))
    
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add':
            import datetime
            try:
                fecha_str = request.form.get('fecha')
                fecha_obj = datetime.datetime.fromisoformat(fecha_str) if fecha_str else datetime.datetime.utcnow()
                e = Evento(
                    titulo=request.form.get('titulo'),
                    descripcion=request.form.get('descripcion'),
                    fecha=fecha_obj,
                    lugar=request.form.get('lugar'),
                    categoria=request.form.get('categoria'),
                    imagenUrl=request.form.get('imagenUrl')
                )
                db.session.add(e)
                db.session.flush()
                
                # Create a default ticket type
                precio_val = float(request.form.get('precio') or 0)
                tb = TipoBoleto(
                    evento_id=e.id,
                    nombre="General",
                    precio=precio_val
                )
                db.session.add(tb)
                db.session.commit()
                log_auditoria("Agregar Evento", "Evento", f"ID: {e.id}")
                flash("Evento agregado exitosamente")
            except Exception as ex:
                flash(f"Error al agregar evento: {str(ex)}")
        elif action == 'toggle':
            e_id = request.form.get('id')
            e = Evento.query.get(e_id)
            if e:
                e.activo = not e.activo
                db.session.commit()
                log_auditoria("Alternar Evento", "Evento", f"ID: {e.id}, Activo: {e.activo}")
                flash("Estado del evento actualizado")
        return redirect(url_for('admin_eventos'))

    eventos = Evento.query.order_by(Evento.fecha.desc()).all()
    categorias = [r[0] for r in db.session.query(Evento.categoria).distinct().filter(Evento.categoria != None, Evento.categoria != '').all()]
    return render_template('admin/eventos.html', usuario=user, eventos=eventos, categorias=categorias)

@app.route('/admin/eventos/edit/<int:id>', methods=['GET', 'POST'])
def admin_editar_evento(id):
    user = get_current_user()
    if not user or user.rol != 'admin': return redirect(url_for('index'))
    
    e = Evento.query.get_or_404(id)
    if request.method == 'POST':
        import datetime
        try:
            e.titulo = request.form.get('titulo')
            e.descripcion = request.form.get('descripcion')
            e.lugar = request.form.get('lugar')
            e.categoria = request.form.get('categoria')
            e.imagenUrl = request.form.get('imagenUrl')
            
            fecha_str = request.form.get('fecha')
            if fecha_str:
                e.fecha = datetime.datetime.strptime(fecha_str, '%Y-%m-%dT%H:%M')
                
            db.session.commit()
            log_auditoria("Editar Evento", "Evento", f"ID: {e.id}")
            flash("Evento actualizado exitosamente")
            return redirect(url_for('admin_eventos'))
        except Exception as ex:
            flash(f"Error al editar evento: {str(ex)}")
            
    return render_template('admin/editar_evento.html', usuario=user, evento=e)

@app.route('/admin/noticias', methods=['GET', 'POST'])
def admin_noticias():
    user = get_current_user()
    if not user or user.rol != 'admin': return redirect(url_for('index'))
    
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add':
            n = Noticia(
                titulo=request.form.get('titulo'),
                contenido=request.form.get('contenido'),
                imagenUrl=request.form.get('imagenUrl')
            )
            db.session.add(n)
            db.session.commit()
            log_auditoria("Agregar Noticia", "Noticia", f"ID: {n.id}")
            flash("Noticia agregada")
        elif action == 'toggle':
            n_id = request.form.get('id')
            n = Noticia.query.get(n_id)
            if n:
                n.activo = not n.activo
                db.session.commit()
                log_auditoria("Alternar Noticia", "Noticia", f"ID: {n.id}, Activo: {n.activo}")
                flash("Estado de noticia actualizado")
        return redirect(url_for('admin_noticias'))

    noticias = Noticia.query.order_by(Noticia.fechaPub.desc()).all()
    return render_template('admin/noticias.html', usuario=user, noticias=noticias)

@app.route('/admin/eventos/editar/<int:id>', methods=['GET', 'POST'])
def editar_evento(id):
    user = get_current_user()
    if not user or user.rol != 'admin': return redirect(url_for('index'))
    evento = Evento.query.get_or_404(id)
    categorias = [r[0] for r in db.session.query(Evento.categoria).distinct().filter(Evento.categoria != None, Evento.categoria != '').all()]

    if request.method == 'POST':
        evento.titulo = request.form.get('titulo')
        evento.descripcion = request.form.get('descripcion')
        evento.lugar = request.form.get('lugar')
        evento.categoria = request.form.get('categoria')
        evento.imagenUrl = request.form.get('imagenUrl')
        db.session.commit()
        log_auditoria("Editar Evento", "Evento", f"ID: {evento.id}")
        flash("Evento actualizado")
        return redirect(url_for('admin_eventos'))
    return render_template('admin/editar_evento.html', usuario=user, evento=evento, categorias=categorias)

@app.route('/admin/noticia/editar/<int:id>', methods=['GET', 'POST'])
def editar_noticia(id):
    user = get_current_user()
    if not user or user.rol != 'admin': return redirect(url_for('index'))
    
    n = Noticia.query.get_or_404(id)
    if request.method == 'POST':
        n.titulo = request.form.get('titulo')
        n.contenido = request.form.get('contenido')
        n.imagenUrl = request.form.get('imagenUrl')
        db.session.commit()
        log_auditoria("Editar Noticia", "Noticia", f"ID: {n.id}")
        flash("Noticia actualizada")
        return redirect(url_for('admin_noticias'))
        
    return render_template('admin/editar_noticia.html', usuario=user, noticia=n)

@app.route('/admin/faqs', methods=['GET', 'POST'])
def admin_faqs():
    user = get_current_user()
    if not user or user.rol != 'admin': return redirect(url_for('index'))

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add':
            f = PreguntaFrecuente(
                pregunta=request.form.get('pregunta'),
                respuesta=request.form.get('respuesta')
            )
            db.session.add(f)
            db.session.commit()
            log_auditoria("Agregar FAQ", "PreguntaFrecuente", f"ID: {f.id}")
            flash("FAQ agregada")
        elif action == 'toggle':
            f_id = request.form.get('id')
            f = PreguntaFrecuente.query.get(f_id)
            if f:
                f.activo = not f.activo
                db.session.commit()
                log_auditoria("Alternar FAQ", "PreguntaFrecuente", f"ID: {f.id}, Activo: {f.activo}")
                flash("Estado de FAQ actualizado")
        return redirect(url_for('admin_faqs'))

    faqs = PreguntaFrecuente.query.all()
    return render_template('admin/faqs.html', usuario=user, faqs=faqs)

@app.route('/admin/faqs/edit/<int:faq_id>', methods=['GET', 'POST'])
def admin_editar_faq(faq_id):
    user = get_current_user()
    if not user or user.rol != 'admin': return redirect(url_for('index'))
    
    f = PreguntaFrecuente.query.get_or_404(faq_id)
    if request.method == 'POST':
        f.pregunta = request.form.get('pregunta')
        f.respuesta = request.form.get('respuesta')
        db.session.commit()
        log_auditoria("Editar FAQ", "PreguntaFrecuente", f"ID: {f.id}")
        flash("FAQ actualizada exitosamente")
        return redirect(url_for('admin_faqs'))
        
    return render_template('admin/editar_faq.html', usuario=user, faq=f)

@app.route('/admin/mercancia', methods=['GET', 'POST'])
def admin_mercancia():
    user = get_current_user()
    if not user or user.rol != 'admin': return redirect(url_for('index'))

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add':
            m = Mercancia(
                titulo=request.form.get('titulo'),
                descripcion=request.form.get('descripcion'),
                precio=float(request.form.get('precio')),
                categoria=request.form.get('categoria'),
                colores=request.form.get('colores'),
                imagenUrl=request.form.get('imagenUrl')
            )
            db.session.add(m)
            db.session.flush() # Para obtener m.id
            
            stock_inicial = int(request.form.get('stock') or 0)
            inv = InventarioMercancia(mercancia_id=m.id, talla='Única', stock=stock_inicial)
            db.session.add(inv)
            
            db.session.commit()
            log_auditoria("Agregar Mercancia", "Mercancia", f"ID: {m.id}, Stock: {stock_inicial}")
            flash("Mercancia agregada")
        elif action == 'toggle':
            m_id = request.form.get('id')
            m = Mercancia.query.get(m_id)
            if m:
                m.activo = not m.activo
                db.session.commit()
                log_auditoria("Alternar Mercancia", "Mercancia", f"ID: {m.id}, Activo: {m.activo}")
                flash("Estado de Mercancía actualizado")
        return redirect(url_for('admin_mercancia'))

    mercancia = Mercancia.query.order_by(Mercancia.id.desc()).all()
    categorias = [r[0] for r in db.session.query(Mercancia.categoria).distinct().filter(Mercancia.categoria != None, Mercancia.categoria != '').all()]
    return render_template('admin/mercancia.html', usuario=user, mercancia=mercancia, categorias=categorias)

@app.route('/admin/mercancia/editar/<int:id>', methods=['GET', 'POST'])
def editar_mercancia(id):
    user = get_current_user()
    if not user or user.rol != 'admin': return redirect(url_for('index'))
    mercancia = Mercancia.query.get_or_404(id)
    categorias = [r[0] for r in db.session.query(Mercancia.categoria).distinct().filter(Mercancia.categoria != None, Mercancia.categoria != '').all()]

    if request.method == 'POST':
        mercancia.titulo = request.form.get('titulo')
        mercancia.descripcion = request.form.get('descripcion')
        mercancia.precio = float(request.form.get('precio'))
        mercancia.categoria = request.form.get('categoria')
        mercancia.colores = request.form.get('colores')
        mercancia.imagenUrl = request.form.get('imagenUrl')
        
        # Actualizar Inventario
        tallas = request.form.getlist('talla[]')
        stocks = request.form.getlist('stock[]')
        
        for inv in mercancia.inventario:
            db.session.delete(inv)
        
        for talla, stock in zip(tallas, stocks):
            if talla.strip() and stock.strip():
                try:
                    s_val = int(stock)
                    inv = InventarioMercancia(mercancia_id=mercancia.id, talla=talla.strip(), stock=s_val)
                    db.session.add(inv)
                except ValueError:
                    pass
                    
        db.session.commit()
        log_auditoria("Editar Mercancia", "Mercancia", f"ID: {mercancia.id}")
        flash("Mercancía actualizada")
        return redirect(url_for('admin_mercancia'))
    return render_template('admin/editar_mercancia.html', usuario=user, mercancia=mercancia, categorias=categorias)

@app.route('/admin/auditoria')
def admin_auditoria():
    user = get_current_user()
    if not user or user.rol != 'admin': return redirect(url_for('index'))
    logs = Auditoria.query.order_by(Auditoria.fecha.desc()).all()
    return render_template('admin/auditoria.html', usuario=user, logs=logs)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

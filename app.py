import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from models import db, Usuario, Evento, Noticia, Mercancia, PreguntaFrecuente, CarritoItem, Pedido, PedidoItem, Auditoria, MensajeChat, TipoBoleto

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

@app.route('/')
def index():
    user = get_current_user()
    eventos_db = Evento.query.filter_by(activo=True).order_by(Evento.fecha.asc()).limit(3).all()
    eventos = [{
        'id': e.id,
        'cat': e.categoria,
        'tit': e.titulo,
        'precio': f'${e.precio_desde:.2f}',
        'fecha': e.fecha.strftime('%d %b %Y') if e.fecha else 'Por confirmar',
        'lugar': e.lugar,
        'bg': 'from-purple-800 to-purple-400',
        'txt': 'text-purple-600 dark:text-purple-400',
        'tag': 'bg-purple-100 dark:bg-purple-600/20',
        'imagen': e.imagenUrl
    } for e in eventos_db]

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

    return render_template('index.html', usuario=user, eventos=eventos, noticias=noticias, mercancia=mercancia)

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
            if usuario and usuario.password == password:
                session['userId'] = usuario.id
                return redirect(url_for('perfil'))
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
                    password=password,
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
    for i, e in enumerate(eventos_db):
        c = colores[i % len(colores)]
        eventos.append({
            'id': e.id,
            'cat': e.categoria or 'Evento',
            'tit': e.titulo,
            'precio': f'${e.precio_desde:.2f}',
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
    
    eventos_db = Evento.query.filter_by(activo=True).order_by(Evento.fecha.asc()).limit(3).all()
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
    return render_template('precios_vip.html', usuario=user)

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
            except Exception as e:
                print(e)
                error = "Hubo un error al procesar tu pago."

    return render_template('carrito.html', usuario=user, success=success, error=error)

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

@app.route('/perfil/info')
def perfil_info():
    user = get_current_user()
    if not user: return redirect(url_for('auth'))
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
        'eventos': Evento.query.count()
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
                
        return redirect(url_for('admin_aprobaciones'))

    solicitudes = SolicitudVip.query.filter_by(estado='pendiente').all()
    return render_template('admin/aprobaciones.html', usuario=user, solicitudes=solicitudes)

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
                fecha_obj = datetime.datetime.strptime(fecha_str, '%Y-%m-%dT%H:%M') if fecha_str else datetime.datetime.utcnow()
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
                    precio=precio_val,
                    capacidad=100,
                    disponibles=100
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
            db.session.commit()
            log_auditoria("Agregar Mercancia", "Mercancia", f"ID: {m.id}")
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

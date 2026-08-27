import os
from app import app
from models import db, Evento, Mercancia

with app.app_context():
    eventos = Evento.query.all()
    # Unsplash concert/music images
    event_images = [
        "https://images.unsplash.com/photo-1459749411175-04bf5292ceea?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1540039155732-d674d40d1277?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1470229722913-7c092fb11d4e?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1429962714451-bb934ecdc4ec?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?auto=format&fit=crop&q=80&w=800"
    ]
    
    for i, ev in enumerate(eventos):
        ev.imagenUrl = event_images[i % len(event_images)]
    
    mercancias = Mercancia.query.all()
    # Unsplash merch/clothing images
    merch_images = [
        "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1562157873-818bc0726f68?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1576566588028-4147f3842f27?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?auto=format&fit=crop&q=80&w=800"
    ]
    
    for i, m in enumerate(mercancias):
        m.imagenUrl = merch_images[i % len(merch_images)]
        
    db.session.commit()
    print("Database images updated successfully.")

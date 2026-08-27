from app import app, db
from sqlalchemy import text

with app.app_context():
    try:
        # Intenta agregar la columna a la tabla Evento
        db.session.execute(text("ALTER TABLE Evento ADD categoria VARCHAR(100) DEFAULT 'Evento'"))
        db.session.commit()
        print("Columna 'categoria' agregada exitosamente a la tabla Evento.")
    except Exception as e:
        print(f"Error o la columna ya existe: {e}")

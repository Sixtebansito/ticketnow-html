import unittest
from app import app, db
from models import Usuario, Evento, Mercancia

class TicketNowTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_routes(self):
        routes_to_test = [
            '/',
            '/eventos',
            '/noticias',
            '/tienda',
            '/precios-vip',
            '/ayuda',
            '/carrito'
        ]
        
        with app.app_context():
            # Intentar obtener un evento para probar la vista de detalle
            e = Evento.query.first()
            if e:
                routes_to_test.append(f'/detalle-evento/{e.id}')
                
        for route in routes_to_test:
            with self.subTest(route=route):
                response = self.client.get(route)
                # Redirects (302) o OK (200) son aceptables, pero no 500
                self.assertIn(response.status_code, [200, 302], f"Error al cargar {route}, status: {response.status_code}")

if __name__ == '__main__':
    unittest.main()

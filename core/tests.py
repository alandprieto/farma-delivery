from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import (
    Cliente, Direccion, Farmacia, Producto, ObraSocial, DescuentoObraSocial,
)


class DireccionModelTests(TestCase):
    def test_calcular_distancia_misma_ubicacion(self):
        direccion = Direccion.objects.create(
            calle='Calle', numero='1', ciudad='La Plata',
            provincia='Buenos Aires', codigo_postal='1900',
            latitud=-34.9214, longitud=-57.9544,
        )
        self.assertAlmostEqual(direccion.calcular_distancia(direccion), 0.0, places=2)

    def test_calcular_distancia_sin_coordenadas_devuelve_none(self):
        direccion = Direccion.objects.create(
            calle='Calle', numero='1', ciudad='La Plata',
            provincia='Buenos Aires', codigo_postal='1900',
        )
        otra = Direccion.objects.create(
            calle='Calle', numero='2', ciudad='La Plata',
            provincia='Buenos Aires', codigo_postal='1900',
        )
        self.assertIsNone(direccion.calcular_distancia(otra))

    def test_str_direccion(self):
        direccion = Direccion.objects.create(
            calle='Av 7', numero='1000', ciudad='La Plata',
            provincia='Buenos Aires', codigo_postal='1900',
        )
        self.assertEqual(str(direccion), 'Av 7 1000, La Plata, Buenos Aires')


class VistaTests(TestCase):
    def test_home_requiere_login(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_login_valido_redirige_a_home(self):
        user = User.objects.create_user(username='1234567', password='pass12345', email='a@a.com')
        response = self.client.post(reverse('login'), {'username': '1234567', 'password': 'pass12345'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

    def test_login_con_password_incorrecto(self):
        user = User.objects.create_user(username='1234568', password='pass12345', email='b@b.com')
        response = self.client.post(reverse('login'), {'username': '1234568', 'password': 'incorrecta'})
        self.assertEqual(response.status_code, 200)


class FarmaciaConfigTests(TestCase):
    """Pruebas de las vistas de configuración de farmacia (templates faltantes en fase crítica)"""

    def setUp(self):
        self.user = User.objects.create_user(username='farmacia0', password='pass12345', email='f@f.com')
        self.usuario_password = 'pass12345'
        self.direccion = Direccion.objects.create(
            calle='Av 44', numero='700', ciudad='La Plata',
            provincia='Buenos Aires', codigo_postal='1900',
        )
        self.farmacia = Farmacia.objects.create(
            user=self.user,
            nombre='FarmaTest',
            direccion=self.direccion,
            matricula='MAT0001',
            cuit='30111222333',
            telefono='2210000000',
            email_contacto='f@f.com',
            horario_apertura='08:00',
            horario_cierre='20:00',
        )
        self.obra_social = ObraSocial.objects.create(nombre='OS Test', plan='Plan 100')
        self.producto = Producto.objects.create(
            nombre='Ibuprofeno 400',
            precio_base='250.00',
            laboratorio='Bayer',
            farmacia=self.farmacia,
            stock_disponible=10,
        )

    def _login(self):
        self.client.login(username=self.user.username, password=self.usuario_password)

    def test_configuracion_precios_get_200(self):
        self._login()
        response = self.client.get(reverse('configuracion_precios'))
        self.assertEqual(response.status_code, 200)

    def test_crear_descuento_obra_social(self):
        self._login()
        response = self.client.post(reverse('configuracion_precios'), {
            'producto': self.producto.id,
            'obra_social': self.obra_social.id,
            'descuento_porcentaje': '10',
            'descuento_fijo': '',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(DescuentoObraSocial.objects.filter(
            producto=self.producto, obra_social=self.obra_social, activo=True
        ).exists())

    def test_eliminar_descuento_obra_social(self):
        self._login()
        descuento = DescuentoObraSocial.objects.create(
            producto=self.producto,
            obra_social=self.obra_social,
            descuento_porcentaje=10,
        )
        response = self.client.post(reverse('configuracion_precios'), {
            'accion': 'eliminar',
            'descuento_id': descuento.id,
        })
        self.assertEqual(response.status_code, 302)
        descuento.refresh_from_db()
        self.assertFalse(descuento.activo)

    def test_configuracion_cuenta_get_200(self):
        self._login()
        response = self.client.get(reverse('configuracion_cuenta_farmacia'))
        self.assertEqual(response.status_code, 200)

    def test_guardar_configuracion_cuenta(self):
        self._login()
        response = self.client.post(reverse('configuracion_cuenta_farmacia'), {
            'nombre': 'FarmaTest Renombrada',
            'matricula': 'MAT0001',
            'cuit': '30111222333',
            'telefono': '2210000000',
            'email_contacto': 'nuevo@f.com',
            'calle': 'Av 44',
            'numero': '700',
            'ciudad': 'La Plata',
            'provincia': 'Buenos Aires',
            'codigo_postal': '1900',
            'horario_apertura': '09:00',
            'horario_cierre': '21:00',
        })
        self.assertEqual(response.status_code, 302)
        self.farmacia.refresh_from_db()
        self.assertEqual(self.farmacia.nombre, 'FarmaTest Renombrada')
        self.assertEqual(self.farmacia.horario_apertura.strftime('%H:%M'), '09:00')
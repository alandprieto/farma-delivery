from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Cliente, Direccion


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
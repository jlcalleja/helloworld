import http.client
import os
import unittest
from urllib.request import urlopen
from urllib.error import HTTPError

import pytest

BASE_URL = "http://localhost:5000"
BASE_URL_MOCK = "http://localhost:9090"
DEFAULT_TIMEOUT = 2  # in secs

@pytest.mark.api
class TestApi(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(BASE_URL, "URL no configurada")
        self.assertTrue(len(BASE_URL) > 8, "URL no configurada")

    def test_api_add(self):
        url = f"{BASE_URL}/calc/add/1/2"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(
            response.read().decode(), "3", "ERROR ADD"
        )

    def test_api_sqrt(self):
        url = f"{BASE_URL_MOCK}/calc/sqrt/64"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(
            response.read().decode(), "8", "ERROR SQRT"
        )


    # Pruebas nuevas
    
    def test_api_multiply(self):  # Asegúrate de que esta función no esté dentro de test_api_add
        url = f"{BASE_URL}/calc/multiply/2/3"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(
            response.read().decode(), "6", "ERROR MULTIPLY"
        )

    def test_api_divide(self):
        url = f"{BASE_URL}/calc/divide/6/2"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(
            response.read().decode(), "3.0", "ERROR DIVIDE"
        )
        
    def test_api_divide_by_zero(self):
        url = f"{BASE_URL}/calc/divide/6/0"
        try:
            # Llamada a la API
            response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        except HTTPError as e:
            # Verifica que el código de estado sea 406
            assert e.code == 406
            
            # Verifica que el mensaje de error sea el esperado
            error_message = e.read().decode('utf-8')  # Lee el contenido del cuerpo de la respuesta
            assert error_message == "Division by zero is not allowed"
        else:
            # Si no ocurre error, falla el test
            pytest.fail("Expected HTTPError but got successful response")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()

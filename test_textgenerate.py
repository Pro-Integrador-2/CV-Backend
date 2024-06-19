import unittest
from unittest.mock import patch, MagicMock
from textgenerate import make_script, make_script_welcome
import os

from dotenv import load_dotenv
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

load_dotenv()
api_key = os.getenv('API_KEY_MISTRAL')

model = os.getenv('MISTRAL_MODEL', "open-mistral-7b")
client = MistralClient(api_key=api_key)


class TestMakeScript(unittest.TestCase):

    @patch('main.client')
    @patch('main.os.getenv')
    def test_make_script(self, mock_getenv, mock_client):
        # Configurar el entorno simulado
        mock_getenv.side_effect = lambda key, default: {
            'API_KEY_MISTRAL': 'mock_api_key',
            'MISTRAL_MODEL': 'mock_model'
        }.get(key, default)

        mock_chat_response = MagicMock()
        mock_chat_response.choices[0].message.content.strip.return_value = "Se ha identificado una llave y una persona"
        mock_client.chat.return_value = mock_chat_response

        # Llamar a la función y verificar el resultado
        result = make_script("texto de prueba", language='es')
        self.assertEqual(result, "Se ha identificado una llave y una persona")

    @patch('main.client')
    @patch('main.os.getenv')
    def test_make_script_welcome(self, mock_getenv, mock_client):
        # Configurar el entorno simulado
        mock_getenv.side_effect = lambda key, default: {
            'API_KEY_MISTRAL': 'mock_api_key',
            'MISTRAL_MODEL': 'mock_model'
        }.get(key, default)

        mock_chat_response = MagicMock()
        mock_chat_response.choices[
            0].message.content.strip.return_value = "Soy un asistente encargado de leer un texto en el idioma español..."
        mock_client.chat.return_value = mock_chat_response

        # Llamar a la función y verificar el resultado
        result = make_script_welcome(language_code='es')
        expected_result = "Soy un asistente encargado de leer un texto en el idioma español..."
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()

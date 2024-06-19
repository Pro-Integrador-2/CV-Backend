import unittest
from unittest.mock import patch, MagicMock
import os
import tempfile
import boto3
from voicegenerate import make_voice

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')


class TestMakeVoice(unittest.TestCase):

    @patch('boto3.client')
    @patch('os.getenv')
    def test_make_voice(self, mock_getenv, mock_boto3_client):
        # Configurar el entorno simulado
        mock_getenv.side_effect = lambda key, default: {
            'AWS_ACCESS_KEY_ID': 'mock_access_key_id',
            'AWS_SECRET_ACCESS_KEY': 'mock_secret_access_key'
        }.get(key, default)

        # Crear un objeto MagicMock para simular el cliente de Polly
        mock_polly_client = MagicMock()
        mock_boto3_client.return_value = mock_polly_client

        # Configurar el comportamiento simulado de synthesize_speech
        mock_audio_stream = MagicMock()
        mock_response = {'AudioStream': mock_audio_stream}
        mock_polly_client.synthesize_speech.return_value = mock_response

        # Llamar a la función y verificar el resultado
        text = "Prueba de texto"
        language_code = "es"
        result = make_voice(text, language_code)

        # Verificar que se llamó a synthesize_speech con los parámetros correctos
        mock_polly_client.synthesize_speech.assert_called_once_with(
            Text=text,
            OutputFormat='mp3',
            VoiceId='Lucia'  # Suponiendo que 'es' corresponde a 'Lucia' según tu configuración
        )

        # Verificar que se haya creado un archivo temporal con la extensión .mp3
        self.assertTrue(result.endswith('.mp3'))
        self.assertTrue(os.path.exists(result))

        # Opcional: limpiar el archivo temporal creado
        if os.path.exists(result):
            os.remove(result)


if __name__ == '__main__':
    unittest.main()

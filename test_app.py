import unittest
import eventlet
from app import app, socketio
from flask_socketio import SocketIOTestClient
from PIL import Image
from io import BytesIO
import base64

eventlet.monkey_patch()


def jpeg_to_base64(image_path):
    image = Image.open(image_path)
    # Convertir la imagen a un objeto binario
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    image_bytes = buffered.getvalue()
    # Codificar los bytes de la imagen en base64
    base64_string = base64.b64encode(image_bytes).decode("utf-8")
    return base64_string


imagTr = jpeg_to_base64("h1.jpeg")
IMAGE_DATA_BASE64 = imagTr


class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = socketio.test_client(self.app)
        self.client.connect()

    def tearDown(self):
        if self.client.is_connected():
            self.client.disconnect()
        self.app_context.pop()

    def test_handle_connect(self):
        self.assertTrue(self.client.is_connected())
        self.client.emit('connect')
        received = self.client.get_received()
        self.assertTrue(any(event['name'] == 'connect' for event in received))

    def test_handle_disconnect(self):
        self.assertTrue(self.client.is_connected())
        self.client.disconnect()
        self.assertFalse(self.client.is_connected())

    def test_handle_upload_image_with_image(self):
        self.client.emit('upload_image', {'image': IMAGE_DATA_BASE64, 'language_code': 'es'})
        received = self.client.get_received()
        print(received)
        self.assertTrue(any(event['name'] == 'audio-detection' for event in received))

    def test_handle_voice_guide(self):
        self.client.emit('voice_guide', {'language_code': 'es'})
        received = self.client.get_received()
        print(received)
        self.assertTrue(any(event['name'] == 'audio-guide' for event in received))


if __name__ == '__main__':
    unittest.main()

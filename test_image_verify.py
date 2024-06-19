import unittest
import cv2
import numpy as np
from PIL import Image
from image_verify import compare_images


class TestCompareImages(unittest.TestCase):

    def setUp(self):

        self.image1 = Image.open('f1.jpeg')
        self.image2 = Image.open('f2.jpeg')

    def test_similarity_threshold(self):
        # Convertir imágenes a bytes
        image1_bytes = np.array(self.image1)
        image2_bytes = np.array(self.image2)

        # Llamar a la función y verificar el resultado
        result = compare_images(image1_bytes.tobytes(), image2_bytes.tobytes())
        self.assertTrue(result)

    def test_different_images(self):
        # Crear imágenes diferentes
        different_image1 = Image.new('RGB', (100, 100), color=(255, 0, 0))
        different_image2 = Image.new('RGB', (100, 100), color=(0, 255, 0))

        # Convertir imágenes a bytes
        diff_image1_bytes = np.array(different_image1)
        diff_image2_bytes = np.array(different_image2)

        # Llamar a la función y verificar el resultado
        result = compare_images(diff_image1_bytes.tobytes(), diff_image2_bytes.tobytes())
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()

import cv2
import numpy as np
from PIL import Image


def compare_images(image1_bytes, image2_bytes):
    # Convertir las imágenes en bytes a arrays de imágenes
    nparr1 = np.frombuffer(image1_bytes, np.uint8)
    nparr2 = np.frombuffer(image2_bytes, np.uint8)
    image1 = cv2.imdecode(nparr1, cv2.IMREAD_COLOR)
    image2 = cv2.imdecode(nparr2, cv2.IMREAD_COLOR)

    # Crear el detector ORB
    orb = cv2.ORB_create()

    # Detectar y computar los descriptores keypoints
    keypoints1, descriptors1 = orb.detectAndCompute(image1, None)
    keypoints2, descriptors2 = orb.detectAndCompute(image2, None)

    # Usar el comparador BFMatcher para encontrar las mejores coincidencias
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(descriptors1, descriptors2)

    if len(matches) == 0:
        return False

    # Ordenar las coincidencias según la distancia
    matches = sorted(matches, key=lambda x: x.distance)

    # Calcular el puntaje de similitud (menor es mejor)
    similarity_score = sum(match.distance for match in matches) / len(matches)
    return similarity_score > 30
    


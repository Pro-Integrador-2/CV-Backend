import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image
import numpy as np
import io


GOOGLE_API_KEY = os.getenv('API_GEMINI')
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro-vision')

#img = PIL.Image.open('b1.jpeg')  # Impresora, marco de fotos, regleta, router, caja de zapatos


def detectar_objeto(image_bytes, language='es'):

    img = Image.open(io.BytesIO(image_bytes))
    cookie_picture = {
        'mime_type': 'image/jpeg',
        'data': io.BytesIO(image_bytes),
    }
    print("Se abre imagenn")
    try:
        if language == 'es':
            print(" ingresa if promt en español")
            response = model.generate_content( [
            "¿Qué objetos se detectan en la imagen?, solo dime los nombres de los objetos de mayor confianza, no digas 'se detecta en la imagen', sino lista los nombres"
            , cookie_picture])
            print("se genera el promt")
        elif language == 'en':
            response = model.generate_content([
            "What objects are detected in the image?, only the names of the objects with the highest confidence should be provided, don't say 'it is detected in the image', but list the names"
            , img], stream=True)
        elif language == 'fr':
            response = model.generate_content([
            "Quels objets sont détectés dans l'image ? Je ne vais énumérer que les noms des objets avec le plus haut niveau de confiance, mais liste simplement les noms"
            , img], stream=True)
        elif language == 'it':
            response = model.generate_content([
            """Quali oggetti vengono rilevati nell'immagine? Dimmi solo i nomi degli oggetti più affidabili, non dire  "è stato rilevato nell'immagine " , ma elenca i nomi"""
            , img], stream=True)
        elif language == 'pr':  
            response = model.generate_content([
            "Quais objetos são detectados na imagem? Apenas me diga os nomes dos objetos mais confiáveis, não diga 'é detectado na imagem', mas liste os nomes"
            , img], stream=True)

        response.resolve()
        print("respuestaaaaa")

        if len(response.candidates) > 0 and len(response.candidates[0].content.parts) > 0:
            text = response.candidates[0].content.parts[0].text
            return text
        else:
            print("No text found in the response.")
    except Exception as e:
        print(f"An error occurred: {e}")


#print(detectar_objeto(img))
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv('API_KEY_MISTRAL')

#model = "mistral-large-latest"
model = "open-mistral-7b"
client = MistralClient(api_key=api_key)

def make_script(text):
    try:
        if not api_key:
            raise Exception('API_KEY no está configurada en el archivo .env')
        formato_entrada = text 

        salida_esperada="""Se ha identificado una llave y una persona"""
        
        contexto = """Soy un asistente encargado de leer el siguiente texto """ + "\n" + formato_entrada + """ y debo generar un texto descriptivo que mencione sólo los nombres en español de los elementos identificados, debo  eliminar palabras que son sinónimos, palabras que son iguales o redundantes, debo eliminar sugerencias o inferencias, no debo escribir tantos datos del archivo, solo debo decir los nombres de los objetos. Siempre debo iniciar el texto como 'se ha identificado...'  tengo que ser muy breve  """ + "\n\nUn Ejemplo del texto generado en español sería:""" + "\n" + salida_esperada

        prompt = contexto

        messages = [ChatMessage(role="user", content=prompt)]

        chat_response = client.chat(
            model=model,
            response_format={"type": "text"},
            messages=messages,
        )
        little_paragraph = chat_response.choices[0].message.content.strip()

        return little_paragraph
    except Exception as e:
        print(e)
        return "Error con Mistral"


def make_script_welcome(language_code='es'):
    try:
        if not api_key:
            raise Exception('API_KEY no está configurada en el archivo .env')

        # Mapear el código de idioma a una descripción del idioma
        languages = {
            'es': 'español',
            'en': 'inglés',
            'fr': 'francés'
        }
        language = languages.get(language_code, 'español')
        text = ("Bienvenido a Clear Vision, una herramienta innovadora para personas con discapacidad visual. "
                "Apunta la cámara a los objetos que desees identificar, y la aplicación utilizará inteligencia artificial "
                "para identificarlos y anunciar su nombre. Puedes explorar tu entorno de forma más independiente y segura. "
                "¡Empecemos!")
        contexto = (f"Soy un asistente encargado de leer un texto en el idioma {language}\n"
                    f"Y debo generar un texto en el idioma {language} similar al siguiente que mencione cómo funciona la aplicación :\n\"{text}\""
                    "La guía debe ser corta, no mas de 50 palabras"
                    "Las palabras \"Clear Vision\" son un nombre propio y no deseo traducirlas"
                    f"El texto de respuesta debe estar en {language}.")


        messages = [ChatMessage(role="user", content=contexto)]

        chat_response = client.chat(
            model=model,
            response_format={"type": "text"},
            messages=messages,
        )
        little_paragraph = chat_response.choices[0].message.content.strip()
        return little_paragraph
    except Exception as e:
        print(e)
        return "Error con Mistral"
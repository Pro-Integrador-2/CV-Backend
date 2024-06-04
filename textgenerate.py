from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv('API_KEY_MISTRAL')

#model = "mistral-large-latest"
model = "open-mistral-7b"
client = MistralClient(api_key=api_key)

def make_script(text, language='es'):
    try:
        if not api_key:
            raise Exception('API_KEY no está configurada en el archivo .env')

        if language == 'es':
            salida_esperada = "Se ha identificado una llave y una persona"
            contexto = f"""Soy un asistente encargado de leer el siguiente texto "{text}" y debo generar un texto descriptivo que mencione sólo los nombres en español de los elementos identificados. Debo eliminar palabras que son sinónimos, palabras que son iguales o redundantes, debo eliminar sugerencias o inferencias, no debo escribir tantos datos del archivo, solo debo decir los nombres de los objetos. Siempre debo iniciar el texto como 'se ha identificado...' Tengo que ser muy breve. Un ejemplo del texto generado en español sería: "{salida_esperada}"."""
        elif language == 'en':
            salida_esperada = "A key and a person have been identified"
            contexto = f"""I am an assistant tasked with reading the following text "{text}" and generating a descriptive text that mentions only the names of the identified elements in English. I must eliminate words that are synonyms, words that are identical or redundant, I must eliminate suggestions or inferences, I should not write too much data from the file, I should only mention the names of the objects. I must always start the text with 'identified...'. I have to be very brief. An example of the generated text in English would be: "{salida_esperada}"."""
        elif language == 'fr':
            salida_esperada = "Une clé et une personne ont été identifiées"
            contexto = f"""Je suis un assistant chargé de lire le texte suivant "{text}" et de générer un texte descriptif mentionnant uniquement les noms des éléments identifiés en français. Je dois éliminer les mots qui sont des synonymes, les mots qui sont identiques ou redondants, je dois éliminer les suggestions ou les inférences, je ne dois pas écrire trop de données du fichier, je dois seulement mentionner les noms des objets. Je dois toujours commencer le texte par 'identifié...'. Je dois être très bref. Un exemple du texte généré en français serait : "{salida_esperada}"."""
        else:
            raise ValueError("Unsupported language")

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
                "para identificarlos y anunciar su nombre. "
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
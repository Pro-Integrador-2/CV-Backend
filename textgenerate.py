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
            instrucciones = """ 1. Si el texto está vacío, la salida debe ser: 'No he podido identificar objetos' \n2. Si se identifican objetos en el texto, la salida debe seguir el formato: "Se ha identificado...". \n3. Elimina sinónimos, palabras redundantes y sugerencias o inferencias. \n 4. No debo proporcionar demasiados detalles, solo los nombres de los objetos. \n 5. Siempre debo comenzar la respuesta con "Se ha identificado..." """
            contexto = f"""Soy un asistente encargado de leer el siguiente texto: "{text}". Mi tarea es generar una descripción breve que mencione únicamente los nombres de los objetos identificados en español, debo seguir las siguientes instrucciones: {instrucciones}, un ejemplo del texto generado es: {salida_esperada}"""

        elif language == 'en':
            salida_esperada = "A key and a person have been identified"
            instrucciones =  """1. If the text is empty, the output should be: 'I couldn't identify any objects' \n 2. If objects are identified in the text, the output should follow the format: "The following objects have been identified... \n 3.Remove synonyms, redundant words, and suggestions or inferences. \n 4. I should not provide too many details, only the names of the objects. \n 5.I should always start the response with "The following objects have been identified..."  """
            contexto = f"""I am an assistant tasked with reading the following text "{text}" and generating a descriptive text that mentions only the names of the identified elements in English. I must follow the following instructions:{instrucciones}. An example of the generated text in English would be: "{salida_esperada}"."""
        elif language == 'fr':
            salida_esperada = "Une clé et une personne ont été identifiées"
            instrucciones= """ 1. Si le texte est vide, la sortie doit être : 'Je n'ai pas pu identifier d'objets' \n 2. Si des objets sont identifiés dans le texte, la sortie doit suivre le format : "Les objets suivants ont été identifiés... \n 3.Supprimez les synonymes, les mots redondants et les suggestions ou les inférences.\n 4.Je ne devrais pas fournir trop de détails, seulement les noms des objets.\n5. Je dois toujours commencer la réponse par "Les objets suivants ont été identifiés..."  """
            contexto = f"""Je suis un assistant chargé de lire le texte suivant "{text}" et de générer un texte descriptif mentionnant uniquement les noms des éléments identifiés en français. Je dois suivre les instructions suivantes:{instrucciones},  Un exemple du texte généré en français serait : "{salida_esperada}"."""
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
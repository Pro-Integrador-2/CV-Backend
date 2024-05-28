from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import os
from dotenv import load_dotenv


def make_script(text):
    try:
        load_dotenv()
        api_key = os.getenv('API_KEY_MISTRAL')

        if not api_key:
            raise Exception('API_KEY no está configurada en el archivo .env')

        #model = "mistral-large-latest"
        model = "open-mistral-7b"

        client = MistralClient(api_key=api_key)

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
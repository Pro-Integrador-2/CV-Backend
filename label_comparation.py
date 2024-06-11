import os
from dotenv import load_dotenv
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

load_dotenv()
api_key = os.getenv('API_KEY_MISTRAL')

model = "mistral-large-latest"
#model = "open-mistral-7b"
client = MistralClient(api_key=api_key)


def make_label_comparison(etiqueta_actual, etiqueta_anterior):
    prompt = (
        f"Responde con 'true' o 'false. En la salida No acepto texto, solo true o false"
        f"Estás ayudando a una persona con discapacidad visual a entender su entorno. "
        f"Comparar las etiquetas de los objetos detectados actualmente: {etiqueta_actual} con las etiquetas de los objetos detectados anteriormente: {etiqueta_anterior}. "
        f"Si los objetos actuales son los mismos que los anteriores, respondes false. "
        f"Si hay cambios significativos en los objetos detectados (es decir, hay objetos nuevos que no estaban antes o desaparecieron algunos objetos), retornar true."
    )

    messages = [ChatMessage(role="user", content=prompt)]

    try:
        chat_response = client.chat(
            model=model,
            response_format={"type": "text"},
            messages=messages,
        )
        response_content = chat_response.choices[0].message.content.strip().lower()

        return True if "true" in response_content else False

    except Exception as e:
        print(f"Ocurrió un error al obtener la respuesta: {e}")
        return None



import os

from dotenv import load_dotenv
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

load_dotenv()
api_key = os.getenv('API_KEY_MISTRAL')

# model = "mistral-large-latest"
model = "open-mistral-7b"
client = MistralClient(api_key=api_key)


def make_script(text, language='es'):
    try:
        if not api_key:
            raise Exception('API_KEY no está configurada en el archivo .env')

        if language == 'es':
            salida_esperada = "Se ha identificado una llave y una persona"
            instrucciones = (
                "1. Si el texto está vacío, la salida debe ser: 'No he podido identificar objetos'.\n"
                "2. Si se identifican objetos en el texto, la salida debe seguir el formato: 'Se ha identificado...'.\n"
                "3. Elimina sinónimos, palabras redundantes y sugerencias o inferencias.\n"
                "4. No proporcionar demasiados detalles, solo los nombres de los objetos.\n"
                "5. Siempre debo comenzar la respuesta con 'Se ha identificado...'.\n"
                "6. Siempre debo mencionar un mismo objeto una sola vez, aunque aparezca varias veces en la lista de objetos identificados.\n"
                "7. Las respuestas deben ser concisas y claras."
            )
            contexto = (
                f"Soy un asistente encargado de procesar la siguiente lista de etiquetas detectadas en imágenes tomadas en un periodo de 4 segundos: \"{text}\". "
                f"Mi tarea es generar una descripción breve que mencione únicamente los nombres de los objetos identificados en todas las imágenes en español. "
                f"Debo seguir las siguientes instrucciones: {instrucciones} "
                f"Un ejemplo del texto generado es: {salida_esperada}."
            )
        elif language == 'en':
            salida_esperada = "A key and a person have been identified"
            instrucciones = (
                "1. If the text is empty, the output should be: 'I couldn't identify any objects'.\n"
                "2. If objects are identified in the text, the output should follow the format: 'The following objects have been identified...'.\n"
                "3. Remove synonyms, redundant words, and suggestions or inferences.\n"
                "4. I should not provide too many details, only the names of the objects.\n"
                "5. I should always start the response with 'The following objects have been identified...'.\n"
                "6. I should always mention an object only once, even if it appears multiple times in the list of identified objects.\n"
                "7. Responses should be concise and clear."
            )
            contexto = (
                f"I am an assistant tasked with processing the following list of labels detected in images taken over a period of 4 seconds: \"{text}\". "
                f"My task is to generate a brief description that mentions only the names of the identified objects in all the images in English. "
                f"I must follow these instructions: {instrucciones} "
                f"An example of the generated text is: {salida_esperada}."
            )
        elif language == 'fr':
            salida_esperada = "Une clé et une personne ont été identifiées"
            instrucciones = (
                "1. Si le texte est vide, la sortie doit être : 'Je n'ai pas pu identifier d'objets'.\n"
                "2. Si des objets sont identifiés dans le texte, la sortie doit suivre le format : 'Les objets suivants ont été identifiés...'.\n"
                "3. Supprimez les synonymes, les mots redondants et les suggestions ou les inférences.\n"
                "4. Je ne devrais pas fournir trop de détails, seulement les noms des objets.\n"
                "5. Je dois toujours commencer la réponse par 'Les objets suivants ont été identifiés...'.\n"
                "6. Je dois toujours mentionner un même objet une seule fois, même s'il apparaît plusieurs fois dans la liste des objets identifiés.\n"
                "7. Les réponses doivent être concises et claires."
            )
            contexto = (
                f"Je suis un assistant chargé de traiter la liste suivante des étiquettes détectées dans des images prises sur une période de 4 secondes : \"{text}\". "
                f"Ma tâche est de générer une description brève mentionnant uniquement les noms des objets identifiés dans toutes les images en français. "
                f"Je dois suivre les instructions suivantes : {instrucciones} "
                f"Un exemple du texte généré est : {salida_esperada}."
            )
        elif language == 'pt':
            salida_esperada = "Uma chave e uma pessoa foram identificadas"
            instrucciones = (
                "1. Se o texto estiver vazio, a saída deve ser: 'Não consegui identificar objetos'.\n"
                "2. Se objetos forem identificados no texto, a saída deve seguir o formato: 'Os seguintes objetos foram identificados...'.\n"
                "3. Remova sinônimos, palavras redundantes e sugestões ou inferências.\n"
                "4. Não devo fornecer muitos detalhes, apenas os nomes dos objetos.\n"
                "5. Sempre devo começar a resposta com 'Os seguintes objetos foram identificados...'.\n"
                "6. Sempre devo mencionar um mesmo objeto apenas uma vez, mesmo que apareça várias vezes na lista de objetos identificados.\n"
                "7. As respostas devem ser concisas e claras."
            )
            contexto = (
                f"Sou um assistente encarregado de processar a seguinte lista de etiquetas detectadas em imagens tiradas em um período de 4 segundos: \"{text}\". "
                f"Minha tarefa é gerar uma descrição breve que mencione apenas os nomes dos objetos identificados em todas as imagens em português. "
                f"Devo seguir as seguintes instruções: {instrucciones} "
                f"Um exemplo do texto gerado é: {salida_esperada}."
            )
        elif language == 'it':
            salida_esperada = "È stata identificata una chiave e una persona"
            instrucciones = (
                "1. Se il testo è vuoto, l'output deve essere: 'Non sono riuscito a identificare alcun oggetto'.\n"
                "2. Se nel testo vengono identificati oggetti, l'output deve seguire il formato: 'Sono stati identificati i seguenti oggetti...'.\n"
                "3. Rimuovi sinonimi, parole ridondanti e suggerimenti o inferenze.\n"
                "4. Non dovrei fornire troppi dettagli, solo i nomi degli oggetti.\n"
                "5. Dovrei sempre iniziare la risposta con 'Sono stati identificati i seguenti oggetti...'.\n"
                "6. Dovrei sempre menzionare un oggetto solo una volta, anche se appare più volte nell'elenco degli oggetti identificati.\n"
                "7. Le risposte dovrebbero essere concise e chiare."
            )
            contexto = (
                f"Sono un assistente incaricato di elaborare il seguente elenco di etichette rilevate in immagini scattate in un periodo di 4 secondi: \"{text}\". "
                f"Il mio compito è generare una breve descrizione che menzioni solo i nomi degli oggetti identificati in tutte le immagini in italiano. "
                f"Devo seguire le seguenti istruzioni: {instrucciones} "
                f"Un esempio del testo generato è: {salida_esperada}."
            )
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
        return "Error con Mistral"


def make_script_welcome(language_code='es'):
    try:
        if not api_key:
            raise Exception('API_KEY no está configurada en el archivo .env')

        # Mapear el código de idioma a una descripción del idioma
        languages = {
            'es': 'español',
            'en': 'inglés',
            'fr': 'francés',
            'pt': 'portugues',
            'it': 'italiano'
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
        return "Error con Mistral"
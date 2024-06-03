import boto3
import os
import tempfile
from dotenv import load_dotenv

load_dotenv()
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

def make_voice(text, language_code = "es"):
    # Crear un cliente de Polly
    polly_client = boto3.client('polly', region_name='us-east-1',
                                aws_access_key_id=AWS_ACCESS_KEY_ID,
                                aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    voices = {
        'es': 'Lucia',  # Español
        'en': 'Joanna',  # Inglés
        'fr': 'Celine'  # Francés
    }
    voice_id = voices.get(language_code, 'Lucia')

    # Generar el audio a partir del texto
    response = polly_client.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId=voice_id
    )
    
    # Guardar el audio en un archivo temporal
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
        tmp_file_path = tmp_file.name
        tmp_file.write(response['AudioStream'].read())

    return tmp_file_path

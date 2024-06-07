import base64
import json
import os
import boto3
from dotenv import load_dotenv
from flask import Flask, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from datetime import datetime, timedelta
from textgenerate import make_script, make_script_welcome
from voicegenerate import make_voice

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

load_dotenv()
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

# Diccionario para almacenar las detecciones y la última actualización de cada conexión
connections = {}


@socketio.on('connect')
def handle_connect():
    session_id = request.sid
    connections[session_id] = {'last_detection': None, 'last_update': datetime.utcnow()}
    print(f"Client connected: {session_id}")


@socketio.on('disconnect')
def handle_disconnect():
    session_id = request.sid
    if session_id in connections:
        del connections[session_id]
    print(f"Client disconnected: {session_id}")


@socketio.on('upload_image')
def handle_upload_image(data):
    def detect_labels_in_image(image_bytes):
        client = boto3.client('rekognition', region_name="us-east-1",
                              aws_access_key_id=AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        response = client.detect_labels(
            Image={'Bytes': image_bytes},
            MaxLabels=10,
            MinConfidence=75
        )
        return json.dumps(response['Labels'])

    if not data or 'image' not in data:
        emit('error', {"error": "No image provided"})
        return

    image_data = data['image']
    language = data.get("language_code", "es")

    if image_data.startswith('data:image'):
        image_data = image_data.split(',')[1]

    try:
        image_bytes = base64.b64decode(image_data)
        if image_bytes:
            labels = detect_labels_in_image(image_bytes)
            currentDetection = make_script(labels, language)
            print('objetos -----------> ', currentDetection)
            current_time = datetime.utcnow()
            session_id = request.sid

            if session_id in connections:
                last_detection = connections[session_id]['last_detection']
                last_update = connections[session_id]['last_update']

                if currentDetection != last_detection or current_time - last_update > timedelta(minutes=1):
                    connections[session_id]['last_detection'] = currentDetection
                    connections[session_id]['last_update'] = current_time

                    audio_file_path = make_voice(currentDetection, language)
                    with open(audio_file_path, 'rb') as f:
                        audio_data = f.read()
                    audio_base64 = base64.b64encode(audio_data).decode('utf-8')
                    emit('audio-detection', {'audio': audio_base64, 'session_id': session_id})
    except Exception as e:
        emit('error', {"error": str(e)})


@socketio.on('voice_guide')
def handle_voice_guide(data):
    language = data.get("language_code", "es")
    try:
        welcome_text = make_script_welcome(language)
        audio_path = make_voice(welcome_text, language)
        with open(audio_path, 'rb') as f:
            audio_data = f.read()
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        emit('audio-guide', {'audio': audio_base64})
    except Exception as e:
        emit('error', {"error": str(e)})


if __name__ == '__main__':
    socketio.run(app, debug=True)

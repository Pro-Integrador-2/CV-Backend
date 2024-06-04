import os
import tempfile
import cv2
import boto3
import json
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from dotenv import load_dotenv
import base64
from textgenerate import make_script, make_script_welcome
from voicegenerate import make_voice


app = Flask(__name__)
CORS(app)

load_dotenv()
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

def extract_frame(video_path):
    vidcap = cv2.VideoCapture(video_path)
    success, image = vidcap.read()
    image_bytes = None
    print(f"Video path: {video_path}, Success: {success}")
    if success:
        _, buffer = cv2.imencode('.jpg', image)
        image_bytes = buffer.tobytes()
    vidcap.release()
    return image_bytes


@app.route('/upload-image', methods=['POST'])
def uploadImage():
    data = request.get_json()

    if not data or 'image' not in data or 'language' not in data:
        return jsonify({"error": "No image or language provided"}), 400

    image_data = data['image']
    language = data['language']

    if image_data.startswith('data:image'):
        image_data = image_data.split(',')[1]

    try:
        image_bytes = base64.b64decode(image_data)
        if image_bytes:
            labels = detect_labels_in_image(image_bytes)
            newlabels =json.dumps(labels)
            mytext = make_script(newlabels, language)
            print('objetos -----------> ', mytext)
            audio_file_path = make_voice(mytext, language)

        #return jsonify({"success": mytext}), 200
        return send_file(audio_file_path, as_attachment=True, mimetype='audio/mp3')
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    



def detect_labels_in_image(image_bytes):
    client = boto3.client('rekognition', region_name="us-east-1",
                          aws_access_key_id=AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    response = client.detect_labels(
        Image={'Bytes': image_bytes},
        MaxLabels=10,
        MinConfidence=75
    )
    return response['Labels']

@app.route('/voice-guide', methods=['POST'])
def initVoiceGuide():
    data = request.get_json()

    language = data.get("language_code", "es")
    try:
        welcome_text = make_script_welcome(language)
        audio_path = make_voice(welcome_text, language)
        return send_file(audio_path, as_attachment=True, download_name='output.mp3', mimetype='audio/mp3')
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)


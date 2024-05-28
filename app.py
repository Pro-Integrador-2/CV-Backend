import os
import tempfile
import cv2
import boto3
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import base64
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

@app.route('/upload', methods=['POST'])
def upload_video():
    video_file = request.files['video']
    tmp_file_path = None
    frame = None
    labels = []

    try:
        # Use a temporary file to store the uploaded video
        with tempfile.NamedTemporaryFile(delete=False, suffix='.webm') as tmp_file:
            tmp_file_path = tmp_file.name
            video_file.save(tmp_file_path)

        frame = extract_frame(tmp_file_path)
        if frame:
            labels = detect_labels_in_image(frame)
            print(f"Labels: {labels}")

    except Exception as e:
        print(f"Error processing video: {e}")


    return jsonify({'labels': labels})

@app.route('/upload-image', methods=['POST'])
def uploadImage():
    data = request.get_json()

    if not data or 'image' not in data:
        return jsonify({"error": "No image provided"}), 400

    image_data = data['image']

    if image_data.startswith('data:image'):
        image_data = image_data.split(',')[1]

    try:
        image_bytes = base64.b64decode(image_data)
        if image_bytes:
            labels = detect_labels_in_image(image_bytes)
            print(f"Labels: {labels}")

        return jsonify({"success": labels}), 200
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

if __name__ == '__main__':
    app.run(debug=True)


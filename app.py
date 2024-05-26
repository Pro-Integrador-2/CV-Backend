import os
import tempfile
import cv2
import boto3
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

load_dotenv()
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')


def extract_frame(video_path):
    vidcap = cv2.VideoCapture(video_path)
    success, image = vidcap.read()
    image_bytes = None
    if success:
        _, buffer = cv2.imencode('.jpg', image)
        image_bytes = buffer.tobytes()
    return image_bytes


@app.route('/upload', methods=['POST'])
def upload_video():
    video_file = request.files['video']
    tmp_file_path = None
    frame = None
    labels = None
    print(video_file.filename)
    try:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file_path = tmp_file.name
            video_file.save(tmp_file.name)

        frame = extract_frame(tmp_file_path)
        labels = detect_labels_in_image(frame)
        print(labels)
    except Exception as e:
        print(f"Error processing video: {e}")
    finally:
        if tmp_file_path:
            os.unlink(tmp_file_path)

    return jsonify({'success': True, 'frame': frame, 'labels': labels})


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

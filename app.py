import os
import boto3
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

load_dotenv()
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')


s3_client = boto3.client('s3', region_name=AWS_REGION,
                         aws_access_key_id=AWS_ACCESS_KEY_ID,
                         aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

rekognition_client = boto3.client('rekognition', region_name=AWS_REGION,
                                  aws_access_key_id=AWS_ACCESS_KEY_ID,
                                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY)


@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return "No video file part", 400
    file = request.files['video']
    if file.filename == '':
        return "No selected file", 400
    print('S3_BUCKET_NAME:', S3_BUCKET_NAME)
    filename = secure_filename(file.filename)
    print('filename:', filename, file.filename)
    print(s3_client.upload_fileobj(file, S3_BUCKET_NAME, filename, ExtraArgs={'ContentType': 'video/webm'}))

    response = rekognition_client.start_label_detection(
        Video={'S3Object': {'Bucket': S3_BUCKET_NAME, 'Name': filename}},
        MinConfidence=50
    )
    print(response)
    return jsonify({}), 200


if __name__ == '__main__':
    app.run(debug=True)

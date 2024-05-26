import os
import boto3
import json
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from analizer import VideoDetect
app = Flask(__name__)
CORS(app)

load_dotenv()
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
SNS_TOPIC_ARN = os.getenv('SNS_TOPIC_ARN')
IAM_ROLE_ARN = os.getenv('IAM_ROLE_ARN')

s3_client = boto3.client('s3', region_name=AWS_REGION,
                         aws_access_key_id=AWS_ACCESS_KEY_ID,
                         aws_secret_access_key=AWS_SECRET_ACCESS_KEY)



@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return "No video file part", 400
    file = request.files['video']
    if file.filename == '':
        return "No selected file", 400

    filename = secure_filename(file.filename)
    print('filename:', filename, file.filename)
    s3_client.upload_fileobj(file, S3_BUCKET_NAME, filename, ExtraArgs={'ContentType': 'video/webm'})
    analyzer = VideoDetect(filename)
    analyzer.CreateTopicandQueue()

    analyzer.StartLabelDetection()
    if analyzer.GetSQSMessageSuccess():
        analyzer.GetLabelDetectionResults()

    analyzer.DeleteTopicandQueue()


    return jsonify({}), 200


if __name__ == '__main__':
    app.run(debug=True)
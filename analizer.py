import json
import os
import time
import boto3
from dotenv import load_dotenv

load_dotenv()


class VideoDetect:
    jobId = ''


    bucket = os.getenv('S3_BUCKET_NAME')
    video = ''
    startJobId = ''
    sqsQueueUrl = ''
    snsTopicArn = os.getenv('SNS_TOPIC_ARN')
    processType = ''
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    rek = boto3.client('rekognition', region_name="us-east-1",
                                  aws_access_key_id=AWS_ACCESS_KEY_ID,
                                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    sqs = boto3.resource('sqs', region_name="us-east-1",
                                  aws_access_key_id=AWS_ACCESS_KEY_ID,
                                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    sns = boto3.resource('sns', region_name="us-east-1",
                                  aws_access_key_id=AWS_ACCESS_KEY_ID,
                                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    iam = boto3.resource('iam', region_name="us-east-1",
                                  aws_access_key_id=AWS_ACCESS_KEY_ID,
                                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    topic = None
    queue = None
    def __init__(self, video):
        self.video = video

    def GetSQSMessageSuccess(self):
        status = None
        job_done = False
        while not job_done:
            messages = self.queue.receive_messages(
                MaxNumberOfMessages=1, WaitTimeSeconds=5
            )
            print(messages)
            if messages:
                for message in messages:
                    notification = json.loads(message['Body'])
                    rekMessage = json.loads(notification['Message'])
                    print(rekMessage['JobId'])
                    if rekMessage['JobId'] == self.startJobId:
                        status = rekMessage['status']
                        print(status)
                        print('Matching Job Found:' + rekMessage['JobId'])
                        job_done = True
                        print(notification)
                        message.delete()
                        print(notification)

        return status

    def StartLabelDetection(self):
        response = self.rek.start_label_detection(Video={'S3Object': {'Bucket': self.bucket, 'Name': self.video}},
                                                  NotificationChannel={'RoleArn': self.role.arn,
                                                                       'SNSTopicArn': self.topic.arn},
                                                  MinConfidence=90,
                                                  )

        self.startJobId = response['JobId']
        print('Start Job Id: ' + self.startJobId)

    def GetLabelDetectionResults(self):
        maxResults = 10
        paginationToken = ''
        finished = False

        while not finished:
            response = self.rek.get_label_detection(JobId=self.startJobId,
                                                    MaxResults=maxResults,
                                                    NextToken=paginationToken,
                                                    SortBy='TIMESTAMP',
                                                    AggregateBy="TIMESTAMPS")

            print('Codec: ' + response['VideoMetadata']['Codec'])
            print('Duration: ' + str(response['VideoMetadata']['DurationMillis']))
            print('Format: ' + response['VideoMetadata']['Format'])
            print('Frame rate: ' + str(response['VideoMetadata']['FrameRate']))
            print()

            for labelDetection in response['Labels']:
                label = labelDetection['Label']

                print("Timestamp: " + str(labelDetection['Timestamp']))
                print("   Label: " + label['Name'])
                print("   Confidence: " + str(label['Confidence']))
                print("   Instances:")
                for instance in label['Instances']:
                    print("      Confidence: " + str(instance['Confidence']))
                    print("      Bounding box")
                    print("        Top: " + str(instance['BoundingBox']['Top']))
                    print("        Left: " + str(instance['BoundingBox']['Left']))
                    print("        Width: " + str(instance['BoundingBox']['Width']))
                    print("        Height: " + str(instance['BoundingBox']['Height']))
                    print()
                print()

                print("Parents:")
                for parent in label['Parents']:
                    print("   " + parent['Name'])

                print("Aliases:")
                for alias in label['Aliases']:
                    print("   " + alias['Name'])

                print("Categories:")
                for category in label['Categories']:
                    print("   " + category['Name'])
                print("----------")
                print()

                if 'NextToken' in response:
                    paginationToken = response['NextToken']
                else:
                    finished = True

    def CreateTopicandQueue(self):
        millis = str(int(round(time.time() * 1000)))

        # Create SNS topic
        resource_name = "AmazonRekognition-CV" + millis
        self.topic = self.sns.create_topic(Name=resource_name)

        # create SQS queue
        self.queue = self.sqs.create_queue(
            QueueName=resource_name, Attributes={"ReceiveMessageWaitTimeSeconds": "5"}
        )
        queue_arn = self.queue.attributes["QueueArn"]
        policy = f"""{{
          "Version":"2012-10-17",
          "Statement":[
            {{
              "Sid":"MyPolicy",
              "Effect":"Allow",
              "Principal" : {{"AWS" : "*"}},
              "Action":"SQS:SendMessage",
              "Resource": "{queue_arn}",
              "Condition":{{
                "ArnEquals":{{
                  "aws:SourceArn": "{self.topic.arn}"
                }}
              }}
            }}
          ]
        }}"""
        self.queue.set_attributes(
            Attributes={
                "Policy": policy
            }
        )
        self.topic.subscribe(Protocol="sqs", Endpoint=queue_arn)

        # This role lets Amazon Rekognition publish to the topic. Its Amazon Resource
        # Name (ARN) is sent each time a job is started.
        self.role = self.iam.create_role(
            RoleName=resource_name,
            AssumeRolePolicyDocument=json.dumps(
                {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Principal": {"Service": "rekognition.amazonaws.com"},
                            "Action": "sts:AssumeRole",
                        }
                    ],
                }
            ),
        )
        policy = self.iam.create_policy(
            PolicyName=resource_name,
            PolicyDocument=json.dumps({
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Action": "sns:Publish",
                        "Resource": self.topic.arn
                    }
                ]
            })
        )

        self.role.attach_policy(PolicyArn=policy.arn)


    def DeleteTopicandQueue(self):
        self.sqs.delete_queue(QueueUrl=self.sqsQueueUrl)
        self.sns.delete_topic(TopicArn=self.snsTopicArn)




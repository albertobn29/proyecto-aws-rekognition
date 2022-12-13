import aws.session as session
import os
from dotenv import load_dotenv
load_dotenv()

origen = os.environ.get('BUCKET_SOURCE')
destino = os.environ.get('BUCKET_DEST')

rekog = session.Aws().session.client('rekognition')


def detect_faces(img_name):
    response = rekog.detect_faces(
        Image={
            'S3Object': {
                'Bucket': origen,
                'Name': img_name,
            }
        },
        Attributes=['DEFAULT']
    )
    print(response)

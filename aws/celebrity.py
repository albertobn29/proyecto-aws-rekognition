import aws.session as session
import os
from dotenv import load_dotenv
load_dotenv()

origen = os.environ.get('BUCKET_SOURCE')
destino = os.environ.get('BUCKET_DEST')

rekog = session.Aws().session.client('rekognition')


def celebrity(img_name):
    response = rekog.recognize_celebrities(
        Image={
            'S3Object': {
                'Bucket': destino,
                'Name': img_name,
            }
        }
    )
    # print(response)
    if len(response['CelebrityFaces']) < 0:
        response['CelebrityFaces']['Name'] = 'ninguno'
    return response['CelebrityFaces'][0]

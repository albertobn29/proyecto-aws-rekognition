import aws.session as session
import os
from PIL import Image
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
    for i in range(len(response['FaceDetails'])):
        recortar(img_name, response['FaceDetails'][i]['BoundingBox'], i)
#     Recortar imagen
#     https://www.geeksforgeeks.org/python-pil-image-crop-method/


def recortar(img_name, box, num):
    im = Image.open('static/img/'+img_name)

    width_total, height_total = im.size

    left = int(width_total * box['Left'])-60
    top = int(height_total * box['Top'])-90
    width = int(width_total * box['Width'])
    height = int(height_total * box['Height'])
    right = left+width+120
    bottom = top+height+180

    # The right can also be represented as (left+width)
    # and lower can be represented as (upper+height).
    im1 = im.crop((left, top, right, bottom))
    im1.save(f'static/img/test/{num}_{img_name}')

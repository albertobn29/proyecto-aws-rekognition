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
    # print(response)
    img_name_noext = os.path.splitext(img_name)[0]
    os.mkdir(f'static/img/{img_name_noext}/')

    images = []
    for i in range(len(response['FaceDetails'])):
        img = recortar(img_name, response['FaceDetails'][i]['BoundingBox'], i, img_name_noext)
        images.append(img)

    return images
#     Recortar imagen
#     https://www.geeksforgeeks.org/python-pil-image-crop-method/


def recortar(img_name, box, num, img_dir):
    im = Image.open('static/img/'+img_name)

    width_total, height_total = im.size

    # TODO: Controlar que no se pasen del total de la imagen
    width = int(width_total * box['Width'])
    height = int(height_total * box['Height'])

    left = int(width_total * box['Left'])-60
    top = int(height_total * box['Top'])-90
    right = left+width+120
    bottom = top+height+180

    # The right can also be represented as (left+width)
    # and lower can be represented as (upper+height).
    im1 = im.crop((left, top, right, bottom))
    im1.save(f'static/img/{img_dir}/{num}_{img_name}')
    return f'{img_dir}/{num}_{img_name}'

import aws.bucket as s3
import aws.analysis as detect
import os
from dotenv import load_dotenv
load_dotenv()

origen = os.environ.get('BUCKET_SOURCE')
destino = os.environ.get('BUCKET_DEST')
carpeta_imgs = 'static/img/'


def main(img_name):
    s3.subirFileToBucket(origen, carpeta_imgs+img_name, img_name)
    s3.verElementBucket(origen)
    detect.detect_faces(img_name)


def checkBuckets():
    try:
        s3.crearBucket(os.environ.get('BUCKET_SOURCE'))
    except Exception as err:
        print(err)
        pass

    try:
        s3.crearBucket(os.environ.get('BUCKET_DEST'))
    except Exception as err:
        print(err)
        pass

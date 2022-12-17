import aws.bucket as s3
import aws.analysis as detect
import aws.celebrity as celeb
import os
from dotenv import load_dotenv
load_dotenv()

origen = os.environ.get('BUCKET_SOURCE')
destino = os.environ.get('BUCKET_DEST')
carpeta_imgs = 'static/img/'


def main(img_name):
    s3.subirFileToBucket(origen, carpeta_imgs+img_name, img_name)
    s3.verElementBucket(origen)
    imgs = detect.detect_faces(img_name)
    celebs_info = []
    for img in imgs:
        img_indv_name = img.split('/')[1]
        s3.subirFileToBucket(destino, carpeta_imgs+img, img_indv_name)
        celeb_info = celeb.celebrity(img_indv_name)
        info = {'img': img_indv_name, 'name': celeb_info['Name']}
        celebs_info.append(info)

    data = {'img_principal': img_name,
            'carpeta_imgs': os.path.splitext(img_name)[0],
            'celebs_info': celebs_info}
    return data


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

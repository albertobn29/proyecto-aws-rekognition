import aws.session as session


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


s3 = session.Aws().session.resource('s3')
buckets_name = []


def listBuckets():
    # print(f'\n{bcolors.HEADER}Lista:{bcolors.ENDC}')
    buckets = s3.buckets.all()
    for bucket in buckets:
        buckets_name.append(bucket.name)
        # print(f'\t{bucket.name}')


def verElementBucket(bucket_name: str):
    cont = 0
    print(f'\n{bcolors.HEADER}Elementos del bucket {bucket_name}:{bcolors.ENDC}')
    bucket = s3.Bucket(bucket_name)
    for obj in bucket.objects.all():
        cont += 1
        print(f'\t{obj.key}')
    print(f'\tHay un total de {bcolors.OKCYAN}{cont}{bcolors.ENDC} archivos dentro de {bucket_name}')


def crearBucket(bucket_name: str):
    listBuckets()
    if bucket_name not in buckets_name:
        print(f'\n{bcolors.HEADER}Crear Bucket {bucket_name}{bcolors.ENDC}')
        bucket = s3.Bucket(bucket_name)
        bucket.create()
    else:
        raise Exception(f'{bcolors.FAIL}El bucket ya existe{bcolors.ENDC}')


def eliminarBucket(bucket_name: str):
    print(f'\n{bcolors.HEADER}Bucket {bucket_name} BORRADO{bcolors.ENDC}')
    bucket = s3.Bucket(bucket_name)
    bucket.objects.delete()
    bucket.delete()


def subirFileToBucket(bucket: str, ruta: str, name_file: str):
    bucket = s3.Bucket(bucket)
    print(f'\n{bcolors.OKBLUE}Uploading {name_file}...{bcolors.ENDC}')
    bucket.upload_file(ruta, name_file)
    print(f'{bcolors.OKGREEN}Uploaded complete.{bcolors.ENDC}')


def downloadFile(bucket: str, ruta: str, name_file: str):
    bucket = s3.Bucket(bucket)
    print(f'\n{bcolors.OKBLUE}Downloading {name_file} to {ruta}...{bcolors.ENDC}')
    bucket.download_file(name_file, ruta)
    print(f'{bcolors.OKGREEN}Downloading complete.{bcolors.ENDC}')


def deleteFile(bucket: str, file: str):
    bucket = s3.Bucket(bucket)
    obj = bucket.Object(file)
    obj.delete()
    print(f'\n{bcolors.OKGREEN}Archivo: {file} BORRADO{bcolors.ENDC}')

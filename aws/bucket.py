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
    buckets = s3.buckets.all()
    for bucket in buckets:
        buckets_name.append(bucket.name)


def crearBucket(bucket_name: str):
    listBuckets()
    if bucket_name not in buckets_name:
        print(f'\n{bcolors.HEADER}Crear Bucket {bucket_name}{bcolors.ENDC}')
        bucket = s3.Bucket(bucket_name)
        bucket.create()
    else:
        raise Exception(f'{bcolors.FAIL}El bucket ya existe{bcolors.ENDC}')


def subirFileToBucket(bucket: str, ruta: str, name_file: str):
    bucket = s3.Bucket(bucket)
    print(f'\n{bcolors.OKBLUE}Uploading {name_file}...{bcolors.ENDC}')
    bucket.upload_file(ruta, name_file)
    print(f'{bcolors.OKGREEN}Uploaded complete.{bcolors.ENDC}')

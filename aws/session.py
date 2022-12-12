import boto3
import os
from dotenv import load_dotenv
load_dotenv()

accessKeyId = os.environ.get('ACCESS_KEY_ID')
secretKey = os.environ.get('SECRET_ACCESS_KEY')


class Aws:
    __instance = None
    __inited = False

    def __new__(cls) -> 'Aws':
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self) -> None:
        if type(self).__inited:
            return
        type(self).__inited = True
        self.session = boto3.Session(aws_access_key_id=accessKeyId, aws_secret_access_key=secretKey)

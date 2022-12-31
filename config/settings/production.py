from .base import *

DEBUG = True

ALLOWED_HOSTS = ["tiphub.net", "www.tiphub.net"]
CSRF_TRUSTED_ORIGINS = ['https://*.tiphub.net']


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'damoondbpyv_db',
#         'USER': 'postgres',
#         'PASSWORD': 'rl3dc6wgrhhcq9a',
#         'HOST': 'damoondb-fwd-service',
#         'PORT': 5432
#     }
# }
#
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tiphubne_tiphub',
        'USER': 'tiphubne_mahdi',
        'PASSWORD': 'Mm3381156004',
        'HOST': 'host',
        'PORT': 3306
    }
}

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_ACCESS_KEY_ID = 'daf9c1f9-3ecf-4619-8d28-265bd356f6bd'
AWS_SECRET_ACCESS_KEY = '79dd5596140bc0564f1ea66bb541dfd00a9b582fe53485355a24b89201cf1eae'
AWS_STORAGE_BUCKET_NAME = 'tiphubnet'
AWS_SERVICE_NAME = 's3'
AWS_S3_ENDPOINT_URL = 'https://s3.ir-thr-at1.arvanstorage.ir'
AWS_S3_FILE_OVERWRITE = False

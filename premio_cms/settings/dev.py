from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'mi2mtv$#t(ysjhfsb)+9crm=8tjq*0nwef1)zy4*e!1%zrndg('

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*'] 

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


try:
    from .local import *
except ImportError:
    pass

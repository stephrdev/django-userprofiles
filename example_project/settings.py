import os

PROJECT_ROOT = os.path.dirname(__file__)

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'local_database.db',
        'TEST_NAME': ':memory:',
    }
}

SITE_ID = 1

SECRET_KEY = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

ROOT_URLCONF = 'example_project.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'userprofiles',
    #'userprofiles.contrib.accountverification',
    #'userprofiles.contrib.emailverification',
    #'userprofiles.contrib.profiles',
    #'accounts',
)

EMAIL_HOST = 'localhost'
EMAIL_PORT = '2525'

#AUTH_PROFILE_MODULE = 'accounts.Profile'

#USERPROFILES_CHECK_UNIQUE_EMAIL = True
#USERPROFILES_DOUBLE_CHECK_EMAIL = True
#USERPROFILES_DOUBLE_CHECK_PASSWORD = True
#USERPROFILES_REGISTRATION_FULLNAME = True
#USERPROFILES_USE_ACCOUNT_VERIFICATION = True
#USERPROFILES_REGISTRATION_FORM = 'accounts.forms.ProfileRegistrationForm'
#USERPROFILES_USE_PROFILE = True
#USERPROFILES_PROFILE_ALLOW_EMAIL_CHANGE = True
#USERPROFILES_INLINE_PROFILE_ADMIN = True

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
    'templates',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'userprofiles',
    'accounts',
)

EMAIL_HOST = 'localhost'
EMAIL_PORT = '2525'

AUTH_PROFILE_MODULE = 'accounts.Profile'

USERPROFILES_CHECK_UNIQUE_EMAIL = True
USERPROFILES_DOUBLE_CHECK_EMAIL = False
USERPROFILES_DOUBLE_CHECK_PASSWORD = True
USERPROFILES_REGISTRATION_FULLNAME = True
USERPROFILES_USE_ACCOUNT_VERIFICATION = False
USERPROFILES_USE_PROFILE = True
USERPROFILES_INLINE_PROFILE_ADMIN = True
USERPROFILES_USE_PROFILE_VIEW = True
USERPROFILES_REGISTRATION_FORM = 'accounts.forms.ProfileRegistrationForm'


import os

TEST_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),
    '..', 'userprofiles', 'tests'))

TEST_RUNNER = 'discover_runner.DiscoverRunner'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'userprofiles',
    'test_project.test_accounts',
]

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates'),
)

ROOT_URLCONF = 'test_project.urls'

SECRET_KEY = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

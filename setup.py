import codecs, os
from setuptools import setup, find_packages

def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='django-userprofiles',
    version='0.2',
    description='Registration, e-mail verifications and profiles.',
    long_description=read('README.rst'),
    author='Stephan Jaekel',
    author_email='steph@rdev.info',
    url='https://github.com/stephrdev/django-userprofiles/',
    packages=find_packages(exclude=['example_project', 'example_project.*']),
    package_data = {
        'userprofiles': ['templates/userprofiles/*.html', 'templates/userprofiles/*/*.html',
            'locale/de/LC_MESSAGES/*'],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    zip_safe=False,
)

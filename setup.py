from setuptools import setup, find_packages
 
setup(
    name='django-userprofiles',
    version='0.1',
    description='Profiles and Registration',
    author='Stephan Jaekel',
    author_email='steph@rdev.info',
    url='',
    packages=find_packages(),
    package_data = {
        'userprofiles': ['templates/*/*.html'],
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

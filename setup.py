from setuptools import setup, find_packages
import os

version = __import__('image_filer').__version__

def read(fname):
    # read the contents of a text file
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "django-image-filer",
    version = version,
    url = 'http://github.com/stefanfoulis/django-image-filer',
    license = 'BSD',
    platforms=['OS Independent'],
    description = "A file management application for django that makes handling of images a breeze.",
    long_description = read('README'),
    author = 'Stefan Foulis',
    author_email = 'stefan.foulis@gmail.com',
    packages=find_packages(exclude=['ez_setup']),
    install_requires = [
        'sorl-thumbnail>=3.2.5',
        'django>=1.1',
    ],
    package_data={
        '': ['*.txt', '*.rst',],
        'image_filer': [
            'media/*/css/*.css',
            'media/*/flash/*.swf',
            'media/*/icons/*.png',
            'media/*/img/*',
            'media/*/js/*',
            'media/*/slideshow2/*/*',
            'templates/*/*.html',
            'templates/*/*/*.html',
            'templates/*/*/*/*.html',
        ],
    },
    zip_safe=False,
    classifiers = [
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
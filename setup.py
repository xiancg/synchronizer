from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='synchronizer',
    version='2.0.0',
    description='A collection of utilities for CGI-VFX to copy files '
                'from one place to another, find out basic stat differences '
                'between them and handle file sequences and textures (tx files).',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/xiancg/synchronizer',
    author='Chris Granados - Xian',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.7'
    ],
    packages=find_packages(where='.'),
    python_requires='>=2.7, >=3.7',
    extras_require={
        'dev': ['pytest', 'pytest-cov', 'pytest-datafiles', 'flake8'],
        'docs': ['sphinx', 'sphinx-rtd-theme']
    }
)

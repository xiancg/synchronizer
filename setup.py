from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

version_str = '2.0.1'

setup(
    name='synchronizer',
    version=version_str,
    description='A collection of utilities for CGI-VFX to copy files '
                'from one place to another, find out basic stat differences '
                'between them and handle file sequences and textures (tx files).',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/xiancg/synchronizer',
    download_url='https://github.com/xiancg/synchronizer/archive/v{}.tar.gz'.format(version_str),
    author='Chris Granados - Xian',
    author_email='info@chrisgranados.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.7'
    ],
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4',
    install_requires=['six'],
    extras_require={
        'dev': ['pytest', 'pytest-cov', 'pytest-datafiles', 'python-coveralls', 'flake8'],
        'docs': ['sphinx', 'sphinx-rtd-theme']
    },
    package_data={'': ['cfg/config.json']}
)

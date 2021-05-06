import io
import re

from setuptools import setup


with io.open('README.md', 'rt', encoding='utf8') as f:
    readme = f.read()

with io.open('api/__init__.py', 'rt', encoding='utf8') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)

setup(
    name='api',
    version=version,
    author='Alex Brady',
    author_email='alex.brady.py@gmail.com',
    description='Data importer and organiser for User Tests',
    long_description=readme,
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        ],
    install_requires=[
        'flask==1.1.2',
        'flask-io==1.14.2',
        'marshmallow==2.21.0',
        'sqlalchemy==1.4.12',
        'Flask-SQLAlchemy==2.5.1',
        'requests==2.24.0',
        'flask-marshmallow==0.14.0',
        'python-magic==0.4.18'
        ],
    zip_safe=False,
    platforms='any',
    )

import os
from setuptools import setup
import codecs


def open_local(paths, mode='r', encoding='utf8'):
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        *paths
    )
    return codecs.open(path, mode, encoding)


with open_local(['README.rst']) as readme:
    long_description = readme.read()

with open_local(['requirements.txt']) as req:
    install_requires = req.read().split("\n")

version = '0.2'

setup(
    name='connegp',
    packages=['connegp'],
    version=version,
    description='This small library module assists with tasks related to Content Negotiation by Profile',
    author='Nicholas Car',
    author_email='nicholas.car@surroundaustralia.com',
    url='https://github.com/nicholascar/connegp',
    download_url='https://github.com/nicholascar/connegp/archive/v{:s}.tar.gz'.format(version),
    license='LICENSE',
    keywords=['Content Negotiation', 'HTTP', 'Linked Data', 'Semantic Web', 'Python', 'API', 'RDF'],
    long_description=long_description,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Utilities',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    project_urls={
        'Bug Reports': 'https://github.com/nicholascar/connegp/issues',
        'Source': 'https://github.com/nicholascar/connegp',
    },
    install_requires=install_requires,
    setup_requires=['wheel', 'twine']
)


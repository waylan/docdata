#!/usr/bin/env python

from setuptools import setup
from docdata import __version__ as ver

setup(
    name='docdata',
    description='A better Meta-Data handler for lightweight markup languages.',
    author='Waylan Limberg',
    author_email='waylan.limberg@icloud.com',
    version=ver,
    url='https://github.com/waylan/docdata',
    packages=['docdata'],
    install_requires = ['pyyaml'],
    license='BSD'
)

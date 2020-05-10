# -*- mode: python; python-indent-offset: 4; indent-tabs-mode: nil -*-
# SPDX-License-Indentifier: MPL-2.0

"""A setuptools based setup module."""

from codecs import open
from os import path
from setuptools import setup, find_packages


here = path.abspath(path.dirname(__file__))

# Get the long description from the README file.
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

requirements = [
    'sense_hat==2.2.0'
]
URL = 'https://github.com/rzr/sense-hat-webthing'

setup(
    name='sense-hat-webthing',
    version='0.0.6',
    description='Sense Hat WebThing',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=URL,
    author='Philippe Coval',
    author_email='rzr@users.sf.net',
    keywords='sensehat sense-hat RaspberryPi mozilla iot web thing webthing',
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Programming Language :: Python :: 3.7',
    ],
    license='MPL-2.0',
    project_urls={
        'Source': URL,
        'Tracker': URL + '/issues',
    },
    python_requires='>=3.7se, <4',
)

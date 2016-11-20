#!/usr/bin/env python

import os
from setuptools import setup, find_packages

import pip.download
from pip.req import parse_requirements


reqs_txt = os.path.join(os.path.dirname(__file__), 'requirements.txt')
pip_reqs = parse_requirements(reqs_txt, session=pip.download.PipSession())
pip_reqs = [str(obj.req) for obj in pip_reqs]

setup(
    name = 'skeleton',
    version = '0.2.0',
    description = (
        'Declaratively built schema transformation',
    ),
    author = 'Matt Dennewitz',
    author_email = 'mattdennewitz@gmail.com',
    url = 'https://github.com/mattdennewitz/skeleton',

    install_requires = pip_reqs,
    include_package_data=True,
    packages = find_packages(),
)

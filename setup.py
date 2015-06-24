#!/usr/bin/env python
"""
It is a convention among django developers to place a requirements.txt
in the root of their projects and to run the pip command to install it.
Openshift python cartridge allows for install of the requirements in two
ways.

The first method is via the requirements.txt file. Anything placed there
will get automatically installed on the openshift application virtualenv.

In addition to this, openshift mandates the use of this setup.py to install
the django-project. The install_requires setup option will in addition,
install any other packages which are needed by the application.

With this double approach, it made the most sense to employ the both for
a different purpose.

The setup.py install_requires reads from the django-project 'BASE_DIR'
and imports the requirements from the requirements.txt there.
"""

from setuptools import setup, find_packages
import os

OPENSHIFT_REPO_DIR = os.environ.get('OPENSHIFT_REPO_DIR', os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(OPENSHIFT_REPO_DIR, 'wsgi/webconfgen/requirements.txt')) as requirements:
    PACKAGES = requirements.readlines()

setup(
    name='webconfgen',
    version='0.1.1',
    description='A web based ntp.conf generator',
    author='Parth Laxmikant Kolekar',
    author_email='parth.kolekar@students.iiit.ac.in',
    url='http://github.com/nwtime/webconfgen',
    install_requires=PACKAGES,
    packages=find_packages(),
    include_package_data=True,
)

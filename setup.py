#!/usr/bin/env python

from setuptools import setup, find_packages
import os

OPENSHIFT_REPO_DIR = os.environ.get('OPENSHIFT_REPO_DIR', os.path.dirname(os.path.abspath(__file__)))

with open (os.path.join(OPENSHIFT_REPO_DIR, 'requirements.txt')) as requirements:
    PACKAGES = requirements.readlines()

setup(
    # GETTING-STARTED: set your app name:
    name='webconfgen',
    # GETTING-STARTED: set your app version:
    version='0.1.0',
    # GETTING-STARTED: set your app description:
    description='A web based ntp.conf generator',
    # GETTING-STARTED: set author name (your name):
    author='Parth Laxmikant Kolekar',
    # GETTING-STARTED: set author email (your email):
    author_email='parth.kolekar@students.iiit.ac.in',
    # GETTING-STARTED: set author url (your url):
    url='http://github.com/nwtime/webconfgen',
    # GETTING-STARTED: define required django version:
    install_requires=PACKAGES,
)

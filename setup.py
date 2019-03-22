#!/usr/bin/env python3

from setuptools import setup
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='papero',
    version='0.2.6',
    packages=['papero'],
    author='kydos',
    description="Python's Apero",
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    url='https://github.com/atolab/papero',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Development Status :: 3 - Alpha",
        "Topic :: System :: Networking",
        'License :: OSI Approved :: Apache Software License',
        'License :: OSI Approved :: Eclipse Public License 2.0 (EPL-2.0)',
        "Operating System :: OS Independent"]
)

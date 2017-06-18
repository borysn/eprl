#!/bin/env python3
#
# setup.py
# author: borysn
# license: MIT
from setuptools import setup, find_packages
from codecs import open
from os import path

# get current directory
cwd = path.abspath(path.dirname(__file__))

# get long description
def getLongDesc():
    return open(path.join(cwd, 'README.rst'), encoding='utf-8').read()

# getVersion()
# get current eprl script version
def getVersion():
    return __import__('eprl').util.getEprlVersion()

# setup eprl
setup(
    name='eprl',
    description='edit portage resume list',
    long_description=getLongDesc(),
    version='{}'.format(getVersion()),
    author='borysn',
    author_email='xborysn@gmail.com',
    url='https://github.com/borysn/eprl',
    keywords='python3 script gentoo linux edit portage resume list',
    packages = ['eprl'],
    entry_points = {'console_scripts': ['eprl=eprl.cli:main']},
    install_requires=[],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Topic :: Database',
        'Topic :: System :: Software Distribution',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities'
    ],
    license='MIT'
)

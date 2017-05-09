# setup.py
# author: borysn
# license: MIT
from distutils.core import setup

setup(
    name='eprl',
    description='edit portage resume list',
    long_description=open('README.txt').read(),
    version='0.2',
    author='borysn',
    author_email='xborysn@gmail.com',
    url='https://github.com/borysn/eprl',
    keywords=['python3', 'script', 'portage', 'gentoo', 'linux'],
    platforms=[],
    packages=['eprl'],
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
    include_package_data=True,
    license='MIT'
)

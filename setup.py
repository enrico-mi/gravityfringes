# -*- coding: utf-8 -*-

# Learn more where I took it from: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='gravityfringes',
    version='0.1.0',
    description='Package to read fringes in real time from webcam',
    long_description=readme,
    license=license,
    author='Enrico Milanese',
    author_email='milanese.e@gmail.com',
    url='https://github.com/enrico-mi/gravityfringes.git',
    packages=find_packages(exclude=('test', 'docs'))
)

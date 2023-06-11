# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='Mitsuko',
    version='0.5.0',
    description='RSS feed aggregator',
    long_description=readme,
    author='Julien Poirou',
    author_email='julienpoirou@protonmail.com',
    url='https://github.com/julienpoirou/aggregator-rss',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

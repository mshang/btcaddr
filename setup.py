#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='btcaddr',
    version='1.0',
    description="Generate bitcoin addresses.",
    author="Miles Shang",
    author_email='mail@mshang.ca',
    url='https://github.com/mshang/btcaddr',
    scripts=['btcaddr'],
    license='LICENSE',
)

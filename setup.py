#!/usr/bin/env python
# Copyright (C) 2014 Steve Milner
"""
Build script.
"""

import os.path

from setuptools import setup, find_packages


setup(
    name='flagon',
    version='0.0.3',
    author='Steve Milner',
    url='https://github.com/ashcrow/flagon',
    license='MIT',
    zip_safe=False,
    package_dir={
        'flagon': os.path.join('src', 'flagon')
    },
    packages=find_packages('src'),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
    ],

)

#!/usr/bin/env python
from setuptools import setup


setup(
    name='advanced-advanced-sqlalchemy-manager',
    version='0.1.0',
    description='Manager for SQLAlchemy',
    long_description=open('README.md').read(),
    author='Flowelcat',
    author_email='flowelcat@gmail.com',
    url='https://github.com/Flowelcat/advanced-sqlalchemy-manager',
    install_requires=['sqlalchemy'],
    py_modules=['alchmanager'],
    zip_safe=False,
    test_suite='tests',
    classifiers=(
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    )
)

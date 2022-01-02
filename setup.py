from setuptools import setup, find_packages
import codecs
import os.path


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


setup(
    name='advanced-sqlalchemy-manager',
    version=get_version("alchmanager/__init__.py"),
    description='Advanced query manager for SQLAlchemy',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    keywords='sqlalchemy, alchmanager, query_manager, query',
    author='Flowelcat',
    author_email='flowelcat@gmail.com',
    url='https://github.com/Flowelcat/advanced-sqlalchemy-manager',
    license="GNUv3",
    license_files=('LICENSE.txt',),
    install_requires=['sqlalchemy'],
    packages=find_packages(include=['alchmanager', 'alchmanager.*']),
    include_package_data=True,
    test_suite='tests',
    python_requires=">=3.5",
    classifiers=(
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    )
)

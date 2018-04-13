from __future__ import unicode_literals

import os

from setuptools import setup

basedir = os.path.dirname(__file__)


def readme():
    with open(os.path.join(basedir, 'README.rst')) as f:
        return f.read()


about = {}
with open(os.path.join(basedir, 'flake8_aaa', '__about__.py')) as f:
    exec(f.read(), about)

setup(
    # --- META ---
    name=about['__name__'],
    version=about['__version__'],
    description=about['__description__'],
    license='MIT',
    long_description=readme(),

    # --- Python ---
    packages=['flake8_aaa'],
    py_modules=['flake8_aaa'],
    install_requires=[
        'astroid >= 1.6',
        'asttokens >= 1.1.10',
        'flake8 >= 3',
    ],
    entry_points={
        'flake8.extension': [
            'AAA = flake8_aaa:Checker',
        ],
    },
)

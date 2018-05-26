from __future__ import unicode_literals

import os

from setuptools import setup

basedir = os.path.dirname(__file__)


def readme():
    with open(os.path.join(basedir, 'README.rst')) as f:
        return f.read()


about = {}
with open(os.path.join(basedir, 'flake8_aaa', '__about__.py')) as f:
    exec(f.read(), about)  # yapf: disable

setup(
    # --- META ---
    name=about['__name__'],
    version=about['__version__'],
    description=about['__description__'],
    license='MIT',
    long_description=readme(),
    author='James Cooke',
    author_email='github@jamescooke.info',
    url='https://github.com/jamescooke/flake8-aaa',

    # --- Python ---
    packages=['flake8_aaa'],
    py_modules=['flake8_aaa'],
    install_requires=[
        'asttokens >= 1.1.10',
        'flake8 >= 3',
    ],
    entry_points={
        'flake8.extension': [
            'AAA = flake8_aaa:Checker',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Flake8',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python',
    ],
    zip_safe=False,
)

from __future__ import unicode_literals

import setuptools


setuptools.setup(
    name='flake8-aaa',
    install_requires=[
        'flake8 > 3',
    ],
    license='MIT',
    py_modules=[
        'flake8_aaa',
    ],
    entry_points={
        'flake8.extension': [
            'AAA = flake8_aaa:Checker',
        ],
    },
)

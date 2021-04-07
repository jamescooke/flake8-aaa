import os

from setuptools import find_packages, setup

basedir = os.path.dirname(__file__)


def readme():
    with open(os.path.join(basedir, 'README.rst')) as f:
        return f.read()


about = {}
with open(os.path.join(basedir, 'src', 'flake8_aaa', '__about__.py')) as f:
    exec(f.read(), about)  # yapf: disable

setup(
    # --- META ---
    name=about['__iam__'],
    version=about['__version__'],
    description=about['__description__'],
    license='MIT',
    long_description=readme(),
    author='James Cooke',
    author_email='github@jamescooke.info',
    url='https://github.com/jamescooke/flake8-aaa',

    # --- Python ---
    packages=find_packages('src'),
    package_dir={'': 'src'},
    python_requires='>=3.6, <4',
    install_requires=[
        'asttokens >= 2',
    ],
    entry_points={
        'flake8.extension': [
            'AAA = flake8_aaa:Checker',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Flake8',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python',
    ],
    zip_safe=False,
)

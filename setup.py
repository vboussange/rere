# setup.py
from setuptools import find_packages, setup

setup(
    name='src',
    version='0.1',
    install_requires=[
        'gitpython',
        'numpy',
        'pandas',
        'requests',
        'pytest',
    ],
    python_requires='>=3.7',
    packages=find_packages(),
)

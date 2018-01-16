import sys
import os

from setuptools import setup, find_packages
sys.path.append(os.getcwd())


setup(
    package_dir={'': '.'},
    packages=['salic_api'],
)

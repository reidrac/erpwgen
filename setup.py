#!/usr/bin/env python

from setuptools import setup
from erpwgen import __version__, __description__, __author__, \
                   __author_email__, __license__, __url__

def readme():
    try:
        return open("README.rst").read()
    except:
        return ""

setup(name="erpwgen",
      version=__version__,
      description=__description__,
      long_description=readme(),
      author=__author__,
      author_email=__author_email__,
      url=__url__,
      license=__license__,
      scripts=["erpegen.py"],
      classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Programming Language :: Python",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        ],
      keywords="password generator",
      )

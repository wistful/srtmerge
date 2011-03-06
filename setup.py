#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from setuptools import setup, find_packages

if sys.version_info[:2] < (2, 5):
    raise Exception('This version of srtmerge needs Python 2.5 or later. ')

README = ''
try:
    f = open('README')
    README = f.read()
    f.close()
except:
    pass

setup(name='srtmerge',
      version='0.1',
      author='wistful',
      author_email='wst.public.mail@gmail.com',
      packages=find_packages(),
      description = "srtmerge (.srt) used to merge two Srt files",
      long_description = README,
      url="https://github.com/wistful/srtmerge",
      license = "LGPL",
      platforms = ["Unix,"],
      keywords = "srtmerge srt",
      test_suite='tests',
      classifiers = [
          "Development Status :: 4 - Beta",
          "Environment :: Console",
          "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
          "Operating System :: POSIX :: Linux",
          "Programming Language :: Python :: 2",
          "Topic :: Text Processing",
          "Topic :: Utilities"
      ],
      )

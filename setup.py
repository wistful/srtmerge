#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Setup script to install package."""

import sys
import os

from setuptools import setup, find_packages
from srtmerge import __version__, __author__

if sys.argv[-1] in ('submit', 'publish'):
    os.system('python setup.py bdist_egg sdist --format=zip upload')
    sys.exit()

README = """srtmerge is a Python library used to merge two Srt files.

Usage
=====

::

    from srtmerge import srtmerge
    srtmerge([filepath1, filepath2, ...], out_filepath, offset=1000)

srtmerge filepath1 filepath2 out_filepath offset=1000
"""

requires = ['chardet']

setup(name='srtmerge',
      version=__version__,
      author=__author__,
      author_email='wst.public.mail@gmail.com',
      packages=find_packages(
          exclude=['*.tests', '*.tests.*', 'tests.*', 'tests']),
      description='srtmerge (.srt) used to merge two Srt files',
      long_description=README,
      url='https://github.com/wistful/srtmerge',
      license='LGPL',
      install_requires=requires,
      platforms=['Unix,'],
      keywords='srtmerge, srt, subtitle',
      test_suite='tests',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',  # noqa: E501 pylint: disable=line-too-long
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python :: 3',
          'Topic :: Text Processing',
          'Topic :: Utilities'
      ],
      entry_points={
          'console_scripts': [
              'srtmerge = srtmerge.cli:main'
          ]},
      )

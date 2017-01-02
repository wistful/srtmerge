#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Setup script to install package."""

import sys
import os

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand
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


# http://doc.pytest.org/en/latest/goodpractices.html#manual-integration
class PyTest(TestCommand):
    """Runner for the pytest."""

    user_options = [('pytest-args=', 'a', "Arguments to pass to pytest")]

    def initialize_options(self):
        super(PyTest, self).initialize_options()
        # TestCommand.initialize_options(self)
        self.pytest_args = ''

    def run_tests(self):
        import shlex
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)


requires = ['chardet', 'click']

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
      setup_requires=['pytest-cov'],
      platforms=['Unix,'],
      keywords='srtmerge, srt, subtitle',
      test_suite='tests',
      tests_require=['pytest', 'pytest-cov'],
      cmdclass={'test': PyTest},
      extras_require={
          'lint': [
              'flake8',
              'pylint',
              'pytest',
          ],
      },
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

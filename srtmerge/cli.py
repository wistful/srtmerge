#! /usr/bin/env python
# -*- coding: utf-8 -*-
#    Copyleft 2014 wistful <wst public mail at gmail com>
#
#    This is a free software; you can redistribute it and/or
#    modify it under the terms of the GNU Lesser General Public
#    License as published by the Free Software Foundation; either
#    version 2.1 of the License, or (at your option) any later version.
#
#    This library is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with this library; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

__author__ = 'wistful'
__version__ = '1.0'
__release_date__ = "15/01/2014"

import os
import sys

from .srt import srtmerge


def print_version():
    print("srtmerge: version %s (%s)" % (__version__, __release_date__))


def print_error(message):
    print("srtmerge error: {0}".format(message))


def _check_argv(args):
    """
    check command line arguments
    """
    inPaths = args['inPath']
    if len(inPaths) < 2:
        print_error("too few arguments")
        return False
    for path in inPaths:
        if not os.path.exists(path):
            print_error("file {srt_file} does not exist".format(srt_file=path))
            return False
    return True


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('inPath', type=str, nargs='+',
                        help='srt-files that should be merged')
    parser.add_argument('outPath', type=str,
                        help='output file path')
    parser.add_argument('--offset', action='store_const', const=0, default=0,
                        help='offset in msc (default: 0)')
    parser.add_argument('-d', '--disable-chardet', action='store_true',
                        dest='nochardet', default=False,
                        help='disable auto character encoding')
    parser.add_argument('--encoding', type=str, default='utf-8',
                        help='encoding for the output file (utf-8)')
    parser.add_argument('--version', action="store_true",
                        dest='version', help='print version')
    if '--version' in sys.argv:
        print_version()
        sys.exit(0)
    args = vars(parser.parse_args())
    if _check_argv(args):
        srtmerge(args.get('inPath'),
                 args.get('outPath'),
                 args.get('offset'),
                 not args.get('nochardet'),
                 args.get('encoding'))


if __name__ == '__main__':
    main()

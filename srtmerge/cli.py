#! /usr/bin/env python
# coding:utf-8

"""Command-line interface to merge two subtitle files."""

import os
import sys

from chardet.universaldetector import UniversalDetector

from srtmerge import reader
from srtmerge import srt
from srtmerge import writer

__author__ = 'wistful'
__version__ = '1.0'
__release_date__ = "15/01/2014"


def print_version():
    """Print current version to the stdout."""
    print("srtmerge: version %s (%s)" % (__version__, __release_date__))


def print_error(message):
    """Print error message to the stdout."""
    print("srtmerge error: {0}".format(message))


def _check_argv(args):
    """Check whether input parameters are correct or not."""
    paths = args['inPath']
    if len(paths) < 2:
        print_error("too few arguments")
        return False
    for path in paths:
        if not os.path.exists(path):
            print_error("file {srt_file} does not exist".format(srt_file=path))
            return False
    return True


def detect_encoding(file_path):
    """Return file encoding."""
    with open(file_path, 'rb') as f:
        u = UniversalDetector()
        for line in f:
            u.feed(line)
        u.close()
        return u.result['encoding']


def merge_subtitles(in_path1, in_path2, out_path, encoding):
    subs1 = reader.read(in_path1, detect_encoding(in_path1))
    subs2 = reader.read(in_path2, detect_encoding(in_path2))
    writer.write(out_path, srt.merge(subs1, subs2), encoding)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('inPath', type=str, nargs='+',
                        help='srt-files that should be merged')
    parser.add_argument('outPath', type=str,
                        help='output file path')
    parser.add_argument('--encoding', type=str, default='utf-8',
                        help='encoding for the output file (utf-8)')
    parser.add_argument('--version', action="store_true",
                        dest='version', help='print version')
    if '--version' in sys.argv:
        print_version()
        sys.exit(0)

    args = vars(parser.parse_args())
    if _check_argv(args):
        merge_subtitles(
            args.get('inPath')[0], args.get('inPath')[1],
            args.get('outPath'), args.get('encoding'))


if __name__ == '__main__':
    main()

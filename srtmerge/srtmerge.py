#! /usr/bin/env python
# -*- coding: utf-8 -*-
#    Copyleft 2011 wistful <wst public mail at gmail com>
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
__version__ = '0.6'
__release_date__ = "04/06/2013"

import os
import sys

from srt import subreader, subwriter, SubRecord


def print_version():
    print("srtmerge: version %s (%s)" % (__version__, __release_date__))


def srtmerge(in_srt_files, out_srt, offset=0):
    subs, result = [], []

    # join all srt-records into list
    for index, in_srt in enumerate(in_srt_files):
        for rec in subreader(in_srt):
            # index uses below to sort text by languages
            new_rec = SubRecord(rec.start, rec.finish, (index, rec.text))
            subs.append(new_rec)

    subs.sort()  # sort records by start time
    index = 0
    while index < len(subs) - 1:
        start, finish, rec_text = subs[index]
        text = [rec_text]
        for i in xrange(index + 1, len(subs)):
            sub_rec = subs[i]
            start2, finish2, rec_text2 = sub_rec
            if start2 < finish:
                finish = max(finish, start + (finish2 - start2) * 2 / 3)
                text.append(rec_text2)
            else:
                break
        index = i

        text = "".join(map(lambda item: item[1], sorted(text)))
        result.append(SubRecord(start + offset, finish + offset, text))

    subwriter(out_srt, result)


def _check_argv(args):
    """
    check command line arguments
    """
    for path in args.get('inPaths', []):
        if not os.path.exists(path):
            print("file {srt_file} does not exist".format(srt_file=path))
            return False
    return True


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('inPaths', type=str, nargs='+',
                        help='srt-files that must be merged')
    parser.add_argument('outPath', type=str,
                        help='output file')
    parser.add_argument('--offset', action='store_const', const=0, default=0,
                        help='offset in msc (default: 0)')
    parser.add_argument('--version', action="store_true",
                        dest='version', help='version')
    if '--version' in sys.argv:
        print_version()
        sys.exit(0)
    args = vars(parser.parse_args())
    if _check_argv(args):
        srtmerge(args.get('inPaths', []),
                 args.get('outPath'),
                 args.get('offset'))


if __name__ == '__main__':
    main()

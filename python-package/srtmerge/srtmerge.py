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

from srt import subreader, subwriter
import sys


def srtmerge(in_srt1, in_srt2, out_srt, diff=0):
    subs = [(start + diff, finish + diff, 1, text)
            for (start, finish), text in subreader(in_srt1)]
    subs.extend([(start, finish, 2, text)
                 for (start, finish), text in subreader(in_srt2)])
    subs.sort()
    result = list()
    index = 0
    while index < len(subs) - 1:
        start, finish, flag, sub_text = subs[index]
        text = [(flag, sub_text)]
        for i in xrange(index + 1, len(subs)):
            sub_rec = subs[i]
            start2, finish2, flag2, sub_text2 = sub_rec
            if start2 < finish:
                finish = max(finish, start + (finish2 - start2) * 2 / 3)
                text.append((flag2, sub_text2))
            else:
                break
        index = i
        result.append(((start, finish), "".join([record[1][1] for record in sorted(enumerate(text), key=lambda (index, item): (item[0], index))])))

    subwriter(out_srt, result)


def _check_argv(params):
    """
    check command line arguments
    """
    import os
    if len(params) < 3:
        print "Error: count of params must be at least 3!\n"
        return False
    if not os.path.exists(params[0]) or not os.path.exists(params[1]):
        print "Error: srt filepathes must be exist!\n"
        return False
    if len(params) > 3:
        try:
            int(params[3])
        except ValueError:
            print "Error: offset must be integer!\n"
            return False
    return True

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('inPaths', type=str, nargs='+',
                        help='srt-file that must be merged')
    parser.add_argument('outPath', type=str,
                        help='path to output file')
    parser.add_argument('--offset', action='store_const', const=0,
                        help='offset in msc (default: 0)')
    if _check_argv(sys.argv[1:]):
        if len(sys.argv) == 4:
            sys.argv.append(0)
        srtmerge(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]))
    else:
        print ''
        parser.print_help()

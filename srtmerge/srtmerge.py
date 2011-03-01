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


def _parse_text(text):
    '''
    ordering text
    '''
    result1 = ''
    result2 = ''
    for flag, item in text:
        if flag == 1:
            result1 += item
        if flag == 2:
            result2 += item
    return result1 + result2


def srtmerge(in_srt1, in_srt2, out_srt, diff=0):
    subs = [(start + diff, finish + diff, 1, text) \
            for (start, finish), text in subreader(in_srt1)]
    subs.extend([(start, finish, 2, text) \
                 for (start, finish), text in subreader(in_srt2)])
    subs.sort()
    i = 0
    result = []
    while i < len(subs):
        start1, finish1, flag1, text1 = subs[i]
        j = i + 1
        start = start1
        finish = finish1
        text = [(flag1, text1)]
        while True:
            if j >= len(subs):
                break
            start2, finish2, flag2, text2 = subs[j]
            if start2 < finish:
                text.append((flag2, text2))
                finish = max(finish1, start + (finish2 - start2) * 2 / 3)
                j += 1
            else:
                break
        result.append(((start, finish), _parse_text(text)))
        i = j

    subwriter(out_srt, result)


def _check_argv(params):
    """
    check command line arguments
    """
    import os
    msg = "Correct: srtmerge srtpath1 srtpath2 outsrtpath [diff]"
    if len(params) < 3:
        print "Error: count of params must be at least 3!\n", msg
        return False
    if not os.path.exists(params[0]) or not os.path.exists(params[1]):
        print "Error: srt filepathes must be exist!\n", msg
        return False
    if not os.path.isabs(params[2]):
        print "Error: output srt file path not correct\n", msg
        return False
    if len(params) > 3:
        try:
            int(params[3])
        except ValueError:
            print "Error: diff must be integer!\n", msg
            return False
    return True

if __name__ == '__main__':
    if _check_argv(sys.argv[1:]):
        if len(sys.argv) == 4:
            sys.argv.append(0)
        srtmerge(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]))

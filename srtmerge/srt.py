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

import re


class SrtFormatError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)


def parse_time(str_time):
    """
    convert string format of start-finish to integer(ms) format
    >>> parse_time("00:14:33,460 --> 00:14:35,419")
    (873460, 875419)
    """
    pattern_time = r"(?P<h1>\d+):(?P<m1>\d+):(?P<s1>\d+),(?P<ms1>\d+)\W*-->\W*(?P<h2>\d+):(?P<m2>\d+):(?P<s2>\d+),(?P<ms2>\d+)$"
    try:
        d = re.match(pattern_time, str_time.strip()).groupdict()
    except:
        message = u"Invalid string format '%s' , expect hh:mm:ss,msc --> hh:mm:ss,msc" % str_time
        raise SrtFormatError(message)
    get_ms = lambda h, m, s, ms: (int(s) + int(m) * 60 + int(h) * 60 * 60) * 1000 + int(ms)
    return get_ms(d['h1'], d['m1'], d['s1'], d['ms1']), get_ms(d['h2'], d['m2'], d['s2'], d['ms2'])


def ms2time(ms):
    """
    convert msc to string format
    >>> ms2time(233243)
    '00:03:53,243'
    >>> ms2time(442)
    '00:00:00,442'
    """
    it = int(ms / 1000)
    ms = ms - it * 1000
    ss = it % 60
    mm = ((it - ss) / 60) % 60
    hh = ((it - (mm * 60) - ss) / 3600) % 60
    return "%02d:%02d:%02d,%03d" % (hh, mm, ss, ms)


def parse_ms(start, finish):
    """
    convert msc representation to string format
    >>> parse_ms(442, 233243)
    '00:00:00,442 --> 00:03:53,243'
    """
    return "%s --> %s" % (ms2time(start), ms2time(finish))


def subreader(file_path):
    """
    return [((time_start, time_finish), subtitle_text), ...]
    file_path: full path to srt-file
    """
    pattern_index = r"^\d+$"
    records, times, text = list(), None, list()
    for line in open(file_path, 'r'):
        line = line.strip()
        if re.match(pattern_index, line):
            if times:
                records.append((times, '\n'.join(text) + '\n'))
                times, text = None, list()
        elif '-->' in line:
            times = parse_time(line)
        elif line:
            text.append(line)
    if times:
        records.append((times, '\n'.join(text) + '\n'))
    return records


def subwriter(filepath, subtitles):
    """
    filepath: path to srt-file
    subtitles: [((time_start, time_finish), subtitle_text), ...]

    write subtitles structure to srt-file
    """
    open(filepath, 'w').writelines(["%s\n%s\n%s\n" % (str(index), parse_ms(start, finish), text) for index, ((start, finish), text) in enumerate(subtitles, 1)])

if __name__ == '__main__':
    import doctest
    print doctest.testmod()

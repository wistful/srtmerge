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


def parse_time(str_time):
    """
    srt time-string format -> (int: start, int: finish)
    """
    pattern_time = r"(\d+):(\d+):(\d+),(\d+)\D*-->\D*(\d+):(\d+):(\d+),(\d+)$"
    groups = re.match(pattern_time, str_time.strip()).groups()
    start = None
    finish = None
    if len(groups) == 8:
        start = (int(groups[2]) + int(groups[1])*60 + int(groups[0])*60*60)*1000 + int(groups[3])
        finish = (int(groups[6]) + int(groups[5])*60 + int(groups[4])*60*60)*1000 + int(groups[7])
    return start, finish


def ms2time(ms):
    """
    int: ms -> str: srt time-format
    """
    it = int(ms / 1000)
    ms = ms - it*1000
    ss = it % 60
    mm = ((it-ss)/60) % 60
    hh = ((it-(mm*60)-ss)/3600) % 60
    return "%02d:%02d:%02d,%03d" % (hh, mm, ss, ms)


def parse_ms(start, finish):
    """
    int: start, int: finish -> str: srt time-format
    """
    return "%s --> %s" % (ms2time(start), ms2time(finish))


def subreader(file_path):
    """
    return [((time_start, time_finish), subtitle_text), ...]
    file_path: full path to srt-file
    """
    pattern_index = r"^\d+$"
    index, times, text = [], [], ['']
    for line in open(file_path, 'r'):
        if re.match(pattern_index, line.strip()):
            index.append(line.strip())
        elif '-->' in line:
            start, finish = parse_time(line)
            times.append((start, finish))
            if len(index) > 1:
                text.append('')
        elif line.strip():
            text[-1] += line.strip() + '\n'
    return zip(times, text)


def subwriter(filepath, subtitles):
    """
    filepath: path to srt-file
    subtitles: [((time_start, time_finish), subtitle_text), ...]

    write subtitles structure to srt-file
    """
    fd = open(filepath, 'w')
    index = 1
    for (start, finish), text in subtitles:
        fd.writelines([str(index), '\n', parse_ms(start, finish), '\n', text, '\n'])
        index += 1


if __name__ == '__main__':
    pass

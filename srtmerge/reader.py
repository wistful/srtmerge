"""Module contains readers for different type of subtitles."""

import collections
import re

from srtmerge.common import Record


def time_to_ms(hours, minutes, seconds, milliseconds):
    """Return milliseconds of given time."""
    all_seconds = seconds + minutes * 60 + hours * 60 * 60
    return all_seconds * 1000 + milliseconds


class BaseReader(collections.abc.Iterable):
    """Base subtitle reader."""


class Srt(BaseReader):
    """Reader for srt subtitles."""

    # pattern to parse *.srt subtitles
    RECORD_PATTERN = re.compile(
        r"(?P<index>\d+)\s*\n"
        "(?P<hh1>\d+):(?P<mm1>\d+):(?P<ss1>\d+)[,\.](?P<ms1>\d+)\W*-->"
        "\W*(?P<hh2>\d+):(?P<mm2>\d+):(?P<ss2>\d+)[,\.](?P<ms2>\d+)\s*\n"
        "(?P<text>.*)",
        re.MULTILINE | re.DOTALL)

    def __init__(self, subs_str):
        """Initialize reader for srt subtitles."""
        self._records = self._irecords(subs_str)

    def __iter__(self):
        """Return instance itself as an iterator."""
        return self

    def __next__(self):
        """Return next subtitle record."""
        return next(self._records)

    def _irecords(self, subs_str):
        """Iterate by subtitle records."""
        match_obj = self.RECORD_PATTERN.search(subs_str)
        while match_obj:
            groups = match_obj.groupdict()
            start_time = time_to_ms(int(groups['hh1']), int(groups['mm1']),
                                    int(groups['ss1']), int(groups['ms1']))
            end_time = time_to_ms(int(groups['hh2']), int(groups['mm2']),
                                  int(groups['ss2']), int(groups['ms2']))

            match_obj = self.RECORD_PATTERN.search(groups['text'])
            if match_obj:
                text = groups['text'][:match_obj.start()]
            else:
                text = groups['text']

            yield Record(groups['index'],
                         start_time, end_time, text.strip('\n '))


def read(filepath, encoding='utf8'):
    return Srt(open(filepath, mode='r', encoding=encoding).read())

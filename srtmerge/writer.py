"""Module contains writers for different type of subtitles."""
import os


class BaseWriter(object):

    def __init__(self, records):
        """Initialize srt subtitles writer."""
        self._records = iter(records)

    def __iter__(self):
        """Return instance itself as an iterator."""
        return self

    def __next__(self):
        """Return next subtitle record."""
        raise NotImplementedError()


class Srt(BaseWriter):
    """Writer for srt subtitles."""

    RECORD_PATTERN = '{index}{sep}{start_time} --> {end_time}{sep}{text}'

    @staticmethod
    def ms_to_str(ms):
        """Convert ms to string representation.

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

    def __next__(self):
        """Return next subtitle record."""
        rec = next(self._records)
        params = {
            'index': rec.index,
            'start_time': self.ms_to_str(rec.start_time),
            'end_time': self.ms_to_str(rec.end_time),
            'text': rec.text,
            'sep': os.linesep,
        }
        return self.RECORD_PATTERN.format(**params)


def write(filepath, records, encoding='utf8'):
    """Write given records into srt-file."""
    sep = os.linesep * 2
    with open(filepath, mode='w', encoding=encoding) as fd:
        fd.write(sep.join(Srt(records)))

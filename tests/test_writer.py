"""Tests for the srtmerge.writer module."""
import pytest

from srtmerge import common
from srtmerge import writer


class TestBaseWriter(object):

    def test_init(self):
        records = ['item1', 'item2']
        writer_obj = writer.BaseWriter(records)
        assert records != writer_obj._records
        assert records == list(writer_obj._records)

    def test_iterator(self):
        writer_obj = writer.BaseWriter([])
        assert iter(writer_obj) is writer_obj

    def test_next(self):
        writer_obj = writer.BaseWriter([])
        with pytest.raises(NotImplementedError):
            next(writer_obj)


class TestSrt(object):

    def test_ms_to_str(self):
        assert writer.Srt.ms_to_str(233243) == '00:03:53,243'
        assert writer.Srt.ms_to_str(442) == '00:00:00,442'

    def test_next(self):
        record = common.Record(
            index=11, start_time=1232, end_time=1240, text='test_text')
        writer_obj = writer.Srt([record])
        rec11 = next(writer_obj)
        expected_rec11 = '11\n00:00:01,232 --> 00:00:01,240\ntest_text'
        assert rec11 == expected_rec11


class TestWrite(object):

    def test_write(self, tmpfile, srt_eng_records, srt_eng_file):
        writer.write(tmpfile.strpath, srt_eng_records)
        text = tmpfile.open(encoding='utf8').read()
        assert text == srt_eng_file.open(encoding='utf8').read()

    def test_write_encoding(self, tmpfile, srt_eng_records, srt_eng_file):
        writer.write(tmpfile.strpath, srt_eng_records, 'utf16')
        text = tmpfile.open(encoding='utf16').read()
        assert text == srt_eng_file.open(encoding='utf8').read()

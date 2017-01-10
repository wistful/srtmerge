"""Tests for the srtmerge.reader module."""
import mock

from srtmerge import reader


class TestTimeToMs(object):

    def test_time_to_ms(self):
        assert reader.time_to_ms(1, 2, 3, 40) == 3723040


class TestBaseReader(object):

    def test_iterable(self):
        assert issubclass(reader.BaseReader, reader.collections.abc.Iterable)


class TestSrt(object):

    def setup(self):
        self.testable_cls = reader.Srt

    def test_init(self):
        test_string = 'test string'
        testable_cfg = {
            '_irecords': mock.MagicMock(),
        }
        with mock.patch.multiple(self.testable_cls, **testable_cfg):
            testable_obj = self.testable_cls(test_string)
            assert testable_obj._records == testable_obj._irecords.return_value
            testable_obj._irecords.assert_called_once_with(test_string)

    def test_irecords(self, srt_eng_text, srt_eng_records):
        testable_obj = self.testable_cls.__new__(self.testable_cls)
        for i, record in enumerate(testable_obj._irecords(srt_eng_text)):
            assert record == srt_eng_records[i]

    def test_iter(self, srt_eng_text, srt_eng_records):
        testable_obj = self.testable_cls(srt_eng_text)
        for i, record in enumerate(testable_obj):
            assert record == srt_eng_records[i]


class TestRead(object):

    def test_read(self, srt_rus_file, srt_rus_text):
        srt_cls = mock.MagicMock()
        srt_patch = mock.patch.object(reader, 'Srt', srt_cls)
        with srt_patch:
            result = reader.read(srt_rus_file.strpath)
            assert result == srt_cls.return_value
            srt_cls.assert_called_once_with(srt_rus_text)

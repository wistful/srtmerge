"""Tests for the srtmerge.common module."""

from srtmerge import common


class TestGetDelta(object):

    def test_no_record(self):
        record = None
        position = 123

        result = common.get_delta(record, position)
        assert result == 0

    def test_outside_record(self):
        record = common.Record(
            index=1, start_time=1000, end_time=2000, text='hello world')
        assert 0 == common.get_delta(record, record.start_time - 1)
        assert 0 == common.get_delta(record, record.end_time + 1)

    def test_equals_start_time(self):
        record = common.Record(
            index=1, start_time=1000, end_time=2000, text='hello world')
        assert abs(10000 - common.get_delta(record, record.start_time)) < 1

    def test_equals_end_time(self):
        record = common.Record(
            index=1, start_time=1000, end_time=2000, text='hello world')
        assert common.get_delta(record, record.end_time) <= 0.1

    def test_in_the_middle(self):
        record = common.Record(
            index=1, start_time=1000, end_time=2000, text='hello world')
        position = record.start_time + (record.end_time - record.start_time) / 2  # noqa: E501 pylint: disable=line-too-long
        assert common.get_delta(record, position) >= 2500

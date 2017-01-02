"""Tests configuration."""
import os
import string
import random

from srtmerge.common import Record
import pytest


ENCODING = 'utf8'


@pytest.fixture
def rndfilename():
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for i in range(12))


@pytest.fixture
def tmpfile(tmpdir):
    return tmpdir.join(rndfilename())


@pytest.fixture
def srt_eng_records():
    return [
        Record(index=65, start_time=163802, end_time=167438, text="♪ Our whole universe was%sin a hot, dense state ♪" % os.linesep),  # noqa: E501 pylint: disable=line-too-long
        Record(index=66, start_time=167439, end_time=170758, text="♪ Then nearly 14 billion years%sago expansion started... Wait! ♪" % os.linesep),  # noqa: E501 pylint: disable=line-too-long
        Record(index=67, start_time=170759, end_time=172393, text="♪ The Earth began to cool ♪"),  # noqa: E501 pylint: disable=line-too-long
        Record(index=68, start_time=172394, end_time=174928, text="♪ The autotrophs began to drool,%sNeanderthals developed tools ♪" % os.linesep),  # noqa: E501 pylint: disable=line-too-long
        Record(index=69, start_time=174929, end_time=177614, text="♪ We built the Wall ♪ ♪ <i>We%sbuilt the pyramids</i> ♪" % os.linesep),  # noqa: E501 pylint: disable=line-too-long
        Record(index=70, start_time=177615, end_time=180267, text="♪ Math, Science, History,%sunraveling the mystery ♪" % os.linesep),  # noqa: E501 pylint: disable=line-too-long
        Record(index=71, start_time=180268, end_time=182169, text="♪ That all started%swith a big bang ♪" % os.linesep),  # noqa: E501 pylint: disable=line-too-long
        Record(index=72, start_time=182170, end_time=183138, text="♪ <i>Bang!</i> ♪"),  # noqa: E501 pylint: disable=line-too-long
    ]


@pytest.fixture
def srt_rus_records():
    return [
        Record(index=65, start_time=163802, end_time=167438, text="*Вся наша Вселенная находилась в горячем и плотном состоянии,*"),  # noqa: E501 pylint: disable=line-too-long
        Record(index=66, start_time=167439, end_time=170758, text="*А, примерно четырнадцать миллиардов лет назад началось расширение. Стоп..*"),  # noqa: E501 pylint: disable=line-too-long
        Record(index=67, start_time=170759, end_time=172393, text="*Земля начала остывать,*"),  # noqa: E501 pylint: disable=line-too-long
        Record(index=68, start_time=172394, end_time=174928, text="*Автотрофы стали развиваться,%sНеандертальцы изобрели орудия труда,*" % os.linesep),  # noqa: E501 pylint: disable=line-too-long
        Record(index=69, start_time=174929, end_time=177614, text="*Мы построили Стену%sМы построили Пирамиды,*" % os.linesep),  # noqa: E501 pylint: disable=line-too-long
        Record(index=70, start_time=177615, end_time=180267, text="*Математика, наука, история, разгадывание тайн,*" % os.linesep),  # noqa: E501 pylint: disable=line-too-long
        Record(index=71, start_time=180268, end_time=182169, text="*Все это началось с Большого Взрыва!*" % os.linesep),  # noqa: E501 pylint: disable=line-too-long
        Record(index=72, start_time=182170, end_time=183138, text="*Взрыв!*"),
    ]


@pytest.fixture
def srt_eng_text():
    text = """
    65
    00:02:43,802 --> 00:02:47,438
    ♪ Our whole universe was
    in a hot, dense state ♪

    66
    00:02:47,439 --> 00:02:50,758
    ♪ Then nearly 14 billion years
    ago expansion started... Wait! ♪

    67
    00:02:50,759 --> 00:02:52,393
    ♪ The Earth began to cool ♪

    68
    00:02:52,394 --> 00:02:54,928
    ♪ The autotrophs began to drool,
    Neanderthals developed tools ♪

    69
    00:02:54,929 --> 00:02:57,614
    ♪ We built the Wall ♪ ♪ <i>We
    built the pyramids</i> ♪

    70
    00:02:57,615 --> 00:03:00,267
    ♪ Math, Science, History,
    unraveling the mystery ♪

    71
    00:03:00,268 --> 00:03:02,169
    ♪ That all started
    with a big bang ♪

    72
    00:03:02,170 --> 00:03:03,138
    ♪ <i>Bang!</i> ♪
    """
    return os.linesep.join(
        line.strip() for line in text.split(os.linesep))[1:-1]


@pytest.fixture
def srt_rus_text():
    text = """
    65
    00:02:43.802 --> 00:02:47.438
    *Вся наша Вселенная находилась в горячем и плотном состоянии,*

    66
    00:02:47.439 --> 00:02:50.758
    *А, примерно четырнадцать миллиардов лет назад началось расширение. Стоп..*

    67
    00:02:50.759 --> 00:02:52.393
    *Земля начала остывать,*

    68
    00:02:52.394 --> 00:02:54.928
    *Автотрофы стали развиваться,
    Неандертальцы изобрели орудия труда,*

    69
    00:02:54.929 --> 00:02:57.614
    *Мы построили Стену
    Мы построили Пирамиды,*

    70
    00:02:57.615 --> 00:03:00.267
    *Математика, наука, история, разгадывание тайн,*

    71
    00:03:00.268 --> 00:03:02.169
    *Все это началось с Большого Взрыва!*

    72
    00:03:02.170 --> 00:03:03.138
    *Взрыв!*
    """
    return os.linesep.join(
        line.strip() for line in text.split(os.linesep))[1:-1]


@pytest.fixture
def srt_eng_file(tmpdir, srt_eng_text):
    tmpfile_obj = tmpfile(tmpdir)
    tmpfile_obj.write_text(srt_eng_text, ENCODING)
    return tmpfile_obj


@pytest.fixture
def srt_rus_file(tmpdir, srt_rus_text):
    tmpfile_obj = tmpfile(tmpdir)
    tmpfile_obj.write_text(srt_rus_text, ENCODING)
    return tmpfile_obj

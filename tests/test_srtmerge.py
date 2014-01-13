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

import os
import sys
sys.path.append("..")

import tempfile
import unittest

from srtmerge import srt

DEFAULT_ENCODING = srt.DEFAULT_ENCODING

RES_TIME = [("00:04:03,638 --> 00:04:06,439", (243638, 246439)),
            ("00:04:08,442 --> 00:04:09,506", (248442, 249506)),
            ("00:00:00,442 --> 00:00:02,777", (442, 2777)),
            ("01:00:08,442 --> 01:00:19,985", (3608442, 3619985)),
            ("03:37:00,879 --> 03:58:29,312", (13020879, 14309312)),
            ]

INVALID_TIME = ["00:14:33 --> 00:14:35,419",
                "invalid string --> correct string"]

SUBTITLES_OFFSET = 1250

SUBTITLES = """1
00:03:49,824 --> 00:03:53,243
♪ Our whole universe
was in a hot, dense state ♪

2
00:03:53,244 --> 00:03:56,863
♪ Then nearly 14 billion years
ago expansion started... Wait! ♪

3
00:03:56,864 --> 00:03:58,731
♪ The Earth began to cool ♪

4
00:03:58,732 --> 00:04:01,434
♪ The autotrophs began to drool,
Neanderthals developed tools ♪

5
00:04:01,435 --> 00:04:03,637
♪ We built the Wall ♪
♪ <i>We built the pyramids</i> ♪

6
00:04:03,638 --> 00:04:06,439
♪ Math, Science, History,
unraveling the mystery ♪

7
00:04:06,440 --> 00:04:08,441
♪ That all started
with a big bang ♪

8
00:04:08,442 --> 00:04:09,506
♪ <i>Bang!</i> ♪

"""

SUBTITLES_RUS = """
268
00:14:13,420 --> 00:14:15,979
Джон №1, ты человек-единорог.

269
00:14:15,980 --> 00:14:19,979
Джон №2, ты лесной эльф.

270
00:14:20,180 --> 00:14:24,179
И Фил, ты цыганка-убийца,
Эсмеральда.

271
00:14:25,020 --> 00:14:26,459
Я женщина?

272
00:14:30,780 --> 00:14:32,299
Не думаю, что хотел бы
быть женщиной.

273
00:14:32,300 --> 00:14:33,459
Просто прими это.

274
00:14:33,460 --> 00:14:35,419
Это закончится.

275
00:14:35,420 --> 00:14:39,299
Итак, джентльмены, вы готовы
открыть двери в свой разум,

276
00:14:39,300 --> 00:14:42,019
и перенестись в
неизведанный мир?

"""

SUBTITLES_ENG = """
270
00:14:13,420 --> 00:14:15,979
John One, you're a unicorn man.

271
00:14:15,980 --> 00:14:19,979
John Two, you're a wood fairy.

272
00:14:20,180 --> 00:14:24,179
And Phil, you're the Gypsy
assassin, Esmerelda.

273
00:14:25,020 --> 00:14:26,459
I'm a woman?

274
00:14:30,780 --> 00:14:32,299
I don't think I want to be a woman.

275
00:14:32,300 --> 00:14:33,459
Just go with it.

276
00:14:33,460 --> 00:14:35,419
It will end.

277
00:14:35,420 --> 00:14:39,299
So, gentlemen, are you prepared
to open the doors to your mind

278
00:14:39,300 --> 00:14:42,019
and travel to worlds
hitherto undreamed of?

"""

SUBTITLES_ALL = """1
00:14:13,420 --> 00:14:15,979
John One, you're a unicorn man.
Джон №1, ты человек-единорог.

2
00:14:15,980 --> 00:14:19,979
John Two, you're a wood fairy.
Джон №2, ты лесной эльф.

3
00:14:20,180 --> 00:14:24,179
And Phil, you're the Gypsy
assassin, Esmerelda.
И Фил, ты цыганка-убийца,
Эсмеральда.

4
00:14:25,020 --> 00:14:26,459
I'm a woman?
Я женщина?

5
00:14:30,780 --> 00:14:32,299
I don't think I want to be a woman.
Не думаю, что хотел бы
быть женщиной.

6
00:14:32,300 --> 00:14:33,459
Just go with it.
Просто прими это.

7
00:14:33,460 --> 00:14:35,419
It will end.
Это закончится.

8
00:14:35,420 --> 00:14:39,299
So, gentlemen, are you prepared
to open the doors to your mind
Итак, джентльмены, вы готовы
открыть двери в свой разум,

9
00:14:39,300 --> 00:14:42,019
and travel to worlds
hitherto undreamed of?
и перенестись в
неизведанный мир?

"""

SUBTITLES_ALL_DIFF = """1
00:14:14,670 --> 00:14:17,229
John One, you're a unicorn man.
Джон №1, ты человек-единорог.

2
00:14:17,230 --> 00:14:21,229
John Two, you're a wood fairy.
Джон №2, ты лесной эльф.

3
00:14:21,430 --> 00:14:25,429
And Phil, you're the Gypsy
assassin, Esmerelda.
И Фил, ты цыганка-убийца,
Эсмеральда.

4
00:14:26,270 --> 00:14:27,709
I'm a woman?
Я женщина?

5
00:14:32,030 --> 00:14:33,549
I don't think I want to be a woman.
Не думаю, что хотел бы
быть женщиной.

6
00:14:33,550 --> 00:14:34,709
Just go with it.
Просто прими это.

7
00:14:34,710 --> 00:14:36,669
It will end.
Это закончится.

8
00:14:36,670 --> 00:14:40,549
So, gentlemen, are you prepared
to open the doors to your mind
Итак, джентльмены, вы готовы
открыть двери в свой разум,

9
00:14:40,550 --> 00:14:43,269
and travel to worlds
hitherto undreamed of?
и перенестись в
неизведанный мир?

"""

SUBTITLES_STRUCTURE = [(229824, 233243, '♪ Our whole universe\nwas in a hot, dense state ♪\n'), (233244, 236863, '♪ Then nearly 14 billion years\nago expansion started... Wait! ♪\n'), (236864, 238731, '♪ The Earth began to cool ♪\n'), (238732, 241434, '♪ The autotrophs began to drool,\nNeanderthals developed tools ♪\n'), (241435, 243637, '♪ We built the Wall ♪\n♪ <i>We built the pyramids</i> ♪\n'), (243638, 246439, '♪ Math, Science, History,\nunraveling the mystery ♪\n'), (246440, 248441, '♪ That all started\nwith a big bang ♪\n'), (248442, 249506, '♪ <i>Bang!</i> ♪\n')]

if sys.version_info[0] < 3:
    SUBTITLES_STRUCTURE = [(rec[0], rec[1], rec[2].decode(DEFAULT_ENCODING))
                           for rec in SUBTITLES_STRUCTURE]


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self._fds = []
        self._pathes = []

    def tearDown(self):
        try:
            list(map(os.close, self._fds))
            list(map(os.remove, self._pathes))
        except OSError:
            pass

    def get_tmp_path(self):
        fd, file_path = tempfile.mkstemp()
        self._fds.append(fd)
        self._pathes.append(file_path)
        return file_path


class SrtText(BaseTestCase):

    def test_parse_time(self):
        for str_time, times in RES_TIME:
            self.assertEqual(srt.parse_time(str_time), times)
        for inv_time in INVALID_TIME:
            self.assertRaises(srt.SrtFormatError, srt.parse_time, (inv_time,))

    def test_ms2time(self):
        self.assertEqual(srt.ms2time(233243), '00:03:53,243')
        self.assertEqual(srt.ms2time(248442), '00:04:08,442')
        self.assertEqual(srt.ms2time(442), '00:00:00,442')

    def test_parse_ms(self):
        for str_time, times in RES_TIME:
            self.assertEqual(srt.parse_ms(*times), str_time)

    def test_subreader(self):
        file_path = self.get_tmp_path()
        with open(file_path, 'w') as fd:
            fd.write(SUBTITLES)

        subs = [(record.start, record.finish, record.text)
                for record in srt.subreader(file_path)]
        self.assertEqual(subs, SUBTITLES_STRUCTURE)

    def test_subwriter(self):
        filepath = self.get_tmp_path()
        subs = [srt.SubRecord(start, finish, text)
                for start, finish, text in SUBTITLES_STRUCTURE]
        srt.subwriter(filepath, subs)
        with open(filepath) as fd:
            self.assertEqual(fd.read(), SUBTITLES)


class SrtMergeTest(BaseTestCase):

    def _get_files(self):
        filepath_eng = self.get_tmp_path()
        filepath_rus = self.get_tmp_path()
        filepath_all = self.get_tmp_path()
        with open(filepath_eng, 'w') as fd:
            fd.write(SUBTITLES_ENG)
        with open(filepath_rus, 'w') as fd:
            fd.write(SUBTITLES_RUS)

        return filepath_eng, filepath_rus, filepath_all

    def test_merge(self):
        filepath_eng, filepath_rus, filepath_all = self._get_files()

        srt.srtmerge([filepath_eng, filepath_rus], filepath_all)
        with open(filepath_all) as fd:
            self.assertEqual(fd.read(), SUBTITLES_ALL)

    def test_merge_with_diff(self):
        filepath_eng, filepath_rus, filepath_all = self._get_files()

        srt.srtmerge([filepath_eng, filepath_rus],
                     filepath_all, SUBTITLES_OFFSET)

        with open(filepath_all) as fd:
            self.assertEqual(fd.read(), SUBTITLES_ALL_DIFF)


if __name__ == '__main__':
    unittest.main()

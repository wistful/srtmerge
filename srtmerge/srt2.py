# -*- coding: utf-8 -*-

"""Module contains functions to merge several srt files into one."""
#
#    Copyleft 2014 wistful <wst public mail at gmail com>
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

import collections
import logging
import re

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('srt.log', mode='w', encoding='utf8')
fh.setLevel(logging.DEBUG)

logger.addHandler(fh)

logger.debug('hello')


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

S_RUS = """
115
00:06:10.516 --> 00:06:13.157
но Дания решила раз и навсегда
разобраться с троллями,

116
00:06:13.237 --> 00:06:14.723
только им не хватает денег,

117
00:06:14.724 --> 00:06:16.952
и я предлагаю
помочь им их собрать.

118
00:06:17.084 --> 00:06:19.172
Да, но первый раз ты
выразилась смешнее.

119
00:06:19.252 --> 00:06:20.292
А что я сказала?

120
00:06:20.372 --> 00:06:22.590
Ну помнишь, ты сказала:
"А может, нам собрать деньги в...

121
00:06:22.625 --> 00:06:23.988
Как там? Помнишь? Напомни...

122
00:06:24.018 --> 00:06:25.188
Где это было? В "Дэннис"?

123
00:06:25.268 --> 00:06:27.292
Да, мы еще ели тот десерт...
Как его там...

124
00:06:27.372 --> 00:06:29.508
А, да, ты его еще
проливал и проливал.

125
00:06:29.588 --> 00:06:32.284
Да, да. А еще там был
парень с такой... такой...

126
00:06:32.364 --> 00:06:35.316
Со странной стрижкой. И ты сказал,
что она как член у него на голове.

127
00:06:35.396 --> 00:06:38.105
Да, да, да.
А ты мне сказала, что...

128
00:06:45.859 --> 00:06:47.632
О, привет, ребята.
Чё хотели?

129
00:06:48.460 --> 00:06:50.932
Ах, да.
Сбор денег всей школой.

130
00:06:51.012 --> 00:06:54.128
Завтра мы обойдем все классы
и всё подробно расскажем.

131
00:06:54.252 --> 00:06:55.219
После чего...
"""

S_ENG = """
150
00:06:10.636 --> 00:06:13.220
Denmark is trying to make
trolling a thing of the past.

151
00:06:13.256 --> 00:06:16.757
They're asking for help, and I
thought "Why not a school fundraiser?"

152
00:06:16.809 --> 00:06:19.093
Yeah, but the way you said it was
actually way funnier, remember?

153
00:06:19.145 --> 00:06:20.928
- What? How did I say it?
- Remember? You were like,

154
00:06:20.930 --> 00:06:23.664
"Oh, what if we had a fundraiser in..."
What was it? Remember? It was like...

155
00:06:23.716 --> 00:06:25.182
When was this? Were we at Denny's?

156
00:06:25.234 --> 00:06:27.108
Yeah, we were having that
dessert thing. What was that?

157
00:06:27.143 --> 00:06:29.436
[Giggling] Oh, right, and you
kept spilling it and everything.

158
00:06:29.488 --> 00:06:32.406
Yeah, yeah. Remember there
was that guy that had the...

159
00:06:32.441 --> 00:06:34.742
He had that weird haircut and you
kept saying that it looked like

160
00:06:34.777 --> 00:06:37.778
- he had a dick on his head.
- Yeah, yeah. And you said that...

161
00:06:37.780 --> 00:06:39.280
[Whispering]

162
00:06:39.282 --> 00:06:41.532
[Giggling]

163
00:06:45.788 --> 00:06:48.372
Oh, hey, guys. W-What's up?

164
00:06:48.424 --> 00:06:50.791
Oh, right! A school fundraiser.

165
00:06:50.843 --> 00:06:52.960
Tomorrow, we'll be going
to each individual class

166
00:06:52.962 --> 00:06:54.044
with more information.

167
00:06:54.096 --> 00:06:55.296
And after that...
"""

# pattern to parse *.srt subtitles
SRT_RECORD_PATTERN = re.compile(
    r"(?P<index>\d+)\s*\n"
    "(?P<hh1>\d+):(?P<mm1>\d+):(?P<ss1>\d+)[,\.](?P<ms1>\d+)\W*-->"
    "\W*(?P<hh2>\d+):(?P<mm2>\d+):(?P<ss2>\d+)[,\.](?P<ms2>\d+)\s*\n"
    "(?P<text>.*)",
    re.MULTILINE | re.DOTALL)


# Structure for a subtitle record
Record = collections.namedtuple(
    'Record', ['index', 'start_time', 'end_time', 'text'])


MAX_OFFSET = 75 ** 2  # offset in percents**2
MAX_DURATION = 3000  # max duration in ms for one subtitle record
STEP = 100  # step in ms


def time_to_ms(hours, minutes, seconds, milliseconds):
    """Return milliseconds of given time."""
    all_seconds = seconds + minutes * 60 + hours * 60 * 60
    return all_seconds * 1000 + milliseconds


def ms2time(ms):
    """Convert ms to srt subtitle format.

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


def get_delta(record, position):
    """Return delta for given subtitle and position."""
    if not record:
        return 0
    elif position < record.start_time or position > record.end_time:
        return 0
    else:
        # how many ms are in one percent of subtitle record duration
        ms_per_percent = 100.0 / (record.end_time - record.start_time)
        # delta is lesser in the beginning and end of records
        # and the biggest in the middle of the record
        return 0.1 + (100 - ms_per_percent * (position - record.start_time))**2


def iter_subs(subs):
    """Parse subs and yields Record objects."""
    match_obj = SRT_RECORD_PATTERN.search(subs)
    while match_obj:
        groups = match_obj.groupdict()
        start_time = time_to_ms(int(groups['hh1']), int(groups['mm1']),
                                int(groups['ss1']), int(groups['ms1']))
        end_time = time_to_ms(int(groups['hh2']), int(groups['mm2']),
                              int(groups['ss2']), int(groups['ms2']))

        match_obj = SRT_RECORD_PATTERN.search(groups['text'])
        if match_obj:
            text = groups['text'][:match_obj.start()]
        else:
            text = groups['text']

        yield Record(groups['index'], start_time, end_time, text.strip('\n '))


def merge(subs1, subs2):
    """Generator to merge records from given subtitles."""
    subs1 = sorted(subs1, key=lambda item: item.start_time)
    subs2 = sorted(subs2, key=lambda item: item.start_time)

    # max indexes for subtitles
    max_index1, max_index2 = len(subs1) - 1, len(subs2) - 1
    # temporary indexes for the subtitles records
    tmp_init_index1, tmp_init_index2 = 0, 0

    index = 1  # index of merged subtitle record
    while True:
        # initial index is the first not processed index of input subtitle
        init_index1, init_index2 = tmp_init_index1, tmp_init_index2

        if init_index1 > max_index1 and init_index2 > max_index2:
            # all records were processed
            break

        # initial subtitle records
        rec1 = subs1[init_index1] if init_index1 <= max_index1 else None
        rec2 = subs2[init_index2] if init_index2 <= max_index2 else None

        # min start time of next merged subtitle record
        start_time = min(rec1.start_time if rec1 else float('inf'),
                         rec2.start_time if rec2 else float('inf'))
        # max end time of next merged subtitle record
        end_time = max(
            rec1.end_time if rec1 else float('nan'),
            rec2.end_time if rec2 else float('nan'),
            start_time + MAX_DURATION)

        position = start_time  # goes from min start_time to max end_time
        # min_delta uses to find most suitable
        # start_time and end_time for next merged record
        min_delta = float('inf')

        # temporary lists with indexed of processed input subtitle records
        tmp_subs1 = []
        tmp_subs2 = []

        # temporary indexes of input subtitle records
        tmp_index1 = init_index1
        tmp_index2 = init_index2

        record = None  # next merged record
        while position <= end_time:
            if tmp_index1 > max_index1 and tmp_index2 > max_index2:
                # all input records were processed
                break

            # calculates delta for every input record
            # delta is lesser in the beginning and end of records
            # and biggest in the middle of the record
            delta1 = get_delta(rec1, position)
            delta2 = get_delta(rec2, position)

            # delta < MAX_OFFSE means that enough position is too far
            # from the beginning of the input record
            # and text of the record must be included into merged record
            if 0 < delta1 < MAX_OFFSET and tmp_index1 not in tmp_subs1:
                tmp_subs1.append(tmp_index1)

            if 0 < delta2 < MAX_OFFSET and tmp_index2 not in tmp_subs2:
                tmp_subs2.append(tmp_index2)

            # delta is a sum of two deltas for every input subtitle record
            # with some influence of count processed records.
            delta = (delta1 + delta2) * (len(tmp_subs1) + len(tmp_subs2))

            if delta < min_delta and (tmp_subs1 or tmp_subs2):
                min_delta = delta
                text1 = '\n'.join(subs1[i].text for i in tmp_subs1)
                text2 = '\n'.join(subs2[i].text for i in tmp_subs2)
                record = Record(index, start_time, position,
                                '%s\n%s' % (text1, text2))

                tmp_init_index1 = init_index1 + len(tmp_subs1)
                tmp_init_index2 = init_index2 + len(tmp_subs2)

            position += STEP

            # position is outside of the input record,
            # increase temporary index and use next input record.
            if rec1 and position > rec1.end_time and tmp_index1 < max_index1:
                tmp_index1 += 1
                rec1 = subs1[tmp_index1]
            if rec2 and position > rec2.end_time and tmp_index2 < max_index2:
                tmp_index2 += 1
                rec2 = subs2[tmp_index2]

        if record:
            yield record
            index += 1


def main():
    merged = merge(iter_subs(SUBTITLES_ENG), iter_subs(SUBTITLES_RUS))
    merged = merge(iter_subs(S_ENG), iter_subs(S_RUS))

    for record in merged:
        logger.debug(
            '\n%s\n%s\n', record.end_time - record.start_time, record.text)

main()

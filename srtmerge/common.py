# coding=utf8

"""Module contains functions to merger two subtitles into one."""
import collections

# Structure for a subtitle record
Record = collections.namedtuple(
    'Record', ['index', 'start_time', 'end_time', 'text'])


MAX_OFFSET = 75 ** 2  # offset in percents**2
MAX_DURATION = 3000  # max duration in ms for one subtitle record
STEP = 100  # step in ms


def get_delta(record, position):
    """Return delta for given subtitle record and position."""
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
            rec1.end_time if rec1 else start_time + MAX_DURATION,
            rec2.end_time if rec2 else start_time + MAX_DURATION,
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

#!/usr/bin/python

# Copy function with progress display using a callback function.
# The callback function used here mimics the output of
# 'rsync --progress'.

# Copyright (C) 2012 Thomas Hipp

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# https://gist.github.com/monstermunchkin/2391716

import datetime
import os

def copy(src, dst, callback=None):
    blksize = 1048576 # 1MiB
    try:
        s = open(src, 'rb')
        d = open(dst, 'wb')
    except (KeyboardInterrupt, Exception) as e:
        if 's' in locals():
            s.close()
        if 'd' in locals():
            d.close()
        raise
    try:
        total = os.stat(src).st_size
        pos = 0
        start_elapsed = datetime.datetime.now()
        start_update = datetime.datetime.now()
        while True:
            buf = s.read(blksize)
            bytes_written = d.write(buf)
            end = datetime.datetime.now()
            pos += bytes_written
            diff = end - start_update
            if callback and diff.total_seconds() >= 0.2:
                callback(pos, total, end - start_elapsed)
                start_update = datetime.datetime.now()
            if bytes_written < len(buf) or bytes_written == 0:
                break
    except (KeyboardInterrupt, Exception) as e:
        s.close()
        d.close()
        raise
    else:
        callback(total, total, end - start_elapsed)
        s.close()
        d.close()

def tmstr(t):
    days, rest = divmod(t, 86400)
    hours, rest = divmod(rest, 3600)
    minutes, seconds = divmod(rest, 60)
    return '{0:4d}:{1:02d}:{2:02d}'.format(int(days * 24 + hours),
            int(minutes), round(seconds))

mod = 101
speed = [0] * mod
index = 0

def progress(pos, total, elapsed):
    global speed
    global index
    global mod
    elapsed_ = elapsed.total_seconds()
    speed[index % mod] = pos / elapsed_
    index = (index + 1) % mod
    out = '{0:12} {1:4.0%} {2:7.2f}{unit}B/s {3}'
    unit = ('Mi', 1048576) if total > 999999 else ('ki', 1024)
    # complete
    if pos == total:
        print(out.format(pos, pos / total, sum(speed) / mod / unit[1],
            tmstr(elapsed_), unit=unit[0]))
    # in progress
    else:
        print(out.format(pos, pos / total, sum(speed) / mod / unit[1],
            tmstr((total - pos) / sum(speed) * mod), unit=unit[0]), end='')
        print('\r')
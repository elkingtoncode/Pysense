from __future__ import print_function
import os

from hardware.detect_utils import cmd


def sizeingb(size):
    return int((size * 512) / (1000 * 1000 * 1000))


def disksize(name):
    size = open('/sys/block/' + name + '/size').read(-1)
    return sizeingb(long(size))


def disknames():
    return [name for name in os.listdir('/sys/block')
            if name[1] == 'd' and name[0] in 'shv']


def parse_hdparm_output(output):
    res = output.split(' = ')
    if len(res) != 2:
        return 0.0
    try:
        mbsec = res[1].split(' ')[-2]
        return float(mbsec)
    except (ValueError, KeyError):
        return 0.0


def diskperfs(names):
    return dict((name, parse_hdparm_output(cmd('hdparm -t /dev/%s' % name)))
                for name in names)


def disksizes(names):
    return dict((name, disksize(name)) for name in names)


def _main():
    names = disknames()
    sizes = disksizes(names)
    names = [name for name, size in sizes.items() if size > 0]
    perfs = diskperfs(names)
    for name in names:
        print('%s %d GB (%.2f MB/s)' % (name, sizes[name], perfs[name]))

if __name__ == "__main__":
    _main()

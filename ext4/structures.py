"""
Estruturas básicas do EXT4.
"""

import struct


def u16(buf, off):
    return struct.unpack_from("<H", buf, off)[0]


def u32(buf, off):
    return struct.unpack_from("<I", buf, off)[0]


def u64(buf, off):
    return struct.unpack_from("<Q", buf, off)[0]


def s16(buf, off):
    return struct.unpack_from("<h", buf, off)[0]


def s32(buf, off):
    return struct.unpack_from("<i", buf, off)[0]


def bytes_at(buf, off, size):
    return buf[off:off + size]
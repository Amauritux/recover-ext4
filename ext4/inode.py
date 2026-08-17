"""
Parser de inode EXT4.
"""

from ext4.structures import u16, u32


EXT4_EXTENTS_FL = 0x00080000


class Ext4Inode:

    def __init__(self, data):

        if len(data) != 256:
            raise ValueError("Um inode EXT4 deve possuir 256 bytes.")

        self.raw = data

        self.mode = u16(data, 0x00)
        self.uid = u16(data, 0x02)

        self.size_lo = u32(data, 0x04)

        self.atime = u32(data, 0x08)
        self.ctime = u32(data, 0x0C)
        self.mtime = u32(data, 0x10)
        self.dtime = u32(data, 0x14)

        self.gid = u16(data, 0x18)
        self.links = u16(data, 0x1A)

        self.blocks_lo = u32(data, 0x1C)

        self.flags = u32(data, 0x20)

        self.i_block = data[0x28:0x28+60]

        self.generation = u32(data, 0x64)

        self.size_high = u32(data, 0x6C)

    @property
    def size(self):

        return (self.size_high << 32) | self.size_lo

    def has_extents(self):

        return (self.flags & EXT4_EXTENTS_FL) != 0

    def is_regular_file(self):

        return (self.mode & 0xF000) == 0x8000

    def is_directory(self):

        return (self.mode & 0xF000) == 0x4000

    def deleted(self):

        return self.dtime != 0

    def extent_header(self):

        return self.i_block[:12]

    def summary(self):

        return {
            "mode": hex(self.mode),
            "size": self.size,
            "links": self.links,
            "flags": hex(self.flags),
            "blocks": self.blocks_lo,
            "deleted": self.deleted(),
            "extents": self.has_extents(),
            "regular": self.is_regular_file(),
            "directory": self.is_directory(),
        }
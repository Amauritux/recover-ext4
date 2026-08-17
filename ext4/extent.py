"""
Leitor do cabeçalho de extents do EXT4.
"""

import struct


class ExtentHeader:

    def __init__(self, data):

        if len(data) < 12:
            raise ValueError("Cabeçalho inválido.")

        (
            self.magic,
            self.entries,
            self.max_entries,
            self.depth,
            self.generation
        ) = struct.unpack("<HHHHI", data[:12])

    def valid(self):

        if self.magic != 0xF30A:
            return False

        if self.entries > self.max_entries:
            return False

        if self.max_entries > 340:
            return False

        if self.depth > 5:
            return False

        return True

    def summary(self):

        return {
            "entries": self.entries,
            "max": self.max_entries,
            "depth": self.depth,
            "generation": self.generation
        }
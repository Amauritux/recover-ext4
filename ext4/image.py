"""
Camada de acesso à imagem EXT4.

Todo o projeto utiliza esta classe para ler a imagem.
"""

from pathlib import Path
import config


class ImageReader:

    def __init__(self, image_path=None):

        self.image_path = Path(image_path or config.IMAGE_FILE)
        self.fd = None

    def open(self):

        if self.fd is None:
            self.fd = open(self.image_path, "rb")

    def close(self):

        if self.fd:
            self.fd.close()
            self.fd = None

    def read(self, offset, size):

        self.open()

        self.fd.seek(offset)

        return self.fd.read(size)

    def partition_read(self, offset, size):

        return self.read(
            config.PARTITION_OFFSET + offset,
            size
        )

    def block_offset(self, block):

        return (
            config.PARTITION_OFFSET +
            block * config.BLOCK_SIZE
        )

    def read_block(self, block):

        return self.read(
            self.block_offset(block),
            config.BLOCK_SIZE
        )

    def inode_offset(self,
                     inode_table_block,
                     inode_index):

        return (
            self.block_offset(inode_table_block)
            + inode_index * config.INODE_SIZE
        )

    def read_inode(self,
                   inode_table_block,
                   inode_index):

        return self.read(
            self.inode_offset(
                inode_table_block,
                inode_index
            ),
            config.INODE_SIZE
        )
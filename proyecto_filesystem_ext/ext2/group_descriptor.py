# Cosas a revisar (y creo que ya estaria completa esta clase):
#  - ver si son necesarios los getters y setters de 'bg_pad' y 'bg_reserved'
#  - en el pdf de ext2/3, en esta seccion del group descriptor tambien habla
#    sobre los bitmaps de bloques e inodos, pero creo que tocare ese tema
#    cuando haga la clase 'ext2' que englobe todo.

import struct

class GroupDescriptor:
    """
    Class representing the Group Descriptor of an ext2 filesystem.
    Each block group has its own group descriptor (which has information about the group).
    """
    def __init__(self, data):
        self._raw_data = data
        # ---
        self._bg_block_bitmap = -1
        self._bg_inode_bitmap = -1
        self._bg_inode_table = -1
        self._bg_free_blocks_count = -1
        self._bg_free_inodes_count = -1
        self._bg_used_dirs_count = -1
        self._bg_pad = -1 # Alignment to word [16-bits padding]
        self._bg_reserved = -1 # Nulls to pad out 32 bytes [12-bytes padding]
        # ---
        self._parse()

    @property
    def raw_data(self):
        return self._raw_data

    @raw_data.setter
    def raw_data(self, value):
        pass

    # ---

    @property
    def bg_block_bitmap(self):
        return self._bg_block_bitmap

    @bg_block_bitmap.setter
    def bg_block_bitmap(self, value):
        self._bg_block_bitmap = value

    @property
    def bg_inode_bitmap(self):
        return self._bg_inode_bitmap

    @bg_inode_bitmap.setter
    def bg_inode_bitmap(self, value):
        self._bg_inode_bitmap = value

    @property
    def bg_inode_table(self):
        return self._bg_inode_table

    @bg_inode_table.setter
    def bg_inode_table(self, value):
        self._bg_inode_table = value

    @property
    def bg_free_blocks_count(self):
        return self._bg_free_blocks_count

    @bg_free_blocks_count.setter
    def bg_free_blocks_count(self, value):
        self._bg_free_blocks_count = value

    @property
    def bg_free_inodes_count(self):
        return self._bg_free_inodes_count

    @bg_free_inodes_count.setter
    def bg_free_inodes_count(self, value):
        self._bg_free_inodes_count = value

    @property
    def bg_used_dirs_count(self):
        return self._bg_used_dirs_count

    @bg_used_dirs_count.setter
    def bg_used_dirs_count(self, value):
        self._bg_used_dirs_count = value

    @property
    def bg_pad(self):
        return self._bg_pad

    @bg_pad.setter
    def bg_pad(self, value):
        self._bg_pad = value

    @property
    def bg_reserved(self):
        return self._bg_reserved

    @bg_reserved.setter
    def bg_reserved(self, value):
        self._bg_reserved = value

    # ---

    def __str__(self):
        return (
                f"Block number of block bitmap:            {self.bg_block_bitmap}\n"
                f"Block number of inode bitmap:            {self.bg_inode_bitmap}\n"
                f"Block number of first inode table block: {self.bg_inode_table}\n"
                f"Number of free blocks in the group:      {self.bg_free_blocks_count}\n"
                f"Number of free inodes in the group:      {self.bg_free_inodes_count}\n"
                f"Number of directories in the group:      {self.bg_used_dirs_count}\n"
                f"Alignment to word:                       {self.bg_pad}\n"
                f"Nulls to pad out 32 bytes:               {self.bg_reserved}\n"
            )

    def _parse(self):
        self.bg_block_bitmap      = struct.unpack("<I", self._raw_data[0:4])[0]
        self.bg_inode_bitmap      = struct.unpack("<I", self._raw_data[4:8])[0]
        self.bg_inode_table       = struct.unpack("<I", self._raw_data[8:12])[0]
        self.bg_free_blocks_count = struct.unpack("<H", self._raw_data[12:14])[0]
        self.bg_free_inodes_count = struct.unpack("<H", self._raw_data[14:16])[0]
        self.bg_used_dirs_count   = struct.unpack("<H", self._raw_data[16:18])[0]
        self.bg_pad               = struct.unpack("<H", self._raw_data[18:20])[0]
        self.bg_reserved          = struct.unpack("<III", self._raw_data[20:32])


# -----------pruebas------------------------------------------------------------

filename = "prueba_gd.bin"

with open(filename, "wb") as f:
    f.write(struct.pack("<I", 3))
    f.write(struct.pack("<I", 4))
    f.write(struct.pack("<I", 5))
    f.write(struct.pack("<H", 50))
    f.write(struct.pack("<H", 20))
    f.write(struct.pack("<H", 40))
    f.write(struct.pack("<H", 0))
    f.write(struct.pack("<III", 0, 0, 0))

with open(filename, "rb") as f:
    gd_data = f.read()

gd = GroupDescriptor(gd_data)
print(gd)



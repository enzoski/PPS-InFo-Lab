# Cosas a revisar:
#  - ver si saco los atributos referidos a la fragmentacion (y sus g & s) o no.
#  - ver bien si lo del getter deberia ir en el setter (en s_log_block_size).
#  - el tema de que el 'unpack' devuelve tuplas, y tengo que colocar al final '[0]' (en el _parse)
#  - los metodos/operaciones en sí del superbloque (definidas al final)
#  - del pdf de ext2/3, respecto al superbloque, solo me faltaria aplicar lo de 's_state' que dice al final.

import struct

class Superblock:
    """
    Class representing the superblock of an ext2 filesystem.
    """
    def __init__(self, data):
        self._raw_data = data # la lectura en crudo del disco (los 1024 bytes del superbloque).
        # ---
        self._s_inodes_count      = -1
        self._s_blocks_count      = -1
        self._s_r_blocks_count    = -1
        self._s_free_blocks_count = -1
        self._s_free_inodes_count = -1
        self._s_first_data_block  = -1 # always is 1
        self._s_log_block_size    = -1
        self._s_log_frag_size     = -1 # not implemented in ext2
        self._s_blocks_per_group  = -1
        self._s_frags_per_group   = -1 # not implemented in ext2
        self._s_inodes_per_group  = -1
        # --- (hasta acá hice getters y setters, __str__ y el _parser)
        self._s_mtime           = None # for 'times' I will use DateTime objects
        self._s_wtime           = None
        self._s_mnt_count       = -1
        self._s_max_mnt_count   = -1
        self._s_magic           = -1 # maybe init whit b'' (to represent strings)
        self._s_state           = -1
        self._s_errors          = -1
        self._s_minor_rev_level = -1
        self._s_lastcheck       = None
        self._s_checkinterval   = None
        self._s_creator_os      = -1 # maybe init whit b''
        self._s_rev_level       = -1
        self._s_def_resuid      = -1
        self._s_def_resgid      = -1
        # ---
        self._s_first_ino      = -1
        self._s_inode_size     = -1
        self._s_block_group_nr = -1
        # ---
        self._s_feature_compat         = -1
        self._s_feature_incompat       = -1
        self._s_feature_ro_compat      = -1
        self._s_uuid                   = -1
        self._s_volume_name            = b''
        self._s_last_mounted           = b''
        self._s_algorithm_usage_bitmap = -1
        self._s_prealloc_blocks        = -1
        self._s_prealloc_dir_blocks    = -1
        # ---
        self._s_padding1 = -1 # Alignment to word [16 bits]
        self._s_reserved = -1 # Nulls to pad out 1,024 bytes [816 bytes]
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
    def s_inodes_count(self):
        return self._s_inodes_count

    @s_inodes_count.setter
    def s_inodes_count(self, value):
        self._s_inodes_count = value

    @property
    def s_blocks_count(self):
        return self._s_blocks_count

    @s_blocks_count.setter
    def s_blocks_count(self, value):
        self._s_blocks_count = value

    @property
    def s_r_blocks_count(self):
        return self._s_r_blocks_count

    @s_r_blocks_count.setter
    def s_r_blocks_count(self, value):
        self._s_r_blocks_count = value

    @property
    def s_free_blocks_count(self):
        return self._s_free_blocks_count

    @s_free_blocks_count.setter
    def s_free_blocks_count(self, value):
        self._s_free_blocks_count = value

    @property
    def s_free_inodes_count(self):
        return self._s_free_inodes_count

    @s_free_inodes_count.setter
    def s_free_inodes_count(self, value):
        self._s_free_inodes_count = value

    @property # but always is 1
    def s_first_data_block(self):
        return self._s_first_data_block

    @s_first_data_block.setter # but always is 1
    def s_first_data_block(self, value):
        self._s_first_data_block = value

    @property
    def s_log_block_size(self):
        # The s_log_block_size field expresses the block size as a power of 2,
        # using 1,024 bytes as the unit. Thus, 0 denotes 1,024-byte blocks,
        # 1 denotes 2,048-byte blocks, and so on.
        size = 2**(10+self._s_log_block_size)
        return size
        
        # creo que esto estaria bien, o sea, si desde 'afuera' quieren ver el tamaño
        # del bloque, directamente veran el tamaño en bytes.
        # y el verdadero valor del atributo (0, 1 o 2), que solo pueda ser accedido
        # internamente (desde acá, el codigo fuente, haciendo self._s_log_block_size).

    @s_log_block_size.setter
    def s_log_block_size(self, value):
        # Valid block size values are 1024, 2048 and 4096 bytes.
        # (actually, in Linux the block size is limited by the architecture page size)
        if value > 2:
            value = 2
        self._s_log_block_size = value

    @property # not implemented in ext2
    def s_log_frag_size(self):
        return self._s_log_frag_size

    @s_log_frag_size.setter # not implemented in ext2
    def s_log_frag_size(self, value):
        """
        The s_log_frag_size field is currently equal to s_log_block_size,
        since block fragmentation is not yet implemented.
        """
        self._s_log_frag_size = value

    @property
    def s_blocks_per_group(self):
        return self._s_blocks_per_group

    @s_blocks_per_group.setter
    def s_blocks_per_group(self, value):
        self._s_blocks_per_group = value

    @property # not implemented in ext2
    def s_frags_per_group(self):
        return self._s_frags_per_group

    @s_frags_per_group.setter # not implemented in ext2
    def s_frags_per_group(self, value):
        self._s_frags_per_group = value

    @property
    def s_inodes_per_group(self):
        return self._s_inodes_per_group

    @s_inodes_per_group.setter
    def s_inodes_per_group(self, value):
        self._s_inodes_per_group = value

    # ---

    def __str__(self):
        return (
                f"Total number of inodes:        {self.s_inodes_count}\n"
                f"Filesystem size in blocks:     {self.s_blocks_count}\n"
                f"Number of reserved blocks:     {self.s_r_blocks_count}\n"
                f"Free blocks counter:           {self.s_free_blocks_count}\n"
                f"Free inodes counter:           {self.s_free_inodes_count}\n"
                f"Number of first useful block:  {self.s_first_data_block}\n"
                f"Block size:                    {self.s_log_block_size}\n"
                f"Fragment size:                 {self.s_log_frag_size}\n"
                f"Number of blocks per group:    {self.s_blocks_per_group}\n"
                f"Number of fragments per group: {self.s_frags_per_group}\n"
                f"Number of inodes per group:    {self.s_inodes_per_group}\n"
            )

    # All fields in the superblock (as in all other ext2 structures) are stored
    # on the disc in little endian format (<)

    # 'I' represents a 32-bits unsigned int format
    # 'i' represents a 32-bits signed int format

    # El unpack devuelve la representacion decimal de los binarios dados
    # segun el formato especificado.

    def _parse(self):
        self.s_inodes_count      = struct.unpack("<I", self._raw_data[0:4])[0]
        self.s_blocks_count      = struct.unpack("<I", self._raw_data[4:8])[0]
        self.s_r_blocks_count    = struct.unpack("<I", self._raw_data[8:12])[0]
        self.s_free_blocks_count = struct.unpack("<I", self._raw_data[12:16])[0]
        self.s_free_inodes_count = struct.unpack("<I", self._raw_data[16:20])[0]
        self.s_first_data_block  = struct.unpack("<I", self._raw_data[20:24])[0]
        self.s_log_block_size    = struct.unpack("<I", self._raw_data[24:28])[0]
        self.s_log_frag_size     = struct.unpack("<i", self._raw_data[28:32])
        self.s_blocks_per_group  = struct.unpack("<I", self._raw_data[32:36])
        self.s_frags_per_group   = struct.unpack("<I", self._raw_data[36:40])
        self.s_inodes_per_group  = struct.unpack("<I", self._raw_data[40:44])

    # Ext2 Superblock Operations

    def read_inode():
        pass

    def write_inode():
        pass

    def put_inode():
        pass

    def delete_inode():
        pass

    def put_super():
        pass

    def write_super():
        pass

    def statfs():
        pass

    def remount_fs():
        pass
    
    
# -----------pruebas------------------------------------------------------------

filename = "prueba_sb.bin"

with open(filename, "wb") as f:
    f.write(struct.pack("<I", 123)) # escribo los binarios de los decimales
    f.write(struct.pack("<I", 200)) # (el 'pack' devuelve un byte-string de la forma b'')
    f.write(struct.pack("<I", 5))
    f.write(struct.pack("<I", 50))
    f.write(struct.pack("<I", 20))
    f.write(struct.pack("<I", 1))
    f.write(struct.pack("<I", 2))
    f.write(struct.pack("<I", 2))
    f.write(struct.pack("<I", 10))
    f.write(struct.pack("<I", 10))
    f.write(struct.pack("<I", 7))

with open(filename, "rb") as f:
    superblock_data = f.read()

sb = Superblock(superblock_data)
print(sb)
# Cosas a revisar:
#  - en 'file_types' no se bien que numeracion poner, porque segun
#    https://www.nongnu.org/ext2-doc/ext2.html#i-mode y https://wiki.osdev.org/Ext2#Inode_Type_and_Permissions, es otra.
#  - en 'i_mode' faltaria parsear los ultimos 3 bits (y no se bien si hacer el parseo en el setter o en el getter)
#  - fijarme lo de las funciones de inodos (definidas al final de la clase)

import datetime
import struct

# Types of files recognized by Ext2 (used in 'i_mode' field)
file_types = {
    0: 'u', # "Unknown"
    1: '-', # "Regular file"
    2: 'd', # "Directory"
    3: 'c', # "Character device"
    4: 'b', # "Block device"
    5: 'p', # "Named pipe"
    6: 's', # "Socket"
    7: 'l', # "Symbolic link"
}

# Permissions a user has on a file (used in 'i_mode' field)
access_rights = {
    0: '-', # denied  (b: 000)
    1: 'x', # execute (b: 001)
    2: 'w', # write   (b: 010)
    4: 'r', # read    (b: 100)
}

N_FLAGS = 14 # in case in the future I parse more (max 32)

# Flags indicate how ext2 should behave when accessing data pointed to by an inode.
file_flags = {
    # 0x0000: "", # (pensaba usar esto si parseaba solo como string, y no como lista)
    # ---
    0x0001: "secure deletion",
    0x0002: "record for undelete",
    0x0004: "compressed file",
    0x0008: "synchronous updates",
    0x0010: "immutable file",
    0x0020: "append only",
    0x0040: "do not dump/delete file",
    0x0080: "do not update .i_atime",
    # -- Reserved for compression usage --
    0x0100: "dirty (modified)",
    0x0200: "compressed blocks",
    0x0400: "access raw compressed data",
    0x0800: "compression error",
    # ---
    0x1000: "b-tree format directory, hash indexed directory", # both have the same bit
    0x2000: "AFS directory"
    # 0x4000: "journal file data" # reserved for ext3
}

class Inode:
    """
    Class representing an i-node of an ext2 filesystem.
    An inode is associated with a file (or directory), and contains metadata
    about it and pointers to its assigned data blocks (or directory blocks).
    All inodes have the same size: 128 bytes.
    """
    def __init__(self, data):
        self._raw_data = data
        # ---
        self._i_mode        = -1
        self._i_uid         = b'' #por si lo represento como string
        self._i_size        = -1 # Effective length of the file in bytes
        self._i_atime       = None
        self._i_ctime       = None
        self._i_mtime       = None
        self._i_dtime       = None
        self._i_gid         = b''
        self._i_links_count = -1
        self._i_blocks      = -1 # Number of data blocks (in units of 512 bytes: sectors) that have been allocated to the file.
        self._i_flags       = -1
        self._osd1          = -1 # Specific operating system information (4 bytes)
        self._i_block       = [] # Pointers to data blocks (usually 15)
        self._i_generation  = -1
        self._i_file_acl    = -1
        self._i_dir_acl     = -1 # Is not used for regular files
        self._i_faddr       = -1
        self._osd2          = -1 # Specific operating system information (12 bytes)
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
    def i_mode(self):
        """
        File type and access rights (16 bits)
        The top 4 bits for the type, and the bottom 12 bits for the access rights.

        :return: a formatted-string (me basé en como realmente se muestra en Linux)
        """
        f_type   = self._i_mode >> 12
        f_rights = self._i_mode & 0x0fff

        owner_rights = (f_rights & 0b000111000000) >> 6
        group_rights = (f_rights & 0b000000111000) >> 3
        other_rights = (f_rights & 0b000000000111)

        rights = [owner_rights, group_rights, other_rights]
        
        permissions = f"{file_types[f_type]}"

        for r in rights:
            permissions += access_rights[r & 0b100] # cada bit tiene un significado
            permissions += access_rights[r & 0b010]
            permissions += access_rights[r & 0b001]

        return permissions

    @i_mode.setter
    def i_mode(self, value):
        self._i_mode = value

    @property
    def i_uid(self):
        return self._i_uid

    @i_uid.setter
    def i_uid(self, value):
        self._i_uid = value

    @property
    def i_size(self):
        return self._i_size

    @i_size.setter
    def i_size(self, value):
        self._i_size = value

    # ---------------------------------------------------------

    # All ext2 'timestamps' are based on 'POSIX time' (https://en.wikipedia.org/wiki/Unix_time),
    # that is, the number of seconds that have elapsed since the Unix epoch
    # (january 1st 1970, 00:00:00 UTC). All the fields that store dates in ext2,
    # have 4 bytes (unsigned), therefore 2^32 seconds can be stored (it will be enough until the year 2106)
    # Python has a method of the class 'datetime' (datetime module) that converts
    # 'POSIX time' to local time (it converts it to our time zone, not to UTC 0, which comes in handy)
    # See: https://docs.python.org/3/library/datetime.html#datetime.datetime.fromtimestamp

    @property
    def i_atime(self):
        return self._i_atime

    @i_atime.setter
    def i_atime(self, value):
        self._i_atime = datetime.datetime.fromtimestamp(value) # DateTime object

    @property
    def i_ctime(self):
        return self._i_ctime

    @i_ctime.setter
    def i_ctime(self, value):
        self._i_ctime = datetime.datetime.fromtimestamp(value)

    @property
    def i_mtime(self):
        return self._i_mtime

    @i_mtime.setter
    def i_mtime(self, value):
        self._i_mtime = datetime.datetime.fromtimestamp(value)

    @property
    def i_dtime(self):
        return self._i_dtime

    @i_dtime.setter
    def i_dtime(self, value):
        self._i_dtime = datetime.datetime.fromtimestamp(value)

    # ---------------------------------------------------------

    @property
    def i_gid(self):
        return self._i_gid

    @i_gid.setter
    def i_gid(self, value):
        self._i_gid = value

    @property
    def i_links_count(self):
        return self._i_links_count

    @i_links_count.setter
    def i_links_count(self, value):
        self._i_links_count = value

    @property # Number of data blocks (in units of 512 bytes) of the file (Count of disk sectors)
    def i_blocks(self):
        return self._i_blocks

    @i_blocks.setter # Number of data blocks (in units of 512 bytes) of the file (Count of disk sectors)
    def i_blocks(self, value):
        self._i_blocks = value

    # Returns a formated-string with the flags of the file
    @property
    def i_flags(self):
        flag_list = []
        for b in range(0, N_FLAGS):         # parseo (por ahora) solo 'n' bits de los 32 que tiene "_i_flags".
            k = self._i_flags & (0b1 << b)  # voy aplicando mascaras del tipo 1, 10, 100, 1000 ... (bits).
            if k != 0:
                flag_list.append(file_flags[k]) # los bits en 0 representarán un string vacio, y los 1, un flag.
        return ", ".join(flag_list) # esto lo hago para que se vea "mejor" el string.

    @i_flags.setter
    def i_flags(self, value):
        self._i_flags = value
    
    # faltarian los demas getters y setters

    def __str__(self):
        return (
                f"File type and access rights:                  {self.i_mode}\n"
                f"Owner identifier:                             {self.i_uid}\n"
                f"File length in bytes:                         {self.i_size}\n"
                f"Time of last file access:                     {self.i_atime}\n"
                f"Time that inode last changed (file creation): {self.i_ctime}\n"
                f"Time that file contents last changed:         {self.i_mtime}\n"
                f"Time of file deletion:                        {self.i_dtime}\n"
                f"Group identifier:                             {self.i_gid}\n"
                f"Hard links counter:                           {self.i_links_count}\n"
                f"Number of data blocks of the file:            {self.i_blocks} (in units of 512 bytes)\n"
                f"File flags:                                   {self.i_flags}\n"
                # faltarian los demás
            )

    def _parse(self):
        self.i_mode        = struct.unpack("<H", self._raw_data[0:2])[0]
        self.i_uid         = struct.unpack("<H", self._raw_data[2:4])[0]
        self.i_size        = struct.unpack("<I", self._raw_data[4:8])[0]
        self.i_atime       = struct.unpack("<I", self._raw_data[8:12])[0]
        self.i_ctime       = struct.unpack("<I", self._raw_data[12:16])[0]
        self.i_mtime       = struct.unpack("<I", self._raw_data[16:20])[0]
        self.i_dtime       = struct.unpack("<I", self._raw_data[20:24])[0]
        self.i_gid         = struct.unpack("<H", self._raw_data[24:26])[0]
        self.i_links_count = struct.unpack("<H", self._raw_data[26:28])[0]
        self.i_blocks      = struct.unpack("<I", self._raw_data[28:32])[0]
        self.i_flags       = struct.unpack("<I", self._raw_data[32:36])[0]

    # Ext2 Inode Operations

    # only if the inode refers to a regular file
    def ext2_truncate():
        pass

    # only if the inode refers to a directory
    def ext2_create():
        pass

    def ext2_lookup():
        pass

    def ext2_link():
        pass

    def ext2_unlink():
        pass

    def ext2_symlink():
        pass

    def ext2_mkdir():
        pass

    def ext2_rmdir():
        pass

    def ext2_mknod():
        pass

    def ext2_rename():
        pass

    # only if the inode refers to a symbolic link that can be fully stored inside the inode itself
    def ext2_readlink():
        pass

    def ext2_follow_link():
        pass

    # Note: If the inode refers to a character device file, to a block device file,
    #       or to a named pipe, the inode operations do not depend on the filesystem.


# -----------pruebas------------------------------------------------------------

filename = "prueba_inode.bin"

with open(filename, "wb") as f:
    f.write(struct.pack("<H", 8684)) # 0010 0001 1110 1100 (será un directorio donde el dueño puede hacer todo, el grupo solo leer y ejecutar, y 'otros' solo leer)
    f.write(struct.pack("<H", 123))
    f.write(struct.pack("<I", 2**20)) # 1MiB
    f.write(struct.pack("<I", 0))          # esto no nos muestra el 1° de enero de 1970,
    f.write(struct.pack("<I", 1613677029)) # porque 'datetime' en este caso convierte
    f.write(struct.pack("<I", 3600*3))     # el UTC 0 a UTC-3 (zona horaria de Argentina),
    f.write(struct.pack("<I", 0))          # que es lo preferible.
    f.write(struct.pack("<H", 987))
    f.write(struct.pack("<H", 10))
    f.write(struct.pack("<I", 700))
    f.write(struct.pack("<I", 416)) # 00 0001 1010 0000 ("append only", "do not update .i_atime" y "dirty")

with open(filename, "rb") as f:
    inode_data = f.read()

ind = Inode(inode_data)
print(ind)


    
    

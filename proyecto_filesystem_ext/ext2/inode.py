# Cosas a revisar:
#  - en 'file_types' no se bien qué numeracion poner, porque segun
#    https://www.nongnu.org/ext2-doc/ext2.html#i-mode y https://wiki.osdev.org/Ext2#Inode_Type_and_Permissions, es otra.
#    (pero para el directory_entry sí es esta)
#  - no se bien si hacer ciertos parseos en el setter o en el getter (como el caso de 'i_mode' o 'i_flags')
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
    def __init__(self, data=bytes(128),
                 i_mode=None, i_uid=None, i_size=None, i_atime=None, i_ctime=None,
                 i_mtime=None, i_dtime=None, i_gid=None, i_links_count=None,
                 i_blocks=None, i_flags=None, osd1=None, i_block=None, i_generation=None,
                 i_file_acl=None, i_dir_acl=None, i_faddr=None, osd2=None
                 ):

        p_i_mode        = struct.unpack("<H", data[0:2])[0]
        p_i_uid         = struct.unpack("<H", data[2:4])[0]
        p_i_size        = struct.unpack("<I", data[4:8])[0]
        p_i_atime       = struct.unpack("<I", data[8:12])[0]
        p_i_ctime       = struct.unpack("<I", data[12:16])[0]
        p_i_mtime       = struct.unpack("<I", data[16:20])[0]
        p_i_dtime       = struct.unpack("<I", data[20:24])[0]
        p_i_gid         = struct.unpack("<H", data[24:26])[0]
        p_i_links_count = struct.unpack("<H", data[26:28])[0]
        p_i_blocks      = struct.unpack("<I", data[28:32])[0]
        p_i_flags       = struct.unpack("<I", data[32:36])[0]
        p_osd1          = struct.unpack("<I", data[36:40])[0]
        p_i_block       = struct.unpack("<IIIIIIIIIIIIIII", data[40:100])
        p_i_generation  = struct.unpack("<I", data[100:104])[0]
        p_i_file_acl    = struct.unpack("<I", data[104:108])[0]
        p_i_dir_acl     = struct.unpack("<I", data[108:112])[0]
        p_i_faddr       = struct.unpack("<I", data[112:116])[0]
        p_osd2          = struct.unpack("<III", data[116:128])

        self._raw_data = data

        self.i_mode        = i_mode        or p_i_mode
        self.i_uid         = i_uid         or p_i_uid
        self.i_size        = i_size        or p_i_size
        self.i_atime       = i_atime       or p_i_atime
        self.i_ctime       = i_ctime       or p_i_ctime
        self.i_mtime       = i_mtime       or p_i_mtime
        self.i_dtime       = i_dtime       or p_i_dtime
        self.i_gid         = i_gid         or p_i_gid
        self.i_links_count = i_links_count or p_i_links_count
        self.i_blocks      = i_blocks      or p_i_blocks
        self.i_flags       = i_flags       or p_i_flags
        self.osd1          = osd1          or p_osd1
        self.i_block       = i_block       or p_i_block
        self.i_generation  = i_generation  or p_i_generation
        self.i_file_acl    = i_file_acl    or p_i_file_acl
        self.i_dir_acl     = i_dir_acl     or p_i_dir_acl
        self.i_faddr       = i_faddr       or p_i_faddr
        self.osd2          = osd2          or p_osd2

        # 'i_': inode ; 'p_': parsed

    @property
    def raw_data(self):
        """
        Bytes to be parsed.
        (are the 128 bytes corresponding to the structure of an inode)
        """
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

        Returns a formatted-string (me basé en como realmente se muestra en Linux)
        """
        f_type   = self._i_mode >> 12
        permissions = f"{file_types[f_type]}"

        f_rights = self._i_mode & 0x0fff

        # process control bits (I don't really concatenate them in the final string, for now)
        set_process_user_id =  ((f_rights & 0b100000000000) >> 11) == 1
        set_process_group_id = ((f_rights & 0b010000000000) >> 10) == 1
        sticky_bit =           ((f_rights & 0b001000000000) >>  9) == 1

        # access rights bits
        owner_rights = (f_rights & 0b000111000000) >> 6
        group_rights = (f_rights & 0b000000111000) >> 3
        other_rights = (f_rights & 0b000000000111)

        rights = [owner_rights, group_rights, other_rights]

        for r in rights:
            permissions += access_rights[r & 0b100] # cada bit tiene un significado
            permissions += access_rights[r & 0b010]
            permissions += access_rights[r & 0b001]

        # permissions += f"{set_process_user_id} {set_process_group_id} {sticky_bit}"

        return permissions

    @i_mode.setter
    def i_mode(self, value):
        self._i_mode = int(value)

    @property
    def i_uid(self):
        """
        Owner identifier
        """
        return self._i_uid

    @i_uid.setter
    def i_uid(self, value): #quizas lo represente como string
        self._i_uid = value

    @property
    def i_size(self):
        """
        Effective length of the file in bytes
        """
        return self._i_size

    @i_size.setter
    def i_size(self, value):
        self._i_size = int(value)

    # ---------------------------------------------------------

    # All 'timestamps' of files in ext2 are based on 'POSIX time' (https://en.wikipedia.org/wiki/Unix_time),
    # that is, the number of seconds that have elapsed since the Unix epoch
    # (january 1st 1970, 00:00:00 UTC). All the fields that store dates in ext2,
    # have 4 bytes (unsigned), therefore 2^32 seconds can be stored (it will be enough until the year 2106 :-) )
    # Python has a method of the class 'datetime' (datetime module) that converts
    # 'POSIX time' to local time (it converts it to our time zone, not to UTC 0, which comes in handy)
    # See: https://docs.python.org/3/library/datetime.html#datetime.datetime.fromtimestamp
    # So, I will represent the timestamps with DateTime objects.

    @property
    def i_atime(self):
        """
        Last access timestamp
        """
        return self._i_atime

    @i_atime.setter
    def i_atime(self, value):
        self._i_atime = datetime.datetime.fromtimestamp(value) # DateTime object

    @property
    def i_ctime(self):
        """
        Creation timestamp
        """
        return self._i_ctime

    @i_ctime.setter
    def i_ctime(self, value):
        self._i_ctime = datetime.datetime.fromtimestamp(value)

    @property
    def i_mtime(self):
        """
        Last modification timestamp
        """
        return self._i_mtime

    @i_mtime.setter
    def i_mtime(self, value):
        self._i_mtime = datetime.datetime.fromtimestamp(value)

    @property
    def i_dtime(self):
        """
        Deletion timestamp        
        """
        return self._i_dtime

    @i_dtime.setter
    def i_dtime(self, value):
        self._i_dtime = datetime.datetime.fromtimestamp(value)

    # ---------------------------------------------------------

    @property
    def i_gid(self):
        """
        Group identifier
        """
        return self._i_gid

    @i_gid.setter
    def i_gid(self, value):
        self._i_gid = value

    @property
    def i_links_count(self):
        """
        Hard links counter
        """
        return self._i_links_count

    @i_links_count.setter
    def i_links_count(self, value):
        self._i_links_count = int(value)

    @property
    def i_blocks(self):
        """
        Number of data blocks (in units of 512 bytes) that have been allocated
        to the file (count of disk sectors).
        """
        return self._i_blocks

    @i_blocks.setter
    def i_blocks(self, value):
        self._i_blocks = int(value)

    @property
    def i_flags(self):
        """
        Returns a formated-string with the flags of the file
        """
        flag_list = []
        for b in range(0, N_FLAGS):         # parseo (por ahora) solo 'n' bits de los 32 que tiene "_i_flags".
            k = self._i_flags & (0b1 << b)  # voy aplicando mascaras del tipo 1, 10, 100, 1000 ... (bits).
            if k != 0:
                flag_list.append(file_flags[k]) # los bits en 0 representarán un string vacio, y los 1, un flag.
        return ", ".join(flag_list) # esto lo hago para que se vea "mejor" el string.
        #no se si se podria hacer esto con una lista por comprension ("List Comprehension").

    @i_flags.setter
    def i_flags(self, value):
        self._i_flags = int(value)

    @property
    def osd1(self):
        """
        Specific operating system information (4 bytes)
        """
        return self._osd1

    @osd1.setter
    def osd1(self, value):
        self._osd1 = value

    @property
    def i_block(self):
        """
        Pointers to data blocks (12 direct and 3 indirect)
        (I will store them in a list)
        """
        return self._i_block

    @i_block.setter
    def i_block(self, value):
        self._i_block = list(value)

    @property
    def i_generation(self):
        """
        File version (used when the file is accessed by a network filesystem)
        """
        return self._i_generation

    @i_generation.setter
    def i_generation(self, value):
        self._i_generation = value

    @property
    def i_file_acl(self):
        """
        File access control list
        """
        return self._i_file_acl

    @i_file_acl.setter
    def i_file_acl(self, value):
        self._i_file_acl = value

    @property
    def i_dir_acl(self):
        """
        Directory access control list (is not used for regular files)
        """
        return self._i_dir_acl

    @i_dir_acl.setter
    def i_dir_acl(self, value):
        self._i_dir_acl = value

    @property
    def i_faddr(self):
        """
        Fragment address
        """
        return self._i_faddr

    @i_faddr.setter
    def i_faddr(self, value):
        self._i_faddr = value

    @property
    def osd2(self):
        """
        Specific operating system information (12 bytes)
        """
        return self._osd2

    @osd2.setter
    def osd2(self, value):
        self._osd2 = value

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
                # faltarian los demás (si es que decido querer mostrarlos)
            )

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
    f.write(struct.pack("<I", 0))
    f.write(struct.pack("<IIIIIIIIIIIIIII", 0, 0, 0, 1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 5, 0))
    f.write(struct.pack("<I", 0))
    f.write(struct.pack("<I", 0))
    f.write(struct.pack("<I", 0))
    f.write(struct.pack("<I", 0))
    f.write(struct.pack("<III", 0, 0, 0))

with open(filename, "rb") as f:
    inode_data = f.read()

ind = Inode(inode_data)
print(ind)

# queria ver si se veian los True y False de los bits de control.
#ind.i_mode = 0b0010111111101100
#print(ind.i_mode)

# queria ver como se verían los punteros a los bloques de datos.
print(ind.i_block)
print(type(ind.i_block))

print("")

inode_2 = Inode(i_mode=0x1fff, i_atime=1614745834, i_flags=0b1000000000000)
print(inode_2)

inode_3 = Inode()
print(inode_3)

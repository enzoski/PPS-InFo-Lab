# Creo que ya estaria completa esta clase

import struct

# Types of files recognized by Ext2
file_types = {
    0: "Unknown",
    1: "Regular file",
    2: "Directory",
    3: "Character device",
    4: "Block device",
    5: "Named pipe",
    6: "Socket",
    7: "Symbolic link"
}

class DirectoryEntry:
    """
    Class representing a Directory Entry of an ext2 filesystem.
    (are the records stored in the directory blocks pointed to by directory inodes)

    The structure has a variable length, since the 'name' field is a
    variable length array of up to 255 characters. Moreover, the length of a
    directory entry is always a multiple of 4 and, therefore, null characters ('\0')
    are added for padding at the end of the filename, if necessary.
    (but the 'name_len' field stores the actual file name length)
    """
    def __init__(self, data):
        self._raw_data = data
        # ---
        self._inode     = -1
        self._rec_len   = -1 # in bytes
        self._name_len  = -1
        self._file_type = -1
        self._name      = b'' # up to 255 chars
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
    def inode(self):
        return self._inode

    @inode.setter
    def inode(self, value):
        self._inode = value

    @property
    def rec_len(self):
        return self._rec_len

    @rec_len.setter
    def rec_len(self, value):
        self._rec_len = value

    @property
    def name_len(self):
        return self._name_len

    @name_len.setter
    def name_len(self, value):
        self._name_len = value

    # Returns a string corresponding to the file type.
    @property
    def file_type(self):
        return file_types[self._file_type]

    @file_type.setter
    def file_type(self, value):
        self._file_type = value

    @property
    def name(self):
        return self._name

    # Truncate the byte-string to the first occurrence of '\0', if it exists ('\0' == null character == 0x00 == '\x00')
    @name.setter
    def name(self, value):
        null_char_index = value.find(b'\0')
        if null_char_index != -1:
            self._name = value[0:null_char_index]
        else:
            self._name = value

    # ---

    def __str__(self):
        return (
                f"Inode number:           {self.inode}\n"
                f"Directory entry length: {self.rec_len}\n"
                f"Filename length:        {self.name_len}\n"
                f"File type:              {self.file_type}\n"
                f"Filename:               {self.name.decode('latin1')}\n" # uso esta codificacion u otra???
            )

    def _parse(self):
        self.inode     = struct.unpack("<I", self._raw_data[0:4])[0]
        self.rec_len   = struct.unpack("<H", self._raw_data[4:6])[0]
        self.name_len  = struct.unpack("<B", self._raw_data[6:7])[0]
        self.file_type = struct.unpack("<B", self._raw_data[7:8])[0]
        # I directly assign the raw binaries to it and then in the '__str__' I make it a 'decode'.
        self.name      = self._raw_data[8:self.rec_len] # variable length

        # esta seria otra forma de hacer el 'unpack'
        # self.inode, self.rec_len, self.name_len, self.file_type = struct.unpack("<IHBB", self._raw_data[0:8])


# -----------pruebas------------------------------------------------------------

filename = "prueba_dentry.bin"

with open(filename, "wb") as f:
    f.write(struct.pack("<I", 67))
    f.write(struct.pack("<H", 12))
    f.write(struct.pack("<B", 3))
    f.write(struct.pack("<B", 2))
    f.write(b'usr\0')

with open(filename, "rb") as f:
    dentry_data = f.read()

de = DirectoryEntry(dentry_data)
print(de)
    
    
    
    
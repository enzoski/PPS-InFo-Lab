# Cosas a revisar:
#  - Cuando calculo block_group_count, redondeo al entero superior (*) porque al parecer el espacio libre del final de la particion
#    queda asignado a un 'block group' más, pero que obviamente no respeta tener 'superblock.s_blocks_per_group' bloques, sino menos.
#  - Quizas todos los calculos referidos a la cantidad de grupos de bloques, deberian ir en la clase Superblock.
#  - No puedo leer de una la tabla de descriptores de grupo, ya que si el tamaño de bloque son 4k, hay 2048 bytes libres y recien ahi
#    empieza la tabla (generalizando, la tabla comienza en el BLOQUE SIGUIENTE al del superbloque).
#  - Cuando hago un seek muy grande, me da error.
#  - Quizás haya que mejorar la forma de verificar el tipo de archivo (en 'Ext2.open()')
#  - Falta el manejo de archivos de datos como tal, o sea, buscar un archivo y leer sus binarios
#    (quizas sea una estructura parecida a la de Directory)
#  - Tengo que ver bien lo del path que le paso a Ext2.open(), porque creo que se asume que debemos poner el 'nombre'
#    de la particion (que representaria al directorio raiz '/') seguido de lo que queremos abrir (pero incluso podemos poner cualquier
#    cosa creo o directamente nada, tengo que testear bien eso).
#    En Windows sería por ejemplo C:\..., pero tengo que ver como es el path cuando nosotros le damos un nombre/etiqueta
#    al volumen/particion (por ejemplo, al formatear un pendrive). Además tengo que ver bien como se forma el path en Linux
#    en base al nombre, ya que acá lo voy a hacer respetando el formato Linux.
#  - Estaria bueno agregar metodos como 'read_block(block_number)', 'read_inode(inode_number)', etc...

# NOTA: siempre que se habla de un "número de bloque" o "número de inodo", se habla de manera absoluta,
#       es decir, ese número de bloque/inodo en la totalidad del filesystem (y si es relativo a algo,
#       estará especificado). Los bloques se cuentan desde el area de boot hasta el final de la particion,
#       y los inodos se cuentan por cada entrada de la tabla de inodos de cada grupo de bloques.

import superblock, group_descriptor, inode, directory_entry
from math import ceil

DISK_SECTOR_SIZE        = 512

SB_STRUCT_SIZE          = 1024
GD_STRUCT_SIZE          = 32
INODE_STRUCT_SIZE       = 128
DENTRY_STRUCT_BASE_SIZE = 8

ENCODING = 'latin-1'

class Directory:
    """
    Un directorio es realmente un inodo cuyos bloques de datos que apunta, contienen entradas de directorios.
    Lo que hago con esta clase, es parsear esos bloques.
    """
    def __init__(self, filesystem, inode_obj, name, parent=None):
        
        self.filesystem = filesystem
        self.inode_obj = inode_obj
        self.name = name

        self.files = []

        if parent is None:
            self.path = self.name.decode(ENCODING) # para la raiz, 'name' va a ser el 'volume_name'.
        else:
            self.path = parent.path + '/' + self.name.decode(ENCODING)

        self._parse()

    def __repr__(self):
        # a bit of a hack (X or Y) in case we want to show the root directory,
        # and it doesn't have a certain name (volume_name == "" (empty))
        return f"< Directory {self.path or '/'} >"

    def __str__(self):
        ret = f"< Directory {self.path or '/'} >\n"
        ret += "----------FILES----------\n"
        for f in self.files:
            ret += f"{f.name.decode(ENCODING)} ({f.file_type})\n"
        ret += "-------------------------\n"
        return ret

    def _read_dentries(self, block_number, block_size):

        raw_block = self.filesystem._read_record(block_number, block_size)
        offset = 0
        # let's read the directory entries (the last valid entry points to the end of the block)
        while offset < block_size:
            dx = offset + DENTRY_STRUCT_BASE_SIZE
            file = directory_entry.DirectoryEntry(raw_block[offset:dx])
            file.name = raw_block[dx:dx+file.name_len]
            if file.inode != 0:
                # This happens only if the first file is deleted;
                # all other deleted file entries will be skipped due to
                # a proper rec_len of the previous entry. (inode == 0 -> file deleted)
                self.files.append(file)
            offset += file.rec_len

    def _read_indirect_1_dentries(self, block_number, block_size):

        raw_indirect_1_block = self.filesystem._read_record(block_number, block_size)
        indirect_1_block = [pointer[0] for pointer in struct.iter_unpack("<I", raw_indirect_1_block) if pointer[0] != 0]
        # There may be unallocated blocks yet (pointers to 0), so we will only keep those pointers that do not equal to null (0).
        for p in indirect_1_block:
            self._read_dentries(p, block_size)

    def _read_indirect_2_dentries(self, block_number, block_size):
        raw_indirect_2_block = self.filesystem._read_record(block_number, block_size)
        indirect_2_block = [pointer[0] for pointer in struct.iter_unpack("<I", raw_indirect_2_block) if pointer[0] != 0]
        for p in indirect_2_block:
            self._read_indirect_1_dentries(p, block_size)

    def _read_indirect_3_dentries(self, block_number, block_size):
        raw_indirect_3_block = self.filesystem._read_record(block_number, block_size)
        # how much power in a single line of code! it's beautiful, Python at its best!
        indirect_3_block = [pointer[0] for pointer in struct.iter_unpack("<I", raw_indirect_3_block) if pointer[0] != 0]
        for p in indirect_3_block:
            self._read_indirect_2_dentries(p, block_size)


    def _parse(self):

        block_size = self.filesystem.superblock.s_log_block_size
        directory_blocks = (self.inode_obj.i_blocks*512) / block_size

        i = 0

        # let's read the direct blocks
        while i != directory_blocks and i < 12:
            block_number = self.inode_obj.i_block[i]
            self._read_dentries(block_number, block_size)
            i += 1
        
        # and now the indirect blocks
        while i != directory_blocks and i < 13:
            block_number = self.inode_obj.i_block[i]
            self._read_indirect_1_dentries(block_number, block_size)
            i += 1

        while i != directory_blocks and i < 14:
            block_number = self.inode_obj.i_block[i]
            self._read_indirect_2_dentries(block_number, block_size)
            i += 1

        while i != directory_blocks and i < 15:
            block_number = self.inode_obj.i_block[i]
            self._read_indirect_3_dentries(block_number, block_size)
            i += 1


    # un extra, para curosear.
    def show_dentries(self):
        ret = f"< Directory {self.path or '/'} >\n"
        ret += "----DIRECTORY-ENTRIES----\n"
        for f in self.files:
            ret += f"{str(f)}\n"
        ret += "-------------------------\n"
        return ret

    # un extra, para curosear.
    def show_inode(self):
        ret = f"< Directory {self.path or '/'} >\n"
        ret += "----ASSOCIATED INODE-----\n"
        ret += f"{str(self.inode_obj)}"
        ret += "-------------------------\n"
        return ret


class FileHandle:
    """docstring for FileHandle"""
    def __init__(self, filesystem, inode_obj, name=b'', parent=None):
        
        self.filesystem = filesystem
        self.inode_obj = inode_obj
        self.name = name
        

class Ext2:
    """
    Class that handles an ext2 filesystem.

    :param path: It is the way to access the storage device.
        On Windows, it is in the format: r"\\.\PhysicalDriveX", and on Linux "/dev/sdX".
    :param base_address: It is the offset (byte number), inside the device, where
        the partition (with an ext2 fs) that we want to analyze, begins.
    """
    def __init__(self, path, base_address):
        """
        The storage device opens.
        The byte pointer is positioned at the beginning of the desired partition.
        And the boot area, the superblock (original), the group descriptor table
        (original) and the root inode, are read.
        """
        self.path = path
        self.base_address = base_address

        self.handle = open(path, "rb") # read-only for now (por seguridad, deberia poner este atributo como privado mediante properties)
        self.handle.seek(self.base_address)

        # the first 2 sectors of the partition correspond to the boot area (are unused by the ext2 filesystem).
        self.boot_area = self.handle.read(DISK_SECTOR_SIZE*2)
        # the next 1024 bytes correspond to the original superblock (we are already within block group 0).
        self.superblock = superblock.Superblock(self.handle.read(SB_STRUCT_SIZE))
        # and then there will be as many group descriptors as there are block groups in the filesystem.
        useful_blocks = self.superblock.s_blocks_count - self.superblock.s_first_data_block
        block_group_count = ceil(useful_blocks / self.superblock.s_blocks_per_group) # (*)
        self.group_descriptors = [group_descriptor.GroupDescriptor(self.handle.read(GD_STRUCT_SIZE)) for i in range(block_group_count)]

        # The root directory always corresponds to inode No. 2 (inode [1]), which belongs to block group No. 1 (bg [0])
        it_block = self.group_descriptors[0].bg_inode_table
        raw_root_inode_entry = self._read_record(it_block, INODE_STRUCT_SIZE, offset=INODE_STRUCT_SIZE)
        root_inode = inode.Inode(raw_root_inode_entry)
        self.root = Directory(self, root_inode, name=self.superblock.s_volume_name)

    def __repr__(self):
        return f"< ext2 @ {self.base_address} of {self.path}>\n"

    def __str__(self):
        # NOTE: The filesystem is divided into blocks as follows:
        #       boot_area + (total_blocks - 1 // blocks_per_group)*blocks_per_group + (total_blocks-1 % blocks_per_group)
        #       OR if block_size > 1K:
        #       (total_blocks // blocks_per_group)*blocks_per_group + (total_blocks % blocks_per_group)
        useful_blocks = self.superblock.s_blocks_count - self.superblock.s_first_data_block
        last_block_group_len = useful_blocks % self.superblock.s_blocks_per_group
        aux = f" (the last one has {last_block_group_len} blocks assigned)"
        if last_block_group_len == 0:
            # all block groups have fitted perfectly
            aux = ""

        return (
                f"< ext2 Filesystem:\n"
                f"{'Number of block groups:':49}{len(self.group_descriptors)}{aux}\n"
                f"{self.superblock}>\n"
            )

    def _read_record(self, block_number, length, offset=0):
        """
        Method that reads a certain amount of bytes (length) from a given block
        of the filesystem (block_number), starting from an offset (by default 0).
        """
        block_size = self.superblock.s_log_block_size
        address = block_number*block_size
        self.handle.seek(self.base_address)
        self.handle.read(address + offset) # por alguna razon, el 'seek' me tira error, entonces lo cambié por 'read'.
        return self.handle.read(length)

    def open(self, path):
        """
        Method that "opens" a file or directory on the filesystem.
        It returns an object of type "Directory" or "FileHandle" depending on
        what we are looking for (according to what we specify in the 'path',
        which must be absolute!).
        With the returned object, we can make use of its methods to see
        the content of a directory, or the data of a file, as appropriate
        (among other things).
        """
        path = path.encode(ENCODING) # ext2 is case sensitive, so I handle the path as it comes.
        parts = path.split(b'/')[1:] # descomponemos el path en una lista con los nombres de directorios/archivo.
        obj = self.root # arrancamos siempre desde el directorio raiz.
        if path != b'/': # por si queremos abrir solo la raiz
            for name in parts: # nos iremos adentrando directorio a directorio hasta llegar al archivo o directorio buscado.
                try:
                    # hacemos un diccionario <nombre:inodo> a partir de los directory entry del directorio.
                    files = {f.name:f.inode for f in obj.files}
                except AttributeError:
                    # por si pasa algo así: /home/archivo.txt/fotos
                    # o sea, que haya un nombre de archivo en el medio del path, cuando solo puede estar al final
                    # (todo lo demas deben ser directorios)
                    raise FileNotFoundError(f"{obj.path} is not a Directory!") # we will see this exception by console.
                if name in files: # verificamos que el nombre de directorio/archivo buscado esté en un directory entry del directorio padre.
                    # Locating the inode
                    inode_number = files[name]
                    block_group = (inode_number - 1) // self.superblock.s_inodes_per_group
                    first_inode_table_block = self.group_descriptors[block_group].bg_inode_table
                    local_inode_index = (inode_number - 1) % self.superblock.s_inodes_per_group
                    # and now we read it
                    raw_inode = self._read_record(first_inode_table_block, INODE_STRUCT_SIZE, offset=local_inode_index*INODE_STRUCT_SIZE)
                    inode_obj = inode.Inode(raw_inode)
                    # and we instantiate the directory or file as of the inode that represents it.
                    if inode_obj.i_mode[0] == 'd': # Maybe this way of checking the file type needs to be improved.
                        obj = Directory(self, inode_obj, name, parent=obj)
                    else:
                        obj = FileHandle(self, inode_obj, name, parent=obj) # si llegamos acá antes de terminar el 'for', arriba se lanzará la excepcion 'AttributeError'.
                else:
                    raise FileNotFoundError(f"No such file or directory {obj.path}/{name.decode(ENCODING)}")
            
        return obj

    # No se si sea el nombre de método adecuado, pero queria poner acá el 'close'.
    def unmount(self):
        self.handle.close()
        return True

        
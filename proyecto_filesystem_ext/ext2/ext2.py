# Cosas a revisar:
#  - Cuando calculo block_group_count, redondeo al entero superior (*) porque al parecer el espacio libre del final de la particion
#    queda asignado a un 'block group' más, pero que obviamente no respeta tener 'superblock.s_blocks_per_group' bloques, sino menos.
#    (igualmente esto es más a modo de comentario, así como lo hice funciona como quería, no creo que haya que cambiar la lógica)
#  - Quizas todos los calculos referidos a la cantidad de grupos de bloques, deberian ir en la clase Superblock
#    (por lo que hago en el __str__ y en las 2 lineas previas a armar la lista de descriptores de grupos).
#  - Cuando hago un seek o un read muy grande, me da error (onda, moverse de a gigas). IMPORTANTE.
#  - Quizás haya que mejorar la forma de verificar el tipo de archivo (en 'Ext2.open()')
#  - Falta el manejo de archivos de datos como tal, o sea, buscar un archivo y leer sus binarios
#    (quizas sea una estructura parecida a la de Directory)
#  - Tengo que ver bien lo del path que le paso a Ext2.open(), porque creo que se asume que debemos poner el 'nombre'
#    de la particion (que representaria al directorio raiz '/') seguido de lo que queremos abrir (pero incluso podemos poner cualquier
#    cosa creo o directamente nada, tengo que testear bien eso).
#    En Windows sería por ejemplo C:\..., pero tengo que ver como es el path cuando nosotros le damos un nombre/etiqueta
#    al volumen/particion (por ejemplo, al formatear un pendrive). Además tengo que ver bien como se forma el path en Linux
#    en base al nombre, ya que acá lo voy a hacer respetando el formato Linux.
#  - Podría implementar los métodos que dejé definidos en los otros archivos (en las clases de las estructuras).

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

    def _read_dentries(self, block_number):
        """
        Internal method that reads and parses the directory entries of a block
        in the filesystem. It adds DirectoryEntry objects to the list of files
        of the current Directory object.
        """

        raw_block = self.filesystem.read_block(block_number)

        offset = 0 # this variable will store the starting address of each directory entry
        block_size = self.filesystem.superblock.s_log_block_size
        # let's read and parse the directory entries (the last valid entry points to the end of the block)
        while offset < block_size:
            dx = offset + DENTRY_STRUCT_BASE_SIZE
            file = directory_entry.DirectoryEntry(raw_block[offset:dx]) # we parse the first 8 bytes (the constant part of the dentry).
            file.name = raw_block[dx:dx+file.name_len] # and now the rest, corresponding to the name (the variable part).
            if file.inode != 0:
                # This happens only if the first file is deleted;
                # all other deleted file entries will be skipped due to
                # a proper rec_len of the previous entry. (inode == 0 -> file deleted)
                self.files.append(file)
            offset += file.rec_len

    def _read_indirect_1_dentries(self, block_number):
        raw_indirect_1_block = self.filesystem.read_block(block_number)
        indirect_1_block = [pointer[0] for pointer in struct.iter_unpack("<I", raw_indirect_1_block) if pointer[0] != 0]
        # There may be unallocated blocks yet (pointers to 0), so we will only keep those pointers that do not equal to null (0).
        for p in indirect_1_block:
            self._read_dentries(p) # we read the directory entries contained in the block pointed to by the pointer 'p'.

    def _read_indirect_2_dentries(self, block_number):
        raw_indirect_2_block = self.filesystem.read_block(block_number)
        indirect_2_block = [pointer[0] for pointer in struct.iter_unpack("<I", raw_indirect_2_block) if pointer[0] != 0]
        for p in indirect_2_block:
            self._read_indirect_1_dentries(p)

    def _read_indirect_3_dentries(self, block_number):
        raw_indirect_3_block = self.filesystem.read_block(block_number)
        # how much power in a single line of code! it's beautiful, Python at its best!
        indirect_3_block = [pointer[0] for pointer in struct.iter_unpack("<I", raw_indirect_3_block) if pointer[0] != 0]
        for p in indirect_3_block:
            self._read_indirect_2_dentries(p)


    def _parse(self):

        block_size = self.filesystem.superblock.s_log_block_size
        directory_blocks = (self.inode_obj.i_blocks*512) / block_size

        i = 0

        # let's read the direct blocks
        while i != directory_blocks and i < 12:
            block_number = self.inode_obj.i_block[i]
            self._read_dentries(block_number)
            i += 1
        
        # and now the indirect blocks
        while i != directory_blocks and i < 13:
            block_number = self.inode_obj.i_block[i]
            self._read_indirect_1_dentries(block_number)
            i += 1

        while i != directory_blocks and i < 14:
            block_number = self.inode_obj.i_block[i]
            self._read_indirect_2_dentries(block_number)
            i += 1

        while i != directory_blocks and i < 15:
            block_number = self.inode_obj.i_block[i]
            self._read_indirect_3_dentries(block_number)
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
    """
    Clase que maneja a un archivo de datos, dado su inodo que lo representa.
    Contará con las operaciones básicas de un archivo: read, write, seek, close...
    (el 'open' estaría implementado en la clase Ext2, ya que justamente nos devuelve
    este objeto FileHandle, como cuando hacemos un verdadero open en Python u otro lenguaje).
    Por el momento, solo estará implementado el 'read'.
    """
    def __init__(self, filesystem, inode_obj, name=b'', parent=None):
        
        self.filesystem = filesystem
        self.inode_obj = inode_obj
        self.name = name

        if parent is None:
            self.path = self.name.decode(ENCODING) # para la raiz, 'name' va a ser el 'volume_name'.
        else:
            self.path = parent.path + '/' + self.name.decode(ENCODING)

        self.closed = False

        # Siempre iremos manteniendo los bytes del archivo en un 'buffer',
        # de a 1 bloque por vez (comenzando con su primer bloque)
        self._buffer      = self.filesystem.read_block(self.inode_obj.i_block[0])
        self._buffer_pos  = 0 # 0 <= pos < buffer_size
        self._buffer_size = self.filesystem.superblock.s_log_block_size

        # Guardamos el número del puntero del ultimo bloque 'buffereado',
        # para que en la siguiente lectura del archivo, sepamos donde nos quedamos.
        self._current_block_pointer = 0

        # position in the file (pointer to the byte number), .tell() returns this
        self._file_pos = 0 # 0 <= pos < self.inode_obj.i_size

    def __repr__(self):
        return f"< FileHandle for {self.path}>"
    
    def __str__(self):
        return self.__repr__()

    def close(self):
        """
        Closes the file.
        """
        self.closed = True

    def read(self, size=-1):
        """
        Método que lee una cierta cantidad de bytes (size) del archivo al que
        hace referencia el objeto FileHandle (siempre y cuando el archivo esté 'abierto').
        Si se omite el argumento 'size', se leerá la totalidad del archivo
        (o lo que reste de él segun su posicion del puntero).
        """
        if self.closed == True:
            raise ValueError("I/O operation on closed file.")

        if size < 0: # indicaría que queremos leer lo que reste del archivo.
            size = self.inode_obj.i_size - self._file_pos # file length in bytes - current position of the file pointer.

        ret = [] # acá iremos guardando las cadenas de bytes que leamos del buffer, y al final uniremos todo.

        # let's read the direct blocks
        while size > (self._buffer_size - self._buffer_pos) and self._current_block_pointer+1 < 12:
            ret.append(self._buffer[self._buffer_pos:]) # acá arrancamos de 'buffer_pos' por si primero se leyó poquito (y no se entró a este while), y luego mucho (y sí se entró).
            size           -= self._buffer_size - self._buffer_pos # vamos restando de 'size' la cantidad de bytes que ya leimos.
            self._file_pos += self._buffer_size - self._buffer_pos # vamos avanzando el puntero del archivo a medida que leemos.
            self._buffer_pos = 0 # como consumimos la totalidad del buffer, seteamos su posicion en 0.
            next_block_pointer = self._current_block_pointer + 1
            next_block_number = self.inode_obj.i_block[next_block_pointer]
            if next_block_number == 0: # creeria que no hay huecos entre bloques asignados, por ende cuando llegue al primer bloque sin asignar aun (puntero nulo), significa fin de archivo.
                break
            self._buffer = self.filesystem.read_block(next_block_number) # leemos el siguiente bloque de datos y lo guardamos en el buffer.
            self._current_block_pointer = next_block_pointer

        # cuando lleguemos acá, querrá decir que 'size' es más chico que el tamaño del buffer (bloque)
        span = min(self.inode_obj.i_size - self._file_pos, size) # esto lo hacemos para evitar leer del buffer mas bytes que los restantes del archivo.
        ret.append(self._buffer[self._buffer_pos:self._buffer_pos+span]) # leemos los x ('span') bytes del buffer
        self._buffer_pos += span # y movemos los punteros/posiciones tanto del buffer como del archivo.
        self._file_pos   += span # (no habrá problemas de desbordamientos porque span siempre será mas chico que el tamaño de bloque)
        return b"".join(ret)

            # Tengo que ver qué hacer si se intenta leer más bytes que los que tiene el archivo. HECHO
            # (se resuelve checkeando dentro del while que el siguiente bloque apuntado no sea 0/nulo)
            # (y luego cuando salga del while, o directamente no entre, nos aseguramos de leer lo justo y necesario, con la variable 'span')
            # (y realmente, Python no tira error, sino que lee hasta donde haya bytes y listo. Y si luego seguimos queriendo leer, nos devuelve '' vacío)
            
            # Y tambien qué pasaria si voy leyendo de a pocos bytes, cosa de no entrar en los while,
            # y llega un momento que me paso del tamaño de bloque, ya que necesitaria leer el siguiente. HECHO
            # (esto se soluciona con el chekeo del while '(self._buffer_size - self._buffer_pos)',
            # gracias a la posicion del puntero sabremos cuándo será necesario pasar al siguiente bloque,
            # y en esos casos se entra al while, ya que 'size' sí será mayor que esa diferencia)

            # Tendria que revisar qué pasa si ya lei la totalidad del archivo, y quiero leer una cantidad tan grande que
            # entre al while, porque ahí haría un append de más.

    def tell(self):
        """
        Returns the current position of the file pointer.
        """
        return self._file_pos

        

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
        self.handle.seek(self.base_address + self.superblock.s_log_block_size * (self.superblock.s_first_data_block + 1)) # the group descriptor table begins at the block following the superblock
        useful_blocks = self.superblock.s_blocks_count - self.superblock.s_first_data_block # if block_size=1K, the first block doesn't belong to the first block_group
        block_group_count = ceil(useful_blocks / self.superblock.s_blocks_per_group) # (*)
        self.group_descriptors = [group_descriptor.GroupDescriptor(self.handle.read(GD_STRUCT_SIZE)) for i in range(block_group_count)]

        # The root directory always corresponds to inode No. 2 (inode_table[1]), which belongs to block group No. 1 (bg[0]).
        # (note: I don't use the 'read_inode' method cause for me in this case it is more descriptive to see the read_record's arguments)
        inode_table_block = self.group_descriptors[0].bg_inode_table
        raw_root_inode_entry = self.read_record(inode_table_block, INODE_STRUCT_SIZE, offset=INODE_STRUCT_SIZE)
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

    def read_record(self, block_number, length, offset=0):
        """
        Method that reads a certain amount of bytes (length) from a given block
        of the filesystem (block_number), starting from an offset (by default 0).
        """
        block_size = self.superblock.s_log_block_size
        address = block_number*block_size
        self.handle.seek(self.base_address)
        self.handle.read(address + offset) # por alguna razon, el 'seek' me tira error, entonces lo cambié por 'read'.
        return self.handle.read(length)    # ¿¿ PODRÍA HACER UN for in range(block_number) COSA DE IR HACIENDO SEEK'S DE A 1 BLOQUE ??

    def read_block(self, block_number):
        """
        Method that reads a block from the filesystem (block_number >= 0).
        """
        block_size = self.superblock.s_log_block_size
        address = block_number*block_size
        self.handle.seek(self.base_address)
        self.handle.read(address) # por alguna razon, el 'seek' me tira error, entonces lo cambié por 'read'.
        raw_block = self.handle.read(block_size)
        return raw_block

    def read_inode(self, inode_number):
        """
        Method that reads an inode from the filesystem (inode_number >= 1).
        Attention! Unlike block numbering, the inodes start to be numbered from 1,
        since inode number 0 indicates 'null inode' (so the first entry in
        the inode table 'inode_table[0]', corresponds to inode 1 and not inode 0).
        """
        if inode_number < 1:
            raise TypeError("the inode number must be >= 1 !")
        # locating the inode
        block_group = (inode_number - 1) // self.superblock.s_inodes_per_group
        first_inode_table_block = self.group_descriptors[block_group].bg_inode_table
        local_inode_index = (inode_number - 1) % self.superblock.s_inodes_per_group
        # and now we read it
        raw_inode = self.read_record(first_inode_table_block, INODE_STRUCT_SIZE, offset=local_inode_index*INODE_STRUCT_SIZE)
        return raw_inode


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
                    # We locate, read and parse the inode
                    inode_number = files[name]
                    raw_inode = self.read_inode(inode_number)
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

        
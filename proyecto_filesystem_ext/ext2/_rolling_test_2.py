import ext2

# Abrimos un dispositivo de almacenamiento y nos posicionamos al inicio de una particion
# (el offset nos lo daría la clase MBR o GPT de haruspex, yo lo sé porque lo vi en WinHex)
# A continuacion se lee el area de boot, el superbloque, la tabla de descriptores de grupos y el inodo raiz.
particion_pendrive = ext2.Ext2(r"\\.\PhysicalDrive1", 2048*512)

print(particion_pendrive) # mostraremos parte del superbloque

for gd in particion_pendrive.group_descriptors[0:3]: # mostramos los 3 primeros descriptores de grupos
    print(gd)

print(particion_pendrive.group_descriptors[-1]) # mostramos el ultimo descriptor de grupo

directorio_raiz = particion_pendrive.open("/")
print(directorio_raiz) # archivos del directorio raiz
print(directorio_raiz.show_dentries())
print(directorio_raiz.show_inode())

print(particion_pendrive.read_block(1))
print("")
print(particion_pendrive.read_inode(2))

particion_pendrive.unmount()

# para ver que tire error de 'archivo cerrado'
# particion_pendrive.handle.tell()
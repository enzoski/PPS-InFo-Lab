"""
Testing the handling of a real Ext2 filesystem.
"""

import ext2

DISK_SECTOR_SIZE = 512

# We open a storage device (administrator privileges are required) and position it
# at the start of a partition. The offset (sector number where the partition begins)
# would be given by the class MBR or GPT of haruspex [https://github.com/bconstanzo/haruspex],
# or seeing it in some hex/disk editor like WinHex or HxD ('2048' in this case).
# And the boot area, the superblock, the group descriptor table and the root inode are read.
pendrive_partition = ext2.Ext2(r"\\.\PhysicalDrive1", 2048 * DISK_SECTOR_SIZE)

print(pendrive_partition) # we will show part of the superblock

for gd in pendrive_partition.group_descriptors[0:3]: # we show the first three group descriptors
    print(gd)

print(pendrive_partition.group_descriptors[-1]) # we show the last group descriptor

root_dir = pendrive_partition.open("/")
print(root_dir) # files of root directory
print(root_dir.show_dentries()) # the actual representation of each directory entry in the root directory
print(root_dir.show_inode()) # the representation of the root directory inode

file = pendrive_partition.open("/dir1/foo.txt") # absolute path of the file or directory we want to open
print(file) # internal representation of the FileHandle object
print(file.show_inode()) # we show the inode that represents the file
print(file.read(7))
print(file.read())
print(file.seek(7))
print(file.read())
print(file.tell())
print(file.close())

print("")
print(pendrive_partition.read_block(1)) # we show the raw content of block 1 of the filesystem
print("")
print(pendrive_partition.read_inode(2)) # we show, in raw, the inode 2 of the filesystem
print("")

print(pendrive_partition.unmount()) # for now it only 'closes' the 'handle' of the storage device

import superblock, group_descriptor, inode, directory_entry

import struct

# Superblock parser (1024 bytes)
superblock_data = struct.pack("<IIIIIIIiIII", 123, 200, 5, 50, 20, 1, 2, -2, 10, 10, 7)
superblock_data += struct.pack("<IIHHHHHHIIIIHH", 1614628118, 2, 3, 4, 61267,
                                0, 7, 8, 9, 10, 0, 12, 13, 14)
superblock_data += struct.pack("<IHHIIIBBBBBBBBBBBBBBBB", 15, 16, 17, 18, 19, 20,
                                1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16)
superblock_data += b'prueba_sp_ext2\x00\x00'
superblock_data += b'/mnt/sda1' + bytes(55)
superblock_data += struct.pack("<IBBH", 21, 22, 23, 0)
superblock_data += bytes(204*4)
sb = superblock.Superblock(superblock_data)
"""Another way: sb = Superblock(s_log_block_size=1, s_state=1, s_creator_os=4)"""
print(sb)

# Group descriptor parser (32 bytes)
gd_data = struct.pack("<IIIHHHHIII", 3, 4, 5, 50, 20, 40, 0, 0, 0, 0)
gd = group_descriptor.GroupDescriptor(gd_data)
"""Another way: gd = GroupDescriptor(bg_inode_bitmap=999, bg_free_inodes_count=7)"""
print(gd)

# Inode parser (128 bytes)
inode_data = struct.pack("<HHIIIIIHHIIIIIIIIIIIIIIIIIIIIIIIII", 16876, 123, 2**20,
                         0, 1613677029, 3600*3, 0, 987, 10, 700, 416, 0, 0, 0, 0,
                         1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0)
ind = inode.Inode(inode_data)
"""Another way: ind = Inode(i_mode=0x8fff, i_atime=1614745834, i_flags=0b1000000000000)"""
print(ind)

# Directory entry parser (8 to n bytes)
dentry_data = struct.pack("<IHBB", 67, 12, 3, 2)
dentry_data += b'usr\0'
de = directory_entry.DirectoryEntry(dentry_data)
"""Another way: de = DirectoryEntry(rec_len=30, file_type=1, name="föò.txt")"""
print(de)

#! /usr/bin/env python3
#
# filedata_test.py

import sys

sys.path.insert(0, "../lib")

from filedata import FileData
from minifiledata import MiniFileData

if __name__ == "__main__":
    # FileData
    fd = FileData()
    fd.load("/etc/hosts", checksum=True)
    print(fd.name, fd.path, fd.checksum, fd.size, fd.uid, fd.gid, fd.owner, fd.group)
    print()

    encs = fd._dumps()
    print(len(encs))
    fd2 = FileData(encs)
    print(fd.name, fd.path, fd.checksum, fd.size, fd.uid, fd.gid, fd.owner, fd.group)
    print()

    print(f"fd._dumps(): {fd._dumps()}")
    print(f"str(fd): {str(fd)}")
    print(f"fd: {fd}")
    print()

    fd = FileData()
    fd.load("/boot/initrd.img", "b", checksum=True)
    print(fd.name, fd.path, fd.checksum, fd.size, fd.uid, fd.gid, fd.owner, fd.group)
    print()

    encs = fd._dumps()
    print(len(encs))
    fd2 = FileData(encs)
    print(fd.name, fd.path, fd.checksum, fd.size, fd.uid, fd.gid, fd.owner, fd.group)
    print()

    # MiniFileData
    mfd = MiniFileData()
    mfd.load("/etc/hosts")
    print(mfd.name, mfd.path, len(mfd.data))
    print()

    encs = fd._dumps()
    print(len(encs))
    mfd2 = MiniFileData(encs)
    print(mfd.name, mfd.path, len(mfd.data))
    print()

    mfd = MiniFileData()
    mfd.load("/boot/initrd.img", "b")
    print(mfd.name, mfd.path, len(mfd.data))
    print()

    encs = fd._dumps()
    print(len(encs))
    mfd2 = MiniFileData(encs)
    print(mfd.name, mfd.path, len(mfd.data))
    print()

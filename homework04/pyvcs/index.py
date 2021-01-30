import hashlib
import operator
import os
import pathlib
import struct
import sys
import typing as tp

from pyvcs.objects import hash_object


class GitIndexEntry(tp.NamedTuple):
    # @see: https://github.com/git/git/blob/master/Documentation/technical/index-format.txt
    ctime_s: int
    ctime_n: int
    mtime_s: int
    mtime_n: int
    dev: int
    ino: int
    mode: int
    uid: int
    gid: int
    size: int
    sha1: bytes
    flags: int
    name: str

    def pack(self) -> bytes:
        inocut = self.ino & 0xFFFFFFFF
        head = struct.pack(
            "!LLLLLLLLLL20sH",
            self.ctime_s,
            self.ctime_n,
            self.mtime_s,
            self.mtime_n,
            self.dev,
            inocut,
            self.mode,
            self.uid,
            self.gid,
            self.size,
            self.sha1,
            self.flags,
        )
        name = self.name.encode()
        n = 0
        pacd = head + name + b"\x00" * n
        while len(pacd) % 8 != 0:
            n += 1
            pacd = head + name + b"\x00" * n
        return pacd

    @staticmethod
    def unpack(data: bytes) -> "GitIndexEntry":
        head = data[:62]
        unpacd = struct.unpack("!LLLLLLLLLL20sH", head)
        named = data[62 : len(data)].decode().rstrip("\x00")
        res = GitIndexEntry(
            ctime_s=unpacd[0],
            ctime_n=unpacd[1],
            mtime_s=unpacd[2],
            mtime_n=unpacd[3],
            dev=unpacd[4],
            ino=unpacd[5],
            mode=unpacd[6],
            uid=unpacd[7],
            gid=unpacd[8],
            size=unpacd[9],
            sha1=unpacd[10],
            flags=unpacd[11],
            name=named,
        )
        return res


def read_index(gitdir: pathlib.Path) -> tp.List[GitIndexEntry]:
    if not os.path.isfile(pathlib.Path(gitdir, "index")):
        return []
    with open(pathlib.Path(gitdir, "index"), "rb") as f:
        bytearr = []
        while True:
            byte = f.read(1)
            bytearr.append(byte)
            if not byte:
                break
        head = b"".join(bytearr[0:4])
        version = int.from_bytes(b"".join(bytearr[4:8]), "big")
        qty = int.from_bytes(b"".join(bytearr[8:12]), "big")
        payload = bytearr[12 : len(bytearr) - 21]
        indexsha = b"".join(bytearr[len(bytearr) - 21 : len(bytearr) - 1])
    n = 61
    start = 0
    objs = []
    lens = []
    for i in range(len(payload)):
        chck1 = i - 1 > n and (i + 1) % 8 == 0
        chck3 = payload[i] == b"\x00"
        chck4 = False
        try:
            payload[i + 2].decode()
        except:
            chck4 = True
        if (chck1 and chck3) or (chck1 and chck4):
            objs.append(payload[start : i + 1])
            lens.append(len(payload[start:i]) + 1)
            n += len(payload[start : i + 1])  # do i really need 1?
            start = i + 1
            if len(objs) == qty:
                break
    res = []
    names = []
    for i in range(qty):
        names.append(b"".join(objs[i][62:]).strip(b"\x00").decode())
    for i in range(qty):
        x = GitIndexEntry.unpack(b"".join(objs[i][0:62]))
        res.append(
            GitIndexEntry(
                ctime_s=x.ctime_s,
                ctime_n=x.ctime_n,
                mtime_s=x.mtime_s,
                mtime_n=x.mtime_n,
                dev=x.dev,
                ino=x.ino,
                mode=x.mode,
                uid=x.uid,
                gid=x.gid,
                size=x.size,
                sha1=x.sha1,
                flags=x.flags,
                name=names[i],
            )
        )
    return res


def write_index(gitdir: pathlib.Path, entries: tp.List[GitIndexEntry]) -> None:
    # PUT YOUR CODE HERE
    signature = b"DIRC"
    version = 2
    header = struct.pack("!4sLL", signature, version, len(entries))
    # fheader = struct.unpack("!4sLL",header)
    payload = []
    for i in entries:
        payload.append(GitIndexEntry.pack(i))
    payload_joined = b"".join(payload)
    data = header + payload_joined
    digest = hashlib.sha1(data).digest()
    with open(pathlib.Path(gitdir, "index"), "wb") as f:
        f.write(data + digest)
        f.close()


def ls_files(gitdir: pathlib.Path, details: bool = False) -> None:
    # PUT YOUR CODE HERE
    objs = read_index(gitdir)
    resdet = []
    if details:
        res = []
        for i in objs:
            res.append(["100644", i.sha1.hex(), "0", str(i.name).strip()])
        for j in res:
            resdet.append(f"{j[0]} {j[1]} {j[2]}\t{j[3]}")
        for k in resdet:
            print(k)
    else:
        res_1 = []
        for q in objs:
            res_1.append(q.name)
        print(*res_1, sep="\n")


def update_index(gitdir: pathlib.Path, paths: tp.List[pathlib.Path], write: bool = True) -> None:
    entries = read_index(gitdir)
    for path in paths:
        with path.open("rb") as f:
            data = f.read()
        stat = os.stat(path)
        entries.append(
            GitIndexEntry(
                ctime_s=int(stat.st_ctime),
                ctime_n=0,
                mtime_s=int(stat.st_mtime),
                mtime_n=0,
                dev=stat.st_dev,
                ino=stat.st_ino,
                mode=stat.st_mode,
                uid=stat.st_uid,
                gid=stat.st_gid,
                size=stat.st_size,
                sha1=bytes.fromhex(hash_object(data, "blob", write=True)),
                flags=7,
                name=str(path),
            )
        )
    if write:
        write_index(gitdir, sorted(entries, key=lambda x: x.name))

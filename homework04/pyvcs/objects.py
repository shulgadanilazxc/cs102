import hashlib
import os
import pathlib
import re
import stat
import typing as tp
import zlib

from pyvcs.refs import update_ref
from pyvcs.repo import repo_find

# import os


def hash_object(data: bytes, fmt: str, write: bool = False) -> str:
    header = fmt + f" " + f"{len(data)}\0"
    sha = hashlib.sha1(header.encode() + data).hexdigest()
    if write:
        wd = pathlib.Path(".", os.environ["GIT_DIR"], "objects", sha[0:2])
        pathlib.Path(wd).mkdir(parents=True, exist_ok=True)
        filename = sha[2:]
        f = open(pathlib.Path(wd, filename), "wb")
        if isinstance(data, bytes):
            store = header.encode() + data
        filec = zlib.compress(header.encode() + data)
        f.write(filec)
        f.close()
    return sha


def resolve_object(obj_name: str, gitdir: pathlib.Path) -> tp.List[str]:
    wd = pathlib.Path(gitdir, "objects", obj_name[0:2])
    files = []
    for (dirpath, dirnames, filenames) in os.walk(wd):
        for i in filenames:
            if obj_name[2:] == i[:3]:
                files.append("".join([obj_name[0:2], i]))
    if len(files) > 0:
        return files
    else:
        raise Exception(f"Not a valid object name {obj_name}")


def find_object(obj_name: str, gitdir: pathlib.Path) -> str:
    # PUT YOUR CODE HERE
    ...


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
    wd = pathlib.Path(gitdir, "objects", sha[0:2])
    filename = sha[2:]
    f = open(pathlib.Path(wd, filename), "rb")
    cont = zlib.decompress(f.read())
    templ = cont.split(b" ")
    typec = templ[0].decode()
    del templ[0]
    templ_joined = b" ".join(templ)
    cont = templ_joined.split(b"\x00", maxsplit=1)[1]

    return typec, cont


def read_tree(data: bytes) -> tp.List[tp.Tuple[int, str, str]]:
    ans = []
    while data:
        before_sha_ind = data.index(b"\00")
        mode, name = data[:before_sha_ind].decode().split(" ")
        sha = data[before_sha_ind + 1 : before_sha_ind + 21]
        ans.append((int(mode), sha.hex(), name))
        data = data[before_sha_ind + 21 :]
    return ans


def cat_file(obj_name: str, pretty: bool = True) -> None:
    # PUT YOUR CODE HERE
    typec, cont = read_object(
        obj_name, pathlib.Path(".", os.environ.get("GIT_DIR", default=".git"))
    )
    if pretty and (typec == "blob" or typec == "commit"):
        print(cont.decode())
    else:
        tree = read_tree(cont)
        for i in tree:
            if i[0] == 40000:
                obj_type = "tree"
            else:
                obj_type = "blob"
            print(f"{i[0]:06}", obj_type, i[1] + "\t" + i[2])


def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    # PUT YOUR CODE HERE
    ...


def commit_parse(raw: bytes, start: int = 0, dct=None):
    comm_dict: tp.Dict[str, tp.Any]
    comm_dict = {"message": []}
    for row in raw.decode().split("\n"):
        if row.startswith(("parent", "committer", "author", "tree")):
            name, val = row.split(" ", maxsplit=1)
            comm_dict[name] = val
        else:
            comm_dict["message"].append(row)
    return comm_dict

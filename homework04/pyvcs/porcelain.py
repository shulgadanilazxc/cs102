import os
import pathlib
import typing as tp

from pyvcs.index import read_index, update_index
from pyvcs.objects import commit_parse, find_object, find_tree_files, read_object, read_tree
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref
from pyvcs.tree import commit_tree, write_tree


def add(gitdir: pathlib.Path, paths: tp.List[pathlib.Path]) -> None:
    to_add_file = []
    for path in paths:
        if path.is_file():
            to_add_file.append(path)
        if path.is_dir():
            add(gitdir, list(path.glob("*")))
    update_index(gitdir, to_add_file)


def commit(gitdir: pathlib.Path, message: str, author: tp.Optional[str] = None) -> str:
    commit_hash = commit_tree(
        gitdir,
        write_tree(gitdir, read_index(gitdir), str(gitdir.parent)),
        message,
        resolve_head(gitdir),
        author,
    )
    with (gitdir / get_ref(gitdir)).open("w") as f:
        f.write(commit_hash)
    return commit_hash


def checkout(gitdir: pathlib.Path, obj_name: str) -> None:
    for entry in read_index(gitdir):
        if (gitdir.parent / entry.name).exists():
            os.remove(entry.name)
    data_of_comm = commit_parse(read_object(obj_name, gitdir)[1])
    doing = True
    while doing:
        tree_data: tp.List[tp.Tuple[pathlib.Path, tp.List[tp.Tuple[int, str, str]]]] = [
            (gitdir.parent, read_tree(read_object(data_of_comm["tree"], gitdir)[1]))
        ]
        while len(tree_data) != 0:
            tree_path, tree_content = tree_data.pop()
            for file_data in tree_content:
                fmt, data = read_object(file_data[1], gitdir)
                if fmt == "tree":
                    tree_data.append((tree_path / file_data[2], read_tree(data)))
                    if not (tree_path / file_data[2]).is_dir():
                        (tree_path / file_data[2]).mkdir()
                else:
                    if not (tree_path / file_data[2]).exists():
                        with (tree_path / file_data[2]).open("wb") as f:
                            f.write(data)
                        (tree_path / file_data[2]).chmod(file_data[0])
        if "parent" in data_of_comm:
            data_of_comm = commit_parse((read_object(data_of_comm["parent"], gitdir)[1]))
        else:
            doing = False
    for to_remove_directory in gitdir.parent.glob("*"):
        if to_remove_directory.is_dir() and to_remove_directory != gitdir:
            try:
                os.removedirs(to_remove_directory)
            except OSError:
                continue

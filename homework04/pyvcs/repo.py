import os
import pathlib
import typing as tp


def repo_find(workdir: tp.Union[str, pathlib.Path] = ".") -> pathlib.Path:
    # PUT YOUR CODE HERE
    if os.getenv("GIT_DIR") is None:
        os.environ["GIT_DIR"] = ".git"
    wd = pathlib.Path(workdir, os.environ["GIT_DIR"])
    # wd = wd.absolute()
    if str(wd).count(".git") > 1:
        wd = pathlib.Path(str(wd).split(".git")[0] + ".git")
    # if tee[len(tee)-4:len(tee)] != ".git" :
    # wd = wd / ".git"
    if os.path.isdir(wd) != True:
        raise Exception("Not a git repository")

    return wd


def repo_create(workdir: tp.Union[str, pathlib.Path]) -> pathlib.Path:
    # os.environ["GIT_DIR"] =".git"
    if os.path.isdir(workdir) != True:
        raise Exception(f"{workdir} is not a directory")
    # PUT YOUR CODE HERE
    if os.getenv("GIT_DIR") is None:
        os.environ["GIT_DIR"] = ".git"

    wd = pathlib.Path(workdir, os.environ["GIT_DIR"])
    pathlib.Path(wd).mkdir(parents=True, exist_ok=True)
    pathlib.Path(wd, "refs", "heads").mkdir(parents=True, exist_ok=True)
    pathlib.Path(wd, "refs", "tags").mkdir(parents=True, exist_ok=True)
    pathlib.Path(wd, "objects").mkdir(parents=True, exist_ok=True)

    f = open(pathlib.Path(wd, "HEAD"), "w")
    f.write("ref: refs/heads/master\n")
    f.close()

    f = open(pathlib.Path(wd, "config"), "w")
    f.write(
        "[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = false\n\tlogallrefupdates = false\n"
    )
    f.close()

    f = open(pathlib.Path(wd, "description"), "w")
    f.write("Unnamed pyvcs repository.\n")
    f.close()
    return pathlib.Path(os.environ["GIT_DIR"])

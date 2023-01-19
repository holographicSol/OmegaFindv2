""" Written by Benjamin Jack Cullen """
import os

x_files = []


def scantree(path: str) -> str:
    global x_files
    try:
        for entry in os.scandir(path):
            if entry.is_dir(follow_symlinks=False):
                yield from scantree(entry.path)
            else:
                yield entry
    except Exception as e:
        e = str(e)
        e = e.split(': ')
        e1 = e[0]
        e2 = e[1].replace('\\\\', '\\')
        e2 = e2.replace("'", "")
        x_files.append([e1, e2])


def scan(path: str) -> list:
    global x_files
    x_files = []
    fp = []
    [fp.append(entry.path) for entry in scantree(path) if entry.is_file()]
    return fp, x_files

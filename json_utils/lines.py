import json_numpy
import builtins
import gzip


def write(path, obj_list, mode="w"):
    with Writer(path, mode) as jlwr:
        for obj in obj_list:
            jlwr.write(obj)


def read(path, mode="r"):
    obj_list = []
    with Reader(path, mode) as jlre:
        for obj in jlre:
            obj_list.append(obj)
    return obj_list


class Reader:
    def __init__(self, path, mode="r"):
        assert "r" in mode
        assert not "w" in mode
        self.path = path
        if str.endswith(mode, "|gz"):
            self.filehandle = gzip.open(self.path, mode="rt")
        else:
            self.filehandle = builtins.open(self.path, mode="rt")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        self.filehandle.close()

    def __iter__(self):
        return self

    def __next__(self):
        line = self.filehandle.__next__().strip()
        return json_numpy.loads(line)

    def __repr__(self):
        out = "{}(".format(self.__class__.__name__)
        out += "path '" + self.path + "'"
        out += ")\n"
        return out


class Writer:
    def __init__(self, path, mode="w"):
        assert not "r" in mode
        assert "w" in mode
        self.path = path
        if str.endswith(mode, "|gz"):
            self.filehandle = gzip.open(self.path, mode="wt")
        else:
            self.filehandle = builtins.open(self.path, mode="wt")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        self.filehandle.close()

    def write(self, obj):
        line = json_numpy.dumps(obj, indent=None)
        self.filehandle.write(line)
        self.filehandle.write("\n")

    def __repr__(self):
        out = "{}(".format(self.__class__.__name__)
        out += "path '" + self.path + "'"
        out += ")\n"
        return out


def open(path, mode="r"):
    """
    Read or write json lines.

    Parameters
    ----------
    path : str
        Path to file.
    mode : str
        Either of ['r', 'r|gz', 'w', 'w|gz']. The 't' for text can be added but
        is ignored.

    Returns
    -------
    reader/writer : Reader/Writer
        Depending on mode.
    """
    if "r" in mode:
        return Reader(path=path, mode=mode)
    elif "w" in mode:
        return Writer(path=path, mode=mode)
    else:
        raise ValueError("mode must either contain 'r' or 'w'.")

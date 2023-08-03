from typing import Union, List
import os

class Path:
    def __init__(self, raw: str, root: Union[str, List[str]] = []):
        self.raw = raw
        self._root: List[str] = []

        if isinstance(root, List):
            self._root.extend(root)

        if isinstance(root, str):
            self._root.append(root)

    def tostr(self):
        return os.path.join(*[*self._root], self.raw)

    def isvalid(self):
        pathstr = self.tostr()
        return os.path.exists(pathstr)
    

class PathManager:
    def __init__(self, root: Union[str, List[str]] = [], use_posix=False):
        self._root = []
        self.use_posix = use_posix

        if isinstance(root, List):
            self._root.extend(root)

        if isinstance(root, str):
            self._root.append(root)

    def __getattribute__(self, name: str):
        val = super().__getattribute__(name)

        # ignore private PathManager attributes (could be done more elegantly)
        if name in ["_root", "root"]:
            return val

        # ignore the dunders
        if name.startswith("__") and name.endswith("__"):
            return val

        # handle attributes of type str (just raw string paths or file names)
        if isinstance(val, str):
            return os.path.join(*[*self._root, val])

        # handle attributes of type Path
        if isinstance(val, Path):
            return os.path.join(*[*self._root, *val._root], val.raw)

        # otherwise, just return the val captured from super
        return val

    def aspath(self, name: str):
        val = super().__getattribute__(name)

        if isinstance(val, str):
            return Path(val, root=self._root)

        if isinstance(val, Path):
            return val

        raise TypeError(f"{name} value is not of type {str} or {Path}.")

    @property
    def root(self) -> str:
        aspath = os.path.join(*self._root)
        return aspath

    def setroot(self, root: Union[str, List[str]]):
        if isinstance(root, List):
            self._root = [*root]

        if isinstance(root, str):
            self._root = [root]

    def add_root(self, root: Union[str, List[str]]):
        if isinstance(root, List):
            self._root.extend(root)

        if isinstance(root, str):
            self._root.append(root)


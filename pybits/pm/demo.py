from pybits.pm import PathManager, Path

class SimplePm(PathManager):
    foo = "foo.txt"
    bar = "bar.txt"

simple = SimplePm(root="root_dir")
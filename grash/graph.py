import magic
import grash.parser
import os


class Graph:
    def __init__(self, paths, scripts):
        self._nodes = dict()
        self._scripts = scripts
        self._get_all_from_paths(paths)
        self._add_scripts(scripts)
        self._graph_deps()

    def _get_all_from_paths(self, paths):
        for path in paths:
            for root, dirs, files in os.walk(path):
                for file in files:
                    self._nodes[file] = self.Node(os.path.join(root, file))

    def _add_scripts(self, scripts):
        for script in scripts:
            self._nodes[script] = self.Node(script)

    def _graph_deps(self):
        for script in self.scripts:
            words = grash.parser.parse(script)
            for word in words:
                if word in self._nodes:
                    self._nodes[script].deps.append(self._nodes[word])

    @property
    def scripts(self):
        return self._scripts

    def __getitem__(self, key):
        return self._nodes[key]

    class Node:
        def __init__(self, file_path):
            self._file_path = file_path
            self._filename = os.basename(file_path)
            self._get_type()
            self._deps = []

        def _get_type(self):
            self._type = magic.from_file(self._file_path)

        @property
        def name(self):
            return os.path.basename(self._filename)

        @property
        def type(self):
            return self._type

        @property
        def dependencies(self):
            return self._deps

        @dependencies.setter
        def dependencies(self, deps):
            self._deps = deps

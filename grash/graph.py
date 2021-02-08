import magic
import grash.parser
import os


def _get_all_files_from_paths(paths):
    """
    Gets all files located within paths
    :param paths: Paths to search for files
    :return: List of all files found in paths
    """
    path_files = []
    for path in paths:
        for root, dirs, files in os.walk(path):
            path_files += [os.path.join(root, file) for file in files]
    return path_files


class Graph:
    """
    Dependency graph class
    """
    def __init__(self, paths, scripts):
        self._nodes = dict()
        self._scripts = scripts
        self._create_nodes(paths)
        self._add_scripts(scripts)
        self._graph_deps()

    def _create_nodes(self, paths):
        """
        Create nodes for all the files in paths
        :param paths: Paths to process
        :return: None
        """
        for file in _get_all_files_from_paths(paths):
            self._nodes[os.path.basename(file)] = self.Node(file)

    def _add_scripts(self, scripts):
        """
        Adds each script
        :param scripts:
        :return: None
        """
        for script in scripts:
            self._nodes[script] = self.Node(script)

    def _graph_deps(self):
        """
        Gets dependencies for all scripts
        :return: None
        """
        for script in self.scripts:
            words = grash.parser.parse(script)
            for word in words:
                if word in self._nodes:
                    self._nodes[script].dependencies.append(self._nodes[word])

    @property
    def scripts(self):
        """
        Returns all scripts in graph
        :return: List of scripts
        """
        return self._scripts

    def __getitem__(self, key):
        """
        Getter for a node in the graph
        :param key: Name of script or file
        :return: Node representing script or file
        """
        return self._nodes[key]

    class Node:
        """
        A node in the dependency graph.  Could be a script or a dependency.
        """
        def __init__(self, file_path):
            self._file_path = file_path
            self._filename = os.path.basename(file_path)
            self._type = magic.from_file(self._file_path)
            self._deps = []

        @property
        def name(self):
            """
            Returns name of file
            :return: Name of file
            """
            return os.path.basename(self._filename)

        @property
        def type(self):
            """
            Returns what type of executable
            :return: File type
            """
            return self._type

        @property
        def dependencies(self):
            """
            Returns the list of dependencies
            :return: List of dependencies
            """
            return self._deps

        @dependencies.setter
        def dependencies(self, deps):
            """
            Sets the list of dependencies
            :param deps: List of dependencies
            :return: None
            """
            self._deps = deps

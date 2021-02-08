from grash.graph import Graph
import argparse
import os


def main():
    parser = argparse.ArgumentParser(description='Inspect dependencies between bash scripts')
    subparsers = parser.add_subparsers(title='subcommands', dest='command')

    parser_inspect = subparsers.add_parser('inspect', help='Inspect and print dependencies')
    parser_inspect.add_argument('-p', '--path', help="Use passed path instead of PATH from environment")
    parser_inspect.add_argument('scripts', nargs='+', help="Scripts to inspect")

    # TODO
    # parser_graph = subparsers.add_parser('graph', help='Graph dependencies')
    # parser_graph.add_argument('-p', '--path', help="Use passed path instead of PATH from environment")
    # parser_graph.add_argument('-o', '--output', help="Output image file")
    # parser_graph.add_argument('scripts', nargs='+', help="Scripts to graph")

    args = parser.parse_args()

    paths = args.path.split(':') if args.path else os.environ.get('PATH').split(':')

    dep_graph = Graph(paths, args.scripts)

    return do_inspect(dep_graph) if args.command == 'inspect' else do_graph(dep_graph) if args.command == 'graph' else None


def do_inspect(graph):
    """
    Prints out graph to console
    :param graph: Graph object to print out
    :return:
    """
    for script in graph.scripts:
        print(f"Script: {script}")
        print(f"has dependencies...")
        for dep in sorted(graph[script].dependencies, key=lambda d: d.name):
            print(dep.name)


def do_graph(graph):
    """
    Creates output image file of graph
    :param graph:
    :return:
    """
    # TODO
    return


if __name__ == '__main__':
    main()

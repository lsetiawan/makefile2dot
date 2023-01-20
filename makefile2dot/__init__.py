"""
Define the needed functions.
"""

import subprocess as sp
import graphviz as gv
import argparse


def stream_database(input_path='.'):
    """
    Generate and yield entries from the Makefile database.

    This function reads a Makefile using the make program (only tested with GNU
    Make) on your machine. It in turn generates the database constructed from
    the Makefile, ignoring default targets ("-r").
    """
    command = ["make", "-prnB", "-C", input_path]
    with sp.Popen(command, stdout=sp.PIPE, universal_newlines=True) as proc:
        for line in proc.stdout:
            if line[0] == '#':
                continue
            if line.isspace():
                continue
            if ': ' not in line:
                continue
            if line[0] == '&':
                continue
            yield line.strip()


def build_graph(stream, **kwargs):
    """
    Build a dependency graph from the Makefile database.
    """

    graph = gv.Digraph(comment="Makefile")
    graph.attr(rankdir=kwargs.get('direction', 'TB'))
    for line in stream:
        target, dependencies = line.split(':')

        # Draw all targets except .PHONY (it isn't really a target).
        if target != ".PHONY":
            graph.node(target)

        for dependency in dependencies.strip().split(' '):
            if dependency in ["default", "clean"]:
                continue
            elif target == ".PHONY":
                graph.node(dependency, shape="circle")
            elif target in ["default"]:
                graph.node(dependency, shape="rectangle")
            else:
                graph.node(dependency, shape="rectangle")
                graph.edge(target, dependency)

    return graph


def makefile2dot(**kwargs):
    """
    Visualize a Makefile as a Graphviz graph.
    """

    direction = kwargs.get('direction', "BT")
    if direction not in ["LR", "RL", "BT", "TB"]:
        raise ValueError('direction must be one of "BT", "TB", "LR", RL"')

    output = kwargs.get('output', '')
    input_path = kwargs.get('input_path', '.')
    view = kwargs.get('view', False)

    graph = build_graph(stream_database(input_path=input_path), direction=direction)
    if output == "":
        if view:
            graph.view()
        else:
            print(graph)
    else:
        with open(output, 'w') as file:
            file.write(str(graph))
        if view:
            graph.view()

def main():
    DESC = "Create a dot graph of a Makefile."
    PARSER = argparse.ArgumentParser(description=DESC)
    PARSER.add_argument('--input', '-i', dest='input_path', default=".",
                        help="input directory where Makefile resides")

    PARSER.add_argument('--direction', '-d', dest='direction', default="BT",
                        help="direction to draw graph ('BT', 'TB', 'LR', or 'RL')")

    PARSER.add_argument('--output', '-o', dest='output', default="",
                        help="output file name (default: stdout).")

    PARSER.add_argument('--view', '-v', action='store_true',
                        help="view the graph (disables output to stdout)")

    ARGS = PARSER.parse_args()

    makefile2dot(direction=ARGS.direction, output=ARGS.output, view=ARGS.view, input_path=ARGS.input_path)

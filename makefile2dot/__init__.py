"""
Define the needed functions.
"""

from sys import stdin, stdout, stderr
import re


def _line_emitter(input_stream):
    """
    Emit all lines that don't end with a continuation character ("\\").
    """
    line_to_emit = ''

    for line in input_stream:
        if line.endswith('\\'):
            line_to_emit += line[:-1]
        else:
            line_to_emit += line
            yield line_to_emit
            line_to_emit = ''


def _dependency_emitter(lines):
    """
    Emit a list of dependencies for each target.
    """
    colon = re.compile(':')

    def no_content(line):
        if not line:
            return True

        commented = line in ['\t', '#']
        contains_assignment = line.find('=') > 0
        contains_question = line.find('?') > 0
        return commented or contains_assignment or contains_question

    for line in lines:
        if no_content(line):
            continue

        parts = colon.split(line)
        if len(parts) == 1:
            continue
        elif len(parts) == 2:
            if not parts[1] or parts[1][0] != '=':
                yield tuple(parts)
        else:
            print(stderr, 'more then one ":" not yet implemented ;)\n')
            print(stderr, 'got the following:\n%s' % parts)


def _single_dot_dep_emitter(out_deps_pairs):
    """
    Emit a `dot` language command to draw the dependency in GraphViz.
    """
    whitespace = re.compile('[ \t]+')
    for outs_str, deps_str in out_deps_pairs:
        for out in whitespace.split(outs_str.strip()):
            yield '\t"%s"\n' % out
            deps = whitespace.split(deps_str.strip())
            for dep in deps:
                if dep:
                    if dep[0] == '#':
                        break
                    yield '\t"%s" -> "%s"\n' % (dep, out)


def _trio(line):
    """
    Compose _single_dot_dep_emitter to _dependency_emitter to _line_emitter.
    """
    return _single_dot_dep_emitter(_dependency_emitter(_line_emitter(line)))


def makefile2dot():
    """
    Visalize a Makefile as a Graphviz graph.
    """
    stdout.write('digraph G {\n\trankdir="BT"\n')
    for line in _trio(''.join(stdin).split('\n')):
        stdout.write(line)
    stdout.write('}\n')

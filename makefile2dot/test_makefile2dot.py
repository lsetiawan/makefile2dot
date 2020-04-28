"""
Test the helper functions in makefile2dot.
"""
from makefile2dot import _line_emitter, _dependency_emitter, _trio


def test_makefile():
    '''
    Should still return the target.
    '''
    line = r"""
target: hello
    recipe

other_target: hey there
"""
    assert 


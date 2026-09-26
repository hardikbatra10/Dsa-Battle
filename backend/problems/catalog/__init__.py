"""The problem catalog, one module per topic.

seed_problems.py imports PROBLEMS from here. To add problems, edit (or
add) a topic module and list it below - nothing else needs to change.
"""

from .arrays import PROBLEMS as _arrays
from .strings import PROBLEMS as _strings
from .linked_list import PROBLEMS as _linked_list
from .stack_queue import PROBLEMS as _stack_queue
from .trees import PROBLEMS as _trees
from .graphs import PROBLEMS as _graphs
from .heap import PROBLEMS as _heap
from .dp import PROBLEMS as _dp
from .greedy import PROBLEMS as _greedy
from .backtracking import PROBLEMS as _backtracking
from .binary_search import PROBLEMS as _binary_search
from .two_pointers import PROBLEMS as _two_pointers
from .sliding_window import PROBLEMS as _sliding_window
from .bit_manipulation import PROBLEMS as _bit_manipulation
from .math_problems import PROBLEMS as _math_problems


PROBLEMS = [
    *_arrays,
    *_strings,
    *_linked_list,
    *_stack_queue,
    *_trees,
    *_graphs,
    *_heap,
    *_dp,
    *_greedy,
    *_backtracking,
    *_binary_search,
    *_two_pointers,
    *_sliding_window,
    *_bit_manipulation,
    *_math_problems,
]

__all__ = ["PROBLEMS"]

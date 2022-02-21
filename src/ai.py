from abc import ABCMeta, abstractmethod
from math import inf
from operator import gt as greater_than
from operator import lt as lesser_than


class AiNode(metaclass=ABCMeta):
    @abstractmethod
    def children_get(self):
        pass

    @abstractmethod
    def end_node(self) -> bool:
        pass

    @abstractmethod
    def score(self):
        pass


def minimax(node: AiNode, depth: int, maximizing: bool) -> tuple[int, any, int]:
    """

    :param node:
    :param depth:
    :param maximizing:
    :return:
    """
    if depth == 0 or node.end_node():
        return node.score(), node, 1
    if maximizing:
        op_func = greater_than
        value = -inf
    else:
        op_func = lesser_than
        value = inf

    total_explored = 0
    best_child = node
    for child in node.children_get():
        child_value, _, explored = minimax(child, depth - 1, not maximizing)
        total_explored += explored

        if op_func(child_value, value):
            best_child = child
            value = child_value

    return value, best_child, total_explored

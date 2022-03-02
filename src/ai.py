from abc import ABCMeta, abstractmethod
from math import inf
from operator import gt as greater_than
from operator import lt as lesser_than
from operator import ge as greater_or_equal
from operator import le as lesser_or_equal


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
    Run minimax to determine the best child of a node

    :param node: Node to start searching from, must implement AiNode
    :param depth: Maximum depth to search for, terminates when it reaches 0
    :param maximizing: True when the function gets executed for the maximizing player
    :return: (Score, Child of node with the best score, Total nodes explored)
    """
    if depth == 0 or node.end_node():
        return node.score(), node, 1
    if maximizing:
        op_func = greater_than
        best_value = -inf
    else:
        op_func = lesser_than
        best_value = inf

    total_explored = 0
    best_child = node
    for child in node.children_get():
        child_value, _, explored = minimax(child, depth - 1, not maximizing)
        total_explored += explored

        if op_func(child_value, best_value):
            best_child = child
            best_value = child_value

    return best_value, best_child, total_explored


def alpha_beta(node: AiNode, depth: int, maximizing: bool, alpha: int = -inf, beta: int = inf) -> tuple[int, any, int]:
    """
    Run alpha_beta to determine the best child of a node

    :param node: Node to start searching from, must implement AiNode
    :param depth: Maximum depth to search for, terminates when it reaches 0
    :param maximizing: True when the function gets executed for the maximizing player
    :param alpha: Alpha value to determine cut off, initial call should be -inf
    :param beta: Beta value to determine cut off, initial call should be -inf
    :return: (Score, Child of node with the best score, Total nodes explored)
    """
    if depth == 0 or node.end_node():
        return node.score(), node, 1

    total_explored = 0
    best_child = node

    if maximizing:
        best_value = -inf
        for child in node.children_get():
            child_value, _, explored = alpha_beta(child, depth - 1, False, alpha, beta)
            total_explored += explored

            if child_value > best_value:
                best_child = child
                best_value = child_value

            alpha = max(best_value, alpha)
            # break off
            if beta <= best_value:
                break
    else:
        best_value = inf
        for child in node.children_get():
            child_value, _, explored = alpha_beta(child, depth - 1, True, alpha, beta)
            total_explored += explored

            if child_value < best_value:
                best_child = child
                best_value = child_value

            beta = min(best_value, beta)

            # break off
            if alpha >= best_value:
                break

    return best_value, best_child, total_explored

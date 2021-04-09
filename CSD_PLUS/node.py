# node.py
# 03-04-2021
# Some simple algorithms to work with the string sanitization projects from:
#
# https://github.com/Yebulabula/String-Sanitization-Project
#
# Author Ye Mao
# King's College London
# Version 1.0

from collections import defaultdict
import math


def delete(data, index):
    """
        The function to delete symbol at input index.
        :param data: (string) The input data for delete.
        :param index: (int) The index of deleted symbol
        :return: (string) The string data after deletion.
    """
    return data[:index] + data[index + 1:]


class ELLS_node:
    """
        The class is to store all information and statistics of tree node.
    """

    def __init__(self, state, move, score, c, parent=None):
        """
            Initialize a ELLS_node
            :param state (string): The data(value) of each node.
            :param move (int): The index of the deleted letter of the node's parent.
            :param score (float): The R-score of deletion(move).
            :param c (int): The exploration parameter in UCT formula.
            :param parent (ELLS_node): The parent node of node.

        """
        self.state = state
        self.move = move
        self.score = score
        self.parent = parent
        self.C = c

        self.children = defaultdict(ELLS_node)  # The collection of child nodes.
        self.isExpanded = False  # The boolean statement to check is the node has been expanded
        self.reward = 0  # The cumulative reward for all simulations on the node.
        self.visits = 0  # The number of visits on the node.

    def _print_attribute(self):
        """
            The function to print all attributes' values of the node.
            :return: None
        """
        print(vars(self))

    def compute_uct(self):
        """
            The function to calculate the UCT value of the node.
            :return: UCT(float): if the number of visits on the node is non-zero, we calculate the UCT
            of selected node by UCB1 formula:  -reward/visits + c * sqrt(log(parent visits) / visits)
        """
        if self.visits != 0:
            return - self.reward / self.visits + self.C * math.sqrt(math.log(self.parent.visits) / self.visits)
        else:
            return float('inf')

    def select_leaf(self):
        """
            The function to recursively select the current most promising node (maximizes UCT) until it reaches
            the leaf node.
            :return: current(ELLS_node) The current best leaf node. Such node will also be used in further
                     expansion and simulation step.
            :return: selected_nodes_R(float) The sum of promising nodes' rewards. Eg: we choose the best
                     node follow the order of A -> B -> C, then selected_nodes_R = reward(A) + reward(B)
                     + reward(C)
        """
        current = self
        best_child = None
        selected_nodes_R = 0
        while current.isExpanded:
            maxUCT = - float('inf')
            for child in current.children.values():
                UCT = child.compute_uct()
                if UCT > maxUCT:
                    maxUCT = UCT
                    best_child = child

            current = best_child
            selected_nodes_R += current.score
        return current, selected_nodes_R

    def backpropagation(self, simulation_reward):
        """
            The function to update the current 'move'(delete) sequence with the simulation result.
            :param simulation_reward:(int) The total R-score of the simulation.
            :return: None
        """
        current = self
        while current.parent is not None:
            current.visits += 1
            current.reward += simulation_reward
            current = current.parent

    def expand(self, legal_deletions, c):
        """
            The function to add all states reachable from the current most promising node to the tree.
            :param legal_deletions: ([(int,int)]) The indices of all legal deleted symbols and their corresponding
            R-scores.
            :param c:(float) the exploration parameter of child node.
            :return: None
        """
        for legal in legal_deletions:
            move = legal[1]

            # create a (move:ELLS-node) item for all child nodes.
            self.children[move] = ELLS_node(delete(self.state, move),
                                            move,
                                            legal[0],
                                            parent=self,
                                            c=c)
        self.isExpanded = True

    def refresh(self):
        """
            The function to refresh the reward and score of the node.
            :return: None
        """
        self.reward = 0
        self.score = 0

class DummyNode(object):
    """
        The class to construct the parent node of the root node.
    """
    def __init__(self):
        self.parent = None

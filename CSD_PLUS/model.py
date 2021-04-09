# model.py
# 03-04-2021
# Some simple algorithms to work with the string sanitization projects from:
#
# https://github.com/Yebulabula/String-Sanitization-Project
#
# Author Ye Mao
# King's College London
# Version 1.0

from collections import defaultdict
import numpy as np
import pandas as pd
import random
from node import ELLS_node, DummyNode
import gc
import DataProcessing


def _non_zero(value):
    """
        The function to transform negative input value to zero.
        :param value: (int) the integer input value
        :return 0:
    """
    return 0 if value < 0 else value


def delete_sequence(data, indices):
    """
        The simple algorithm to delete a sequence of characters from the data.
        :param data: (string) The input data for deletions.
        :param indices: ([int]) The sequence of deleted symbols' indices.
        :return: (string) The string data after deletions.
    """
    outcome = ''
    initial = 0
    for i in indices:
        outcome += data[initial:i]
        initial = i + 1
    outcome += data[indices[-1] + 1:]
    return outcome


class solver:
    """
        The class for user to choose various strategies to enhance data utility.
        Options: (Find more details in report)
        GD-ALGO
        ELLS-ALGO
        Exhaustive-Search
        Baseline
    """

    def __init__(self, w, k, delta, z, sensitive_patterns, tau, omega, c, max_simulations, tolerance):
        """
            The constructor for the solver class.
            :param w: (string) The string data before sanitization.
            :param k: (int) The pattern length.
            :param delta: (int) The number of deletions are allowed to reduce distortion
            :param z: (string) The string data after sanitization.
            :param sensitive_patterns: ([string]) A collection of all length-k sensitive patterns.
            :param tau: (int) The tau value to identify if a pattern is tau-ghost / tau-lost
            :param omega: (int) The weight of non-spurious pattern utility.
            ELLS-ALGO
            :param c: (int) The exploration parameter, which is used in ELLS-ALGO.
            :param max_simulations: (int) The number of simulations per decision.
            :param tolerance: (int) The pruning factor of Monte Carlo search tree.
        """
        self.W = w
        self.k = k
        self.Z = z
        self.tau = tau
        self.delta = delta
        self.omega = omega
        self.S = sensitive_patterns
        self.max_simulations = max_simulations
        self.C = c
        self.tolerance = tolerance
        self.remain_delete = delta

        self.non_sens_w = self._search_nsens(w)  # All non-sensitive patterns in W.
        self.backup_non_sens = defaultdict()  # A dictionary to store all W that have been
        # searched non-sensitive patterns
        self.backup_R_score = defaultdict()  # A dictionary to store all deleted symbols that have been
        # tried to simulate.
        self.GD_Total = 0  # The total R-score of GD-ALGO
        self.ELLS_Total = 0  # The total R-score of ELLS-ALGO
        self.root = ELLS_node(z, None, 0, c, DummyNode())  # The root node for monte carlo search tree.
        self.EX = []  # The collection for storing all possible deleted symbols permutation.
        self.GD_track = [z]  # The track to record the whole deletion process in GD-ALGO.
        self.ELLS_track = [z]  # The track to record the whole deletion process in ELLS-ALGO.

    def _is_spurious(self, freq_z, freq_w):
        """
            The function to check if a pattern is a spurious pattern by using
            the frequency of such pattern in Z and W.
            :param freq_z: The frequency of the pattern in Z.
            :param freq_w: The frequency of the pattern in W.
            :return: (Boolean) True if the pattern is spurious; otherwise, false.
        """
        return True if freq_w < self.tau <= freq_z or \
                       freq_z < self.tau <= freq_w else False

    def _is_sensitve(self, pattern):
        """
            The function to check if a pattern is sensitive pattern.
            :param pattern: (string) A length-k substring
            :return: (Boolean) True if pattern is sensitive, otherwise, false.
        """
        return [False, True][pattern in self.S]

    def _search_nsens(self, data):
        """
            The function to search all non-sensitive patterns in data.
            :param data: (string) A string consists of a sequence of the length-k substring.
            :return: dict{string:int} A dictionary to store all pattern : frequency pair in data.
        """
        pat_dict = defaultdict(int)
        for i in range(len(data) - self.k + 1):
            pat_dict[data[i:i + self.k]] += 1
        return pat_dict

    def _get_score(self, current, non_sens_z, index):
        """
            The function to calculate the R-score of deleting a letter at input index from a current string.
            :param current: (string) A string type data for deletion
            :param non_sens_z: (dict{string:int}) A dictionary for storing all non-sensitive patterns in current.
            :param index: (int) The index of deleted symbol.
            :return score:  (float) The R-score of deletion.
            :return new_dict: (dict{string:int}) A dictionary for storing all affected patterns and their
            corresponding frequency change.
        """
        new_dict = {}
        before = current[_non_zero(index - self.k + 1):index + self.k]
        after = current[_non_zero(index - self.k + 1):index] + current[index + 1: index + self.k]

        non_sens_before = self._search_nsens(before)
        non_sens_after = self._search_nsens(after)

        affected_patterns = set(list(non_sens_after.keys()) + list(non_sens_before.keys()))

        spurious, non_spurious = 0, 0
        for pattern in affected_patterns:
            diff = non_sens_after[pattern] - non_sens_before[pattern]
            if non_sens_after[pattern] > 0 and self._is_sensitve(pattern):
                return float('inf'), None  # output infinity as reinstating sensitive pattern.
            new_dict[pattern] = diff
            freq_Z = non_sens_z[pattern]
            freq_W = self.non_sens_w[pattern]
            distance = freq_Z - freq_W  # distortion of Z
            reduction = np.square(distance + diff) - np.square(distance)
            # distortion reduction of a single pattern.
            if self._is_spurious(freq_z=freq_Z,
                                 freq_w=freq_W):
                spurious += reduction
            else:
                non_spurious += reduction
        score = spurious + self.omega * non_spurious  # calculate R-score
        return score, new_dict

    def _get_distortion(self, data):
        """
            The function to calculate the distortion of data.
            Sigma_sum((distortion in W - distortion in data)^2)
            :param data (string): A string consists of a sequence of a length-k substring.
            :return: (int,int): Distortion of spurious pattern and distortion of the non-spurious pattern.
        """
        non_sens = self._search_nsens(data)
        patterns = set(list(self.non_sens_w.keys()) + list(non_sens.keys()))
        non_spurious, spurious = 0, 0
        for pattern in patterns:
            distortion = np.square(self.non_sens_w[pattern] - non_sens[pattern])
            if self._is_spurious(freq_z=non_sens[pattern],
                                 freq_w=self.non_sens_w[pattern]):
                spurious += distortion
            else:
                non_spurious += distortion
        return spurious, non_spurious

    def _GD_ALGO(self):
        """
            The function to run GD-ALGO. Such algorithm exploits greedy search to recursively
            search current best-deleted symbol until completing delta deletions.
            :return G: (string) The resulting string of GD-ALGO.
        """
        deleted_symbols = []
        Z = self.Z
        non_sens_z = self._search_nsens(Z)

        for i in range(self.delta):
            scores = [(delete, *self._get_score(current=Z,
                                                non_sens_z=non_sens_z,
                                                index=delete)) for delete in range(len(Z))]

            df = pd.DataFrame(scores, columns=['A', 'B', 'C'])
            best_delete, best_score, best_non_sens = scores[df['B'].argmin()]
            for key, value in best_non_sens.items():
                non_sens_z[key] += value
            Z = Z[:best_delete] + Z[best_delete + 1:]
            self.GD_track.append(Z)
            deleted_symbols.append(best_delete)
            self.GD_Total += best_score
        return Z

    def _extract_non_sens(self, data):
        """
            The function to extract all non-sensitive patterns of data from global dictionary if
            global dictionary consists of input (data:index) key, otherwise add it to the global
            dictionary.
            :param data: (string) A string consists of a sequence of length-k substring.
            :return: (dict{string:int}) A dictionary stores all pattern : frequency pair.
        """
        if data not in self.backup_non_sens:
            self.backup_non_sens[data] = self._search_nsens(data)
        return self.backup_non_sens[data]

    def _extract_r_score(self, data, index):
        """
            The function to extract R-score of deleting letter from global dictionary if
            global dictionary consists of input (data:index) key, otherwise add it to the global
            dictionary.
            :param data: (string) A string consists of a sequence of length-k substring.
            :param index: (int) The deleted symbol's index.
            :return: (float): The R-score of delete.
        """
        if (data, index) not in self.backup_R_score:
            score, non_sens = self._get_score(current=data,
                                              non_sens_z=self._extract_non_sens(data),
                                              index=index)
            self.backup_R_score[(data, index)] = score
        return self.backup_R_score[(data, index)]

    def _get_legal_deletions(self, data, strategy=''):
        """
            The function to get all legal deletions.
            :param data: (string) A string type data.
            :param strategy: (string)
            strategy = 'all' -> search all positions in data and output the one that minimizes R-score.
            :return: (float,int) The minimum R-score for all deletions, the index of optimal deletion.
            Others -> collect all deleted symbols whose index in the range of [lowest R-score, lowest R-score
            + tolerance]
            :returns: [(float,int)] A list to store all legal (R-score,deleted symbol index) tuple.
        """
        min = float('inf')
        scores = []
        for i in range(len(data) - 1):
            if data[i] != data[i + 1] or i == len(data) - 1:
                score = self._extract_r_score(data, i)
                scores.append((score, i))
                if score < min:
                    min = score

        scores.append((self._extract_r_score(data, len(data) - 1), len(data) - 1))

        if strategy != 'all':
            if len(scores) != 1:
                max = min + self.tolerance
                return list(filter(lambda f: f[0] <= max, scores)) if len(scores) > 0 else []
            else:
                return scores
        else:
            scores.sort(key=lambda x: x[0])
            return scores[0]

    def simulation(self, simulate, selected_nodes_R):
        """
            The function to perform a simulation rollout (Delete a sequence of symbols).
            :param simulate:  (ELLS-node) The start node for simulation.
            :param selected_nodes_R: (float) The total R-score that 'simulate' node already get.
            :return: (float) The total R-score of simulation.
        """
        state = simulate.state
        actions = len(state) + self.delta - len(self.Z)
        simulation_reward = selected_nodes_R + self.ELLS_Total
        for i in range(actions):
            while 1:
                policy = random.randint(0, len(state) - 1)
                # The legal deleted characters cannot be the same as the neighbours. Such
                # method can ensure that the symbols deleted for this simulation node are
                # completely different each time.
                # Experimental result proves that random function is more effective than
                # searching for all legal deletions for each deletions.
                neighbor_right = policy + 1
                if neighbor_right < len(state):
                    if state[policy] == state[neighbor_right]:
                        continue
                # Consider only the deletion that does not incur any sensitive patterns.
                reinstate = False
                after = state[_non_zero(policy - self.k + 1):policy] + state[policy + 1: policy + self.k]
                for j in range(len(after) - self.k + 1):
                    if self._is_sensitve(after[j:j + self.k]):
                        reinstate = True
                        break
                if not reinstate: break
            simulation_reward += self._extract_r_score(state, policy)
            state = DataProcessing.delete(state, policy)
        return simulation_reward

    def _ELLS_ALGO(self, root, iterations):
        """
            The main function of ELLS-ALGO. This function recursively finding the most promising symbol to delete
            by running a certain number of Monte Carlo cycles (Selection -> Expansion -> Simulation
            -> Backpropagation) until all optimal delete characters.
            :param root: (ELLS_node) The root node of the tree stores the string to be deleted.
            :param iterations: (int) The number of deletions required to make a decision(select deleted symbol)
            :return: H:(string) The resulting data after deletions.
        """
        # Base case of recursion: recursion terminates as only one remaining symbol need to be deleted.
        if self.remain_delete == 1:
            score = self._get_legal_deletions(root.state, strategy='all')  # greedy find current best deleted symbol
            self.ELLS_Total += score[0]
            result = DataProcessing.delete(root.state, score[1])
            self.ELLS_track.append(result)
            return result

        # Expand the root node beforehand.
        if not root.isExpanded:
            root.expand(self._get_legal_deletions(root.state), self.C)

        for _ in range(iterations):
            # Selection
            simulate, selected_nodes_R = root.select_leaf()

            # Expansion delay
            if simulate.visits > 3 and len(self.Z) - len(simulate.state) < self.delta:
                # Expansion
                simulate.expand(self._get_legal_deletions(simulate.state), self.C)
                simulate = simulate.children[next(iter(simulate.children))]
                simulate_score = selected_nodes_R + simulate.score
            else:
                simulate_score = selected_nodes_R
            # Simulation
            simulation_reward = self.simulation(simulate, simulate_score)
            # Backpropagation
            simulate.backpropagation(simulation_reward)

        # Final deleted symbol selection -> select the node by max-robust child selection policy.
        best_child = None
        best_result = - float('inf')
        for child in root.children.values():
            score = - child.reward + child.visits
            if score > best_result:
                best_result = score
                best_child = child
        self.ELLS_track.append(best_child.state)

        # Search tree reuse
        iterations = self.max_simulations - np.sum([child.visits for child in best_child.children.values()])
        self.remain_delete -= 1
        self.ELLS_Total += best_child.score
        best_child.refresh()
        gc.collect()

        # transform best root child to next tree's root node.
        return self._ELLS_ALGO(best_child, int(iterations))

    def run(self):
        """
            The function to run CSD-Plus model. This function uses the result of GD-ALGO as the lower bound,
            followed by run ELLS-ALGO to further optimize the result based on it.
            :return L: (string) If the total R score of GD-ALGO is greater than or equal to the total
            R score of EllS-ALGO, the GD algorithm results are output; otherwise,
            the ELLS algorithm results are output.
        """

        H = self._GD_ALGO()
        G = self._ELLS_ALGO(self.root, self.max_simulations)
        return [G, H][self.GD_Total < self.ELLS_Total]

    def baseline(self):
        """
            The function of the baseline algorithm. Firstly, sort the distortion of each pattern in descending
            order. Second, traverse each letter from the most distorted pattern to the least distorted pattern.
            The loop will terminate if and only if the current candidate letter does not incur any sensitive pattern.
            :return BA: (String) the string type of data, whose length is |Z| - delta.
        """
        Z = self.Z
        w_nsens = self.non_sens_w
        z_nsens = self._search_nsens(Z)
        for i in range(self.delta):
            # A list of all candidate patterns' distortions in Z
            candidates = [(abs(z_nsens[Z[j:j + self.k]] - w_nsens[Z[j:j + self.k]]), list(range(j, j + self.k)))
                          for j in range(len(Z) - self.k + 1)]

            # Sort distortions in descending order.
            # The most distorted pattern will be considered first.
            candidates.sort(key=lambda x: x[0], reverse=True)
            for candidate in candidates:
                for victim in candidate[1]:
                    after = Z[_non_zero(victim - self.k + 1):victim] + Z[victim + 1: victim + self.k]
                    non_sens_after = self._search_nsens(after)
                    # check if 'victim' led to any sensitive patterns.
                    if len(set(non_sens_after.keys()).intersection(set(self.S))) == 0:
                        Z = DataProcessing.delete(Z, victim)
                        z_nsens = self._search_nsens(Z)
                        break
                    else:
                        continue
                    break
                else:
                    continue
                break
        return Z

    def _exhaustive_search(self, lst, n):
        """
            The recursive function to exhaustively search all possible deleted symbols
            permutations, and then choose the permutation which results a string with
            the lowest distortion as the result.

            :param lst: ([int]) A collection of all deleted symbols' indices.
            :param n: (int) The remaining number of deletes. (i.e, delta - sizeof(current permutation list))
            when n = 0, the size of permutation is delta and we complete finding all deleted symbols.
            :return :[int] A collection of best-delta deleted symbols.(Global optimum)

            This function exploits some ideas from below link:
            "https://stackoverflow.com/questions/52356091/recursive-algorithm-to-
             generate-all-permutations-of-length-k-of-a-list-in-python"
        """
        # if length of permutation is <= 0, return empty list
        if n <= 0:
            return [[]]
        # else take empty list l
        l = []
        # loop over the whole list
        for i in range(0, len(lst)):
            m = lst[i]
            remLst = lst[:i] + lst[i + 1:]
            for p in self._exhaustive_search(remLst, n - 1):
                perm = sorted([m] + p)
                if not perm in l:
                    l.append(perm)
                    # all permutations with size delta.
                    if len(perm) == self.delta:
                        tmp = delete_sequence(self.Z, perm)  # simulate deletions
                        self.EX.append(sum(self._get_distortion(tmp)))  # insert each simulation result to list.
        return l

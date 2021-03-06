import numpy as np
import random
import copy
from scheduling import MCTSnodeUCT, MCTStree
import math

def get_value(dict, key):
    return dict[key] if key in dict.keys() else 0


def convert_to_string(index, str):
    return str[:index] + str[index + 1:]


class CSD_PLUS:
    def __init__(self, W, k, C, delta, Z_prime, maxHorizon, sens_patterns, tau, multiplier):
        self.W = W
        self.k = k
        self.tau = tau
        self.simulationCount = 0
        self.C = C
        self.delta = delta
        self.Z_prime = Z_prime
        self.tasks = [(Z_prime, 0)]
        self.maxHorizon = maxHorizon
        self.multiplier = multiplier
        self.sens_patterns = sens_patterns
        self.non_sen_w = self.collect_non_sen(W, k)

    def collect_non_sen(self, str, k):
        non_sens = [str[i:i + k] for i in range(len(str) - k + 1) if '#' not in str[i:i + k]]
        pattern_freq = dict.fromkeys(set(non_sens), 0)
        for non_sen in non_sens:
            pattern_freq[non_sen] += 1
        return pattern_freq

    def reinstate_sens(self, F):
        for i in F.keys():
            if i in self.sens_patterns:
                return float('inf')
            else:
                continue
        return 0

    def check_spurious(self, freq_Z, freq_W):
        return True if freq_W < self.tau < freq_Z or freq_Z < self.tau < freq_W else False

    def split(self, str, non_sens_Z, delete_index):
        if delete_index - self.k < 0:
            before_delete = str[0: delete_index + self.k]
            after_delete = str[0:delete_index] + str[delete_index + 1:delete_index + self.k]

        else:
            before_delete = str[delete_index - self.k + 1:delete_index + self.k]
            after_delete = str[delete_index - self.k + 1:delete_index] + str[delete_index + 1:delete_index + self.k]
        non_sens_before = self.collect_non_sen(before_delete, self.k)
        non_sens_after = self.collect_non_sen(after_delete, self.k)
        total_keys = list(non_sens_after.keys()) + list(non_sens_before.keys())
        SP = []
        NSP = []
        for key in total_keys:
            if self.check_spurious(freq_Z=get_value(non_sens_Z, key),
                                   freq_W=get_value(self.non_sen_w, key)):
                SP.append(key)
            else:
                NSP.append(key)
        GLShift = dict.fromkeys(SP)
        OShift = dict.fromkeys(NSP)
        for key in total_keys:
            val = get_value(non_sens_after, key) - get_value(non_sens_before, key)
            distance = get_value(non_sens_Z, key) - get_value(self.non_sen_w, key)
            distance = abs(distance) - abs(distance + val)
            if key in GLShift:
                GLShift[key] = distance
            else:
                OShift[key] = distance
        w_0 = np.sum(list(GLShift.values()))
        w_1 = np.sum(list(OShift.values()))
        cost = -w_0 + self.multiplier * -w_1 + self.reinstate_sens(non_sens_after)  # distortion increase
        return cost

    def BA_ALGO(self, theta):
        tour = [self.Z_prime]
        Z = self.Z_prime
        shortest_distance = 0
        for i in range(self.delta):
            scores = dict.fromkeys(range(self.k - 1, len(Z)))
            non_sensitive_patterns_z = self.collect_non_sen(Z, self.k)
            for j in range(len(Z)):
                score = self.split(str=Z, delete_index=j, non_sens_Z=non_sensitive_patterns_z)
                scores[j] = score
            if min(scores.values()) < theta:
                shortest_distance += min(scores.values())
                best_delete_index = min(scores, key=lambda k: scores[k])
                Z = Z[:best_delete_index] + Z[best_delete_index + 1:]
                tour.append(Z)
        return tour, shortest_distance

    def EX_ALGO(self, Z, delta):
        arr = []
        new_Z = Z
        length = len(Z)
        for delete in range(delta):
            arr.append(list(range(length)))
            length -= 1
        n = delta
        # to keep track of next element
        # in each of the n arrays
        indices = [0 for i in range(n)]
        best_result = None
        best_score = 0
        while 1:
            # prcurrent combination
            cost_sum = 0
            for i in range(n):
                delete_index = arr[i][indices[i]]
                cost, weight = self.split(str=new_Z, non_sens_Z=self.collect_non_sen(new_Z, self.k),
                                          delete_index=delete_index)
                cost_sum += cost
                new_Z = convert_to_string(delete_index, new_Z)
            if cost_sum < best_score:
                best_score = cost_sum
                print(best_score)
                best_result = new_Z
            new_Z = Z
            next = n - 1
            while next >= 0 and indices[next] + 1 >= len(arr[next]):
                next -= 1
            if next < 0:
                return best_result, best_score
            indices[next] += 1
            for i in range(next + 1, n):
                indices[i] = 0

    def RandomDeletePlan(self, currentSchedulePlan):
        if len(currentSchedulePlan) > self.delta:
            return currentSchedulePlan
        global finalPlan
        finalPlan = currentSchedulePlan
        readyTask = self.possible_delete(currentSchedulePlan)
        if len(readyTask) > 0:
            taskToSchedule = random.choice(readyTask)
            currentSchedulePlan = self.update_plan(taskToSchedule, currentSchedulePlan)
            currentSchedulePlan = self.RandomDeletePlan(currentSchedulePlan)
        return finalPlan


    def possible_delete(self,plan):
        current_str = plan[-1][0]
        if len(plan) <= self.delta:
            scores = []
            for i in range(len(current_str)):
                cost = self.split(delete_index=i, str=current_str,
                                    non_sens_Z=self.collect_non_sen(k=self.k, str=current_str))

                new_task = current_str[:i] + current_str[i + 1:]
                scores.append((new_task, cost))

            if len(scores) > 0:
                # alpha-beta pruning
                scores.sort(key=lambda x: x[1])

                early = scores[0][1]
                latest = early + self.maxHorizon
                scores = list(filter(lambda f: f[1] <= latest, scores))

            return scores
        else:
            return []

    def update_plan(self,task, currentSchedulePlan):
        current = copy.deepcopy(currentSchedulePlan)
        current.append(task)
        return current


    def MCST_ALGO(self,currentPlan):
        global nodeIndex
        print('yes')
        nodeIndex = 1
        # Retrieves the maximum number of rollouts per decision
        simulationDepth = 100

        # Copies the current state
        currentPlanCopy = copy.deepcopy(currentPlan)

        # Check if there is any task to be scheduled...
        possibleTasks = self.possible_delete(currentPlanCopy)

        if len(possibleTasks) == 0:
            # Review this
            return currentPlanCopy
        else:
            # There is at least one task still to be scheduled
            # Creates the Monte Carlo tree object from the current state of the scheduling plan
            mctsTree = MCTStree()

            # Creates the first node with unscheduled tasks, parent is 0 (root level)
            rootNode = MCTSnodeUCT(currentPlanCopy)
            rootNode.parent = 0
            rootNode.index = nodeIndex
            mctsTree.nodes.append(rootNode)

            # Children can be added, so the parent will not be a leaf mode anymore
            rootNode.children = True
            # Schedule each task and add to the MCTS list, expanding it for the first time
            mctsTree = self.expandMCTSnode(mctsTree, rootNode)
            # Iterates through the tree simulationDepth times. Not all of them will result in rollouts, because in some cases a cycle will be used to expand a node, leaving
            # the simulation/rollout step for the next cycle. Something to take care of later, but not required for our early experiments
            for _ in range(simulationDepth):
                mctsTree = self.MCTSagentUCTcycle(mctsTree)

            # Now that a full tree search has been completed, select the node below the initial root node (parent = 1 or first node)
            minAverage = float("inf")
            for node in mctsTree.nodes:
                # One of the decision nodes
                if node.parent == 1:
                    if node.numberVisits == 0: continue
                    average = node.accumulatedFinish / node.numberVisits
                    if average < minAverage:
                        minAverage = average
                        bestNode = node

            optimizedPlan = bestNode.plan
            print(optimizedPlan)
            # Repeat until a terminal state (no more tasks to schedule) is reached
            return self.MCST_ALGO(optimizedPlan)


    # Agent that executes a single MCTS tree search cycle from seletion, expansion if needed, simulation and backpropagation
    def MCTSagentUCTcycle(self,mctsTree):

        # ---------------
        # MCTS Selection
        # Traverses the tree starting from the root node (node index=1), with a policy based on UCT evaluation
        parentNodeIndex = 1

        # Start traversing the tree from the parent node of the current simulation
        # I am placing returns (mctsNodeFocus and mctsNodeExpand) on global variables for ease of implementation only.
        # Not proud of it and will do this right later if time permits. If you are reading this, I had no time... but it works just fine.

        mctsNodeFocus, mctsNodeExpand = self.mctsSelection(mctsTree, parentNodeIndex)

        # ---------------
        # MCTS Expansion
        # Expansion is needed if the leaf node to process has been already sampled
        if mctsNodeExpand:
            mctsTree = self.expandMCTSnode(mctsTree, mctsNodeFocus)
            return mctsTree
        else:
            # ---------------
            # MCTS Simulation
            # With a node to expand selected, do a rollout and update the tree
            # With the chosen node, do a rollout and compute metrics
            nodePlan = copy.deepcopy(mctsNodeFocus.plan)
            randomSimulatedPlan = self.RandomDeletePlan(nodePlan)
            lastTaskFinish = np.sum([i[1] for i in randomSimulatedPlan])
            self.simulationCount += 1

            # ---------------------
            # MCTS Backpropagation
            self.MCTSbackpropagate(mctsTree, mctsNodeFocus, lastTaskFinish)
            return mctsTree


    # Returns a node to either rollout a full simulation for or expand (node + expansionFlag)
    def mctsSelection(self,mctsTree, parentNodeIndex):
        global mctsNodeFocus
        global mctsNodeExpand

        # Initializes UCT
        minUCT = - float("inf")
        hasChildren = False

        # Scans all children nodes
        for node in mctsTree.nodes:

            if node.parent == parentNodeIndex:
                hasChildren = True
                # This is a node to evaluate
                if node.numberVisits == 0:
                    # Unvisited child node, return it immediately for a rollout (simulation)
                    mctsNodeFocus = node
                    mctsNodeExpand = False
                    return mctsNodeFocus, mctsNodeExpand
                else:
                    # Compute UCT metrics for the node
                    nodeUCT = self.computeUCT(node, mctsTree.nodes)
                    if nodeUCT > minUCT:
                        minUCT = nodeUCT
                        bestNode = node

        # If the parent node has children, it is not a leaf mode and the first unvisited child has been returned for a rollout or the child with best UCT was selected for expansion
        if hasChildren:
            nextParentIndex = bestNode.index
            # Drill down further
            self.mctsSelection(mctsTree, nextParentIndex)
        else:
            # Parent node has no children, so it is a leaf node that needs expansion
            # Selects the parent node and spits it back for expansion
            for node in mctsTree.nodes:
                if node.index == parentNodeIndex:
                    parentNode = node
                    mctsNodeFocus = parentNode
                    mctsNodeExpand = True
                    break
        return mctsNodeFocus, mctsNodeExpand


    # Expands a leaf node
    def expandMCTSnode(self,mctsTree, mctsNode):
        global nodeIndex
        # Before calling the first MCTS iteration, since this is a root node from which an Action needs to be chosen, we need to populate the tree with possible actions
        possibleTasks = self.possible_delete(mctsNode.plan)
        # Schedule each task and add to the MCTS list
        if len(possibleTasks) > 0:

            # Children will be added, so the node being expanded is obviously not a leaf node anymore
            mctsNode.children = True

            # Check every task on the current plan
            for task in possibleTasks:
                # Schedule the task and get a new plan
                taskScenario = self.update_plan(task, mctsNode.plan)
                # Upon scheduling the task, the plan becomes a new node and can be added to the list of MCTS sims
                newMctsNode = MCTSnodeUCT(taskScenario)
                newMctsNode.parent = mctsNode.index
                nodeIndex += 1
                newMctsNode.index = nodeIndex
                mctsTree.nodes.append(newMctsNode)
        return mctsTree


    # Backpropagates results from a given Node to its parents on a Tree
    def MCTSbackpropagate(self,mctsTree, mctsNode, result):
        mctsNode.numberVisits += 1
        mctsNode.accumulatedFinish += result
        parent = mctsNode.parent
        # Root node, no need to continue backpropagation
        if parent == 0:
            return
        else:
            for node in mctsTree.nodes:
                if node.index == parent:
                    break
            # Found the parent node, backpropagate results to it as well
            self.MCTSbackpropagate(mctsTree, node, result)


    # Computes MCTS UCT metrics for a given node in an MCTS tree
    def computeUCT(self,node, nodes):
        # Pass this value later
        c = self.C

        # Find the parent first
        index = node.parent
        for parentNode in nodes:
            if parentNode.index == index:
                parentN = parentNode.numberVisits
                break

        # We are minimizing values my maximizing UCT, so Vi is negative
        UCT = - node.accumulatedFinish / node.numberVisits + c * math.sqrt(math.log(parentN) / node.numberVisits)
        return UCT

    def meaure_performance(self, Z):
        WNS = self.non_sen_w
        ZNS = self.collect_non_sen(Z, self.k)
        patterns = set(list(WNS.keys()) + list(ZNS.keys()))
        distortion = 0
        ghostsAndLosts = 0
        for key in patterns:
            if self.check_spurious(freq_Z=get_value(ZNS, key),
                                   freq_W=get_value(self.non_sen_w, key)):
                ghostsAndLosts += abs(get_value(WNS, key) - get_value(ZNS, key))
                continue
            else:
                distortion += abs(get_value(WNS, key) - get_value(ZNS, key))
        return ghostsAndLosts, distortion
# See PyCharm help at https://www.jetbrains.com/help/pycharm/

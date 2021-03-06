import copy
import random
import numpy as np
import math
from main import CSD_PLUS
from scheduling import MCTSnodeUCT, MCTStree



# Easy random scheduler that picks up any available task and schedules it

# def MCTS(solver,W):

# Recursive function that randomly schedules a full plan based on task policy, also used for MCTS rollouts




class MCTS:
    def __init__(self, W, k, Z, C,sensitive_patterns, multiplier, tau, delta,maxHorizon):
        self.simulationCount = 0
        self.C = C
        self.solver = CSD_PLUS(W=W, sens_patterns=sensitive_patterns, k=k, multiplier=multiplier, tau=tau)
        self.delta = delta
        self.tasks = [(Z,0)]
        self.maxHorizon = maxHorizon

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
                cost = self.solver.split(delete_index=i, str=current_str,
                                    non_sens_Z=self.solver.collect_non_sen(k=k, str=current_str))

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


    def montecarloschedulerUCT(self,currentPlan):
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
            return self.montecarloschedulerUCT(optimizedPlan)


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

W = 'ccedbbbbbbabbabbccbc'
Z = 'ccadbacbdedabbbababbabbcba'
k = 4

solver = CSD_PLUS(W=W,Z_prime=Z,maxHorizon=3,delta=5,C=200, sens_patterns=['cced', 'ccbc'], k=k, multiplier=1, tau=2)

solver.MCST_ALGO(solver.tasks)
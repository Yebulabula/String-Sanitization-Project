import numpy as np
from main import CSD_PLUS
import random
import math
import struct
from threading import Thread


def normalization(data):
    _range = np.max(data) - np.min(data)
    return (data - np.min(data)) / _range if _range != 0 else [0] * len(data)


def convert_to_string(index, str):
    return str[:index] + str[index + 1:]


def distance(start, delete_index):
    non_sens_z = solver.collect_non_sen(start, 3)
    return solver.split(str=start,
                        delete_index=delete_index,
                        non_sens_Z=non_sens_z)


class ANR_ALGO:
    class ant(Thread):
        def __init__(self, init_location, id_to_key, pheromone_map, distance_callback, alpha, beta, delta=5,
                     first_pass=False):
            Thread.__init__(self)
            self.init_location = init_location
            self.location = init_location
            self.id_to_key = id_to_key
            self.possible_locations = list(range(len(self.location)))
            self.route = []
            self.distance_traveled = 0.0
            self.pheromone_map = pheromone_map
            self.distance_callback = distance_callback
            self.delta = delta
            self.alpha = alpha
            self.beta = beta
            self.tour_complete = False
            self.first_pass = first_pass

        def _update_distance(self, start, delete_index):
            self.distance_traveled += float(self.distance_callback(start, delete_index))

        def _pick_path(self):
            if self.first_pass:
                return random.choice(self.possible_locations)
            attractiveness = [0] * len(self.possible_locations)
            for possible_location in self.possible_locations:
                distance = float(self.distance_callback(self.location, possible_location))
                start = self.id_to_key[self.location]
                pheromone_value = float(self.pheromone_map[start][possible_location])
                if distance == 0:
                    attractiveness[possible_location] = 0.0
                else:
                    attractiveness[possible_location] = pheromone_value * pow(1, self.alpha) + -distance * pow(2,self.beta)
            attractiveness = normalization(attractiveness)
            sum_total = float(np.sum(attractiveness))

            if sum_total == 0.0:
                # increment all zero's, such that they are the smallest non-zero values supported by the system
                # source: http://stackoverflow.com/a/10426033/5343977
                def next_up(x):

                    # NaNs and positive infinity map to themselves.
                    if math.isnan(x) or (math.isinf(x) and x > 0):
                        return x

                    # 0.0 and -0.0 both map to the smallest +ve float.
                    if x == 0.0:
                        x = 0.0

                    n = struct.unpack('<q', struct.pack('<d', x))[0]

                    if n >= 0:
                        n += 1
                    else:
                        n -= 1
                    return struct.unpack('<d', struct.pack('<q', n))[0]

                for key in attractiveness:
                    attractiveness[key] = next_up(attractiveness[key])
                sum_total = next_up(sum_total)

            toss = random.uniform(0,1)
            cumulative = 0
            for i in range(len(attractiveness)):
                weight = (attractiveness[i] / sum_total)
                if toss <= weight + cumulative:
                    return i
                cumulative += weight

            return random.choice(self.possible_locations)

        def _update_route(self, current, visit):
            self.route.append((current, visit))

        def _get_route(self):
            if self.tour_complete:
                return self.route
            else:
                return None

        def _get_distance_traveled(self):
            if self.tour_complete:
                return self.distance_traveled
            else:
                return None

        def _visit_next(self, current, delete_index):
            self._update_route(current, delete_index)
            self._update_distance(current, delete_index)
            self.location = convert_to_string(delete_index, current)
            self.possible_locations = list(range(len(self.location)))

        def run(self):
            for i in range(self.delta):
                next_delete_index = self._pick_path()
                self._visit_next(self.location, next_delete_index)
            # Complete traversal process
            self.tour_complete = True

    def __init__(self, nodes, Z, shortest, distance_callback, ant_count=20, alpha=0.5, beta=1.5, delta=5,
                 pheromone_evaporation_coefficient=.70, pheromone_constant=5.0, iterations=100):
        self.nodes = nodes
        self.start = Z
        self.nodes_dict = {}
        self.distance_matrix = self._int_values(nodes)
        self.pheromone_map = self._int_values(nodes)
        self.ant_updated_pheromone_map = self._int_values(nodes)
        self.distance_callback = distance_callback
        self.ant_count = ant_count
        self.alpha = float(alpha)
        self.beta = float(beta)
        self.delta = delta
        self.pheromone_evaporation_coefficient = pheromone_evaporation_coefficient
        self.pheromone_constant = pheromone_constant
        self.iterations = iterations
        self.shortest_distance = None
        self.first_pass = True
        self.ants = self._init_ants(self.start)
        self.shortest_path_seen = None

    def _int_values(self, nodes):
        ret = []
        for row in range(len(nodes)):
            self.nodes_dict.update({nodes[row]: row})
            ret.append([float(0.0) for x in range(len(nodes[row]))])
        return ret

    def _init_ants(self, start):
        if self.first_pass:
            return [self.ant(start, self.nodes_dict, self.pheromone_map, self._get_distance,
                             self.alpha, self.beta, self.delta, first_pass=True) for x in range(self.ant_count)]
            # else, just reset them to use on another pass
        for ant in self.ants:
            ant.__init__(start, self.nodes_dict, self.pheromone_map, self._get_distance, self.alpha, self.beta,
                         self.delta)

    def _get_distance(self, start, end):
        distance = self.distance_callback(start, end)
        if start not in self.nodes_dict.keys():
            self.nodes_dict.update({start: len(self.nodes_dict)})
            self.ant_updated_pheromone_map.append([0.0] * len(start))
            self.distance_matrix.append([0.0] * len(start))
            self.pheromone_map.append([0.0] * len(start))
        self.distance_matrix[self.nodes_dict[start]][end] = distance
        return self.distance_matrix[self.nodes_dict[start]][end]

    def _update_pheromone_map(self):
        for row in range(len(self.pheromone_map)):
            for col in range(len(self.pheromone_map[row])):
                # decay the pheromone value at this location
                # tau_xy <- (1-rho)*tau_xy	(ACO)
                self.pheromone_map[row][col] = (1 - self.pheromone_evaporation_coefficient) * \
                                               self.pheromone_map[row][col]
                self.pheromone_map[row][col] += self.ant_updated_pheromone_map[row][col]

    def _populate_ant_updated_pheromone_map(self, ant):
        route = ant._get_route()
        for location in route:
            row = self.nodes_dict[location[0]]
            col = location[1]
            current_value = float(self.ant_updated_pheromone_map[row][col])
            if ant._get_distance_traveled() == 0:
                new_pheromone_value = 0.0
            else:
                new_pheromone_value = - ant._get_distance_traveled() / self.pheromone_constant
            self.ant_updated_pheromone_map[row][col] = current_value + new_pheromone_value


    def _get_optimal(self):
        iterate = 0
        i = 0
        for iteration in range(self.iterations):
            for ant in self.ants:
                ant.start()

            for ant in self.ants:
                ant.join()

            best_iterate = 0
            if best_iterate > 50:
                continue

            if iterate > 2000:
                break

            for ant in self.ants:
                i += 1
                self._populate_ant_updated_pheromone_map(ant)
                if not self.shortest_distance:
                    self.shortest_distance = ant._get_distance_traveled()
                # print(ant._get_distance_traveled())
                if not self.shortest_path_seen:
                    self.shortest_path_seen = ant._get_route()
                # if we see a shorter path, then save for return
                if ant._get_distance_traveled() < self.shortest_distance:
                    self.shortest_distance = ant._get_distance_traveled()
                    print(self.first_pass)
                    print(self.shortest_distance)
                    self.shortest_path_seen = ant._get_route()
                    iterate = 0
                    best_iterate = 0
                else:
                    best_iterate += 1
                    iterate += 1

            self._update_pheromone_map()

            if self.first_pass:
                self.first_pass = False

            self._init_ants(self.start)
            for row in range(len(self.ant_updated_pheromone_map)):
                self.ant_updated_pheromone_map[row] = [0.0] * len(self.ant_updated_pheromone_map[row])
        return self.shortest_path_seen


W = 'abbabbabbababaababbabbabbbbababb'
Z = 'bbababbbabbabaabbabbbabbababbbbb'
k = 3
solver = CSD_PLUS(W=W, sens_patterns=[], k=k, multiplier=0.5, tau=2)
ans, shortest = solver.BA_ALGO(delta=3, theta=100, Z=Z)
non_sens_w = solver.non_sen_w
runner = ANR_ALGO(Z=Z, distance_callback=distance, nodes=ans, shortest=None, delta=3)
answer = runner._get_optimal()
print(ans)
yes = convert_to_string(index=answer[-1][1], str=answer[-1][0])

print()
print('++++ANR-ALGO+++++')
print('ANR-ALGO: distortion', solver.measure_distortion(Z=yes))
print('ANR-ALGO: tua-ghosts & tau-losts', solver.count_spurious_patterns(Z=yes))

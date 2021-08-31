import csv
from operator import truediv
import networkx as nx
from queue import Queue
from datetime import datetime

from validation import Validation
from constant import THRESHOLD_VALUE_FIND_GRAPH


class Graph:
    def __init__(self):
        self.graph = nx.MultiGraph()
        self.base_time_list = []

    def import_graph(self):
        graph = self.graph
        with open('data/entity.csv', 'r') as file:
            reader = csv.reader(file, delimiter="|")
            for row in reader:
                graph.add_node(row[0], entity_type='perusahaan tercatat')

        with open('data/other_entity.csv', 'r') as file:
            reader = csv.reader(file, delimiter="|")
            for row in reader:
                graph.add_node(row[0], entity_type='entitas lain')

        with open('data/relation.csv', 'r') as file:
            ignored_relation = ['industri', 'sub industri', 'sub sektor']
            reader = csv.reader(file, delimiter='|')
            for row in reader:
                if row[1] == 'komisaris':
                    subrelation = 'komisaris independen' if (
                        row[3] == 'yes') else 'komisaris terafiliasi'
                    graph.add_edge(
                        row[0], row[2], relation_type=row[1], subrelation_type=subrelation
                    )
                elif row[1] in ignored_relation:
                    continue
                else:
                    graph.add_edge(
                        row[0], row[2], relation_type=row[1], subrelation_type='-')

        with open('data/listing_date.csv', 'r') as file:
            reader = csv.reader(file, delimiter='|')
            for row in reader:
                row[2] = self.convert_timestamp(row[2])
                graph.nodes[row[0]]['enlisting'] = row[2]
                self.base_time_list.append(row[2])
            self.base_time_list = sorted(set(self.base_time_list))

        with open('data/delisting_date.csv', 'r') as file:
            reader = csv.reader(file, delimiter='|')
            for row in reader:
                row[2] = self.convert_timestamp(row[2])
                graph.nodes[row[0]]['delisting'] = row[2]
                self.base_time_list.append(row[2])
            self.base_time_list = sorted(set(self.base_time_list))

    def ignore_relation_by_entity(self, entity_list):
        for (entity, relation_type) in entity_list:
            for neighbor in self.graph.neighbors(entity):
                for (k, v) in self.graph[entity][neighbor].items():
                    if self.graph[entity][neighbor][k]['relation_type'] == relation_type:
                        self.graph[entity][neighbor][k]['disabled'] = True

    def generate_version(self, time_list):
        graph = self.graph
        for node in list(graph.nodes):
            graph.nodes[node]['version'] = []

        for node in list(graph.nodes):
            if('enlisting' in graph.nodes[node]):
                version = time_list.index(
                    graph.nodes[node]['enlisting'])
                graph.nodes[node]['version'].append(version)
            elif (graph.nodes[node]['entity_type'] == 'perusahaan tercatat'):
                print(node, " tidak memiliki enlisting")

            if('delisting' in graph.nodes[node]):
                version = time_list.index(
                    graph.nodes[node]['delisting'])
                graph.nodes[node]['version'].append(version)

    def validity_checking(self, to_file=True):
        if to_file:
            return Validation.validate_to_file(self.graph)
        else:
            return Validation.validate(self.graph)

    def convert_timestamp(self, string_time):
        temp_time = string_time.split()
        if temp_time[1] == 'mei':
            temp_time[1] = 'may'
        elif temp_time[1] == 'ags':
            temp_time[1] = 'aug'
        elif temp_time[1] == 'okt':
            temp_time[1] = 'oct'
        elif temp_time[1] == 'des':
            temp_time[1] = 'dec'
        fixed_string_time = " ".join(temp_time)
        datetime_obj = datetime.strptime(
            fixed_string_time, "%d %b %Y"
        )
        return datetime_obj.strftime('%Y%m%d')

    def convert_to_version(self, time_list, time):
        return time_list.index(time)

    def create_time_list(self, time_start, time_end):
        new_time_list = [*self.base_time_list, time_start, time_end]
        new_time_list = list(set(new_time_list))
        new_time_list.sort()
        version_start = self.convert_to_version(new_time_list, time_start)
        version_end = self.convert_to_version(new_time_list, time_end)
        return new_time_list, version_start, version_end

    def check_node_validity(self, node, current_version):
        graph = self.graph
        xam = -1

        if 'disabled' in graph.nodes[node] and graph.nodes[node]['disabled']:
            return False

        if graph.nodes[node]['entity_type'] != 'perusahaan tercatat':
            return True

        for version in graph.nodes[node]['version']:
            if version <= current_version and xam <= version:
                xam = version
        if ('delisting' in graph.nodes[node] and xam == graph.nodes[node]['delisting']) or xam == -1:
            return False
        else:
            return True

    def check_edge_validity(self, relation_detail):
        if 'disabled' in relation_detail and relation_detail['disabled']:
            return False
        else:
            return True

    def calculate_time_distance(self, time_start, time_end):
        date_format = "%Y%m%d"
        a = datetime.strptime(time_start, date_format)
        b = datetime.strptime(time_end, date_format)
        delta = b - a
        return delta.days

    def calculate_weight(self, version_list, target_version):
        target_version_time = self.calculate_time_distance(
            version_list[target_version], version_list[target_version+1]
        )
        return target_version_time

    def find(self, init_stock, time_start, time_end, K=2):
        time_list, version_start, version_end = self.create_time_list(
            time_start, time_end)
        self.generate_version(time_list)
        enlisting_version = time_list.index(
            self.graph.nodes[init_stock]['enlisting'])
        version_start = max(version_start, enlisting_version)

        q = Queue()
        is_visited = {v: set() for v in self.graph.nodes}
        answer = dict()
        for version in range(version_start, version_end):  # N-1 range
            q.put([init_stock, version, 0])
        while not q.empty():
            [node, current_version, distance] = q.get()
            is_valid = self.check_node_validity(node, current_version)
            if not is_valid or current_version in is_visited[node]:
                continue
            is_visited[node].add(current_version)

            if distance == K:
                if self.graph.nodes[node]['entity_type'] != 'perusahaan tercatat':
                    continue
                elif 'delisting' in self.graph.nodes[node]:
                    delisting_version = self.convert_to_version(
                        time_list, time_start)
                    if delisting_version <= version_end:
                        continue
                weight = self.calculate_weight(time_list, current_version)
                if node in answer:
                    answer[node] += weight
                else:
                    answer[node] = weight
            elif distance > K:
                continue

            for neighbour in self.graph[node]:
                for (k, relation_detail) in self.graph[node][neighbour].items():
                    if self.check_edge_validity(relation_detail):
                        q.put([neighbour, current_version, distance + 1])

        total_time = self.calculate_time_distance(
            time_list[version_start], time_list[version_end]
        )
        aggregated_result = {
            k: v / total_time for (k, v) in answer.items() if v > THRESHOLD_VALUE_FIND_GRAPH * total_time}
        return aggregated_result

    def find_in_max(self, init_stock, time_start, time_end, max_k=2):
        time_list, version_start, version_end = self.create_time_list(
            time_start, time_end)
        self.generate_version(time_list)
        enlisting_version = time_list.index(
            self.graph.nodes[init_stock]['enlisting'])
        version_start = max(version_start, enlisting_version)

        q = Queue()
        is_visited = {v: set() for v in self.graph.nodes}
        answer_by_distance = [dict() for i in range(max_k+1)]

        for version in range(version_start, version_end):  # N-1 range
            q.put([init_stock, version, 0])

        while not q.empty():
            [node, current_version, distance] = q.get()
            is_valid = self.check_node_validity(node, current_version)
            if not is_valid or current_version in is_visited[node]:
                continue
            is_visited[node].add(current_version)

            if distance <= max_k and self.graph.nodes[node]['entity_type'] == 'perusahaan tercatat':
                if 'delisting' in self.graph.nodes[node]:
                    delisting_version = self.convert_to_version(
                        time_list, time_start)
                    if delisting_version > version_end:
                        weight = self.calculate_weight(
                            time_list, current_version)
                        if node in answer_by_distance[distance]:
                            answer_by_distance[distance][node] += weight
                        else:
                            answer_by_distance[distance][node] = weight
                else:
                    weight = self.calculate_weight(time_list, current_version)
                    if node in answer_by_distance[distance]:
                        answer_by_distance[distance][node] += weight
                    else:
                        answer_by_distance[distance][node] = weight
            elif distance > max_k:
                continue

            for neighbour in self.graph[node]:
                for (k, relation_detail) in self.graph[node][neighbour].items():
                    if self.check_edge_validity(relation_detail):
                        q.put([neighbour, current_version, distance + 1])

        total_time = self.calculate_time_distance(
            time_list[version_start], time_list[version_end]
        )
        aggregated_result = [{
            k: v / total_time for (k, v) in answer.items() if v > THRESHOLD_VALUE_FIND_GRAPH * total_time}
            for answer in answer_by_distance
        ]
        return aggregated_result

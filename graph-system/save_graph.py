import pickle
import numpy as np
import csv
import pandas as pd
import math
from graph import Graph
from evaluation import evaluate
from tqdm import tqdm


def initialize_stock_list():
    stocks = []
    with open('data/entity.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            stocks.append(row[0])
    return stocks


def initialize_ignored_stock_list():
    stocks = []
    with open('data/delisted_entity.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            stocks.append(row[0])

    with open('data/ignored_stock.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            stocks.append(row[0])
    stocks = list(set(stocks))
    return stocks


def write_to_file(data, company):
    dump_file = open(f"graph_result/{company}.obj", "wb")
    pickle.dump(data, dump_file)


def cut_array_from(stock_list, stock):
    idx = stock_list.index(stock)
    stock_list = stock_list[idx:]
    return stock_list


if __name__ == '__main__':
    time_start = "20170101"
    time_end = "20201231"
    max_distance = 10
    stock_list = initialize_stock_list()
    stock_list = cut_array_from(stock_list, "PLAN")
    ignored_stock_list = initialize_ignored_stock_list()
    ignored_relation = [
        ('yuliana', 'direktur'),
        ('santoso', 'direktur'),
        ('suwandi', 'direktur'),
        ('suryadi', 'direktur'),
        ('rudiantara', 'komisaris'),
        ('ervina', 'komite audit'),
        ('marhaendra', 'komisaris'),
        ('akbar', 'komite audit')
    ]
    graph = Graph()
    graph.import_graph()
    graph.ignore_relation_by_entity(ignored_relation)

    for stock in tqdm(stock_list):
        if stock in ignored_stock_list:
            continue
        stock_result = []
        stock_subset = graph.find_in_max(
            stock, time_start, time_end, max_distance)
        write_to_file(stock_subset, stock)

import numpy as np
import csv
import pandas as pd
import random
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


def extract_evaluation(stock_evaluation):
    stock_evaluation = [
        i for i in stock_evaluation if not math.isnan(i['correlation'])]
    if(len(stock_evaluation) == 0):
        return {"max": 0, "min": 0, "avg": 0, "median": 0, "count": 0}
    count = len(stock_evaluation)
    stock_evaluation = stock_evaluation[:5]
    value = np.array([abs(i['correlation']) for i in stock_evaluation])
    return {"max": np.amax(value), "min": np.amin(value), "avg": np.average(value), "median": np.median(value), "count": count}


if __name__ == '__main__':
    time_start = "20170101"
    time_end = "20201231"
    stock_list = initialize_stock_list()
    ignored_stock_list = initialize_ignored_stock_list()
    stock_list = [x for x in stock_list if x not in ignored_stock_list]
    stock_num = [i for i in range(1, 101)]

    graph = Graph()
    graph.import_graph()
    all_result = []
    for num in tqdm(stock_num):
        stock_result = []
        ctr = 1000
        while ctr > 0:
            stock_subset = random.sample(stock_list, num+1)
            stock = stock_subset[-1]
            stock_subset.pop()
            stock_evaluation = evaluate(
                stock, stock_subset, time_start, time_end)
            if(len(stock_evaluation) == 0):
                continue
            data = extract_evaluation(stock_evaluation)
            if(data['count'] == 0 or math.isnan(data["max"]) or data['max'] == 0):
                continue
            ctr -= 1
            stock_result.append(data)
        df = pd.DataFrame(stock_result)
        all_result.append(df.median())
    all_result = pd.DataFrame(all_result)
    all_result.to_csv("output/output_subset_naive/overall.csv")

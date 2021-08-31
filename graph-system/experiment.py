import pickle
import numpy as np
import csv
import pandas as pd
import math
import random
import pprint

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
    # stock_evaluation = stock_evaluation[:5]
    # stock_evaluation = random.sample(stock_evaluation, 5) if len(
    #    stock_evaluation) > 5 else stock_evaluation
    value = np.array([abs(i['correlation']) for i in stock_evaluation])
    return {"max": np.amax(value), "min": np.amin(value), "avg": np.average(value),  "median": np.median(value), "count": count}


def write_to_file(data, company):
    df = pd.DataFrame(data)
    df.to_csv(f"output/output_all_val/{company}.csv")


def cut_array_from(stock_list, stock):
    idx = stock_list.index(stock)
    stock_list = stock_list[idx:]
    return stock_list


def get_subset_from_file(company):
    dump_file = open(f"graph_result/{company}.obj", "rb")
    return pickle.load(dump_file)


if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=4)

    time_start = "20170101"
    time_end = "20201231"
    max_distance = 10
    stock_list = initialize_stock_list()
    stock_list = cut_array_from(stock_list, "PLAN")
    ignored_stock_list = initialize_ignored_stock_list()

    for stock in tqdm(stock_list):
        if stock in ignored_stock_list:
            continue
        stock_result = []
        # stock_subset = graph.find_in_max(
        #    stock, time_start, time_end, max_distance)
        stock_subset = get_subset_from_file(stock)
        for i in range(2, max_distance+1, 2):
            stock_evaluation = evaluate(
                stock, stock_subset[i], time_start, time_end)
            stock_result.append(extract_evaluation(stock_evaluation))
        write_to_file(stock_result, stock)

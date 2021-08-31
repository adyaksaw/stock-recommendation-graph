from graph import Graph
from evaluation import evaluate
import pickle
import pprint

if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=4)
    graph = Graph()
    graph.import_graph()
    warnings = graph.validity_checking()

    while True:
        stock = input("Masukan saham yang dimiliki\n")
        time_start, time_end = input(
            "Masukan rentang waktu dalam format YYYYMMDD YYYYMMDD\n").split()
        #stock = "UVCR"
        #time_start = "20170101"
        #time_end = "20201231"
        print("START FIND")
        stock_result = graph.find(stock, time_start, time_end, 6)
        pp.pprint(stock_result)
        print("START EVALUATION")
        stock_evaluation = evaluate(stock, stock_result, time_start, time_end)

        pp.pprint(stock_evaluation)
        break

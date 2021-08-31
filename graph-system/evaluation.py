import yfinance as yf
from numpy import corrcoef
from constant import THRESHOLD_VALUE_EVALUATION_SIMILARITY
import pickle

dump_file = open("data/stock_price.obj", "rb")
price_list = pickle.load(dump_file)
price_list = {idx: gp.xs(idx, level=0, axis=1).dropna()
              for idx, gp in price_list.groupby(level=0, axis=1)}


def get_price(stock_id, date_first, date_last):
    return price_list[f'{stock_id}.JK'][date_first:date_last].Close


def get_correlation_value(data_a, data_b):
    intersection_keys = data_a.index & data_b.index
    if len(data_a) * THRESHOLD_VALUE_EVALUATION_SIMILARITY < len(intersection_keys):
        return [
            True,
            corrcoef(data_a[intersection_keys],
                     data_b[intersection_keys])[0][1]
        ]
    else:
        return [False, 0]


def get_correlation_value2(data_a, data_b):
    intersection_keys = data_a.index & data_b.index
    if len(data_a) * THRESHOLD_VALUE_EVALUATION_SIMILARITY < len(intersection_keys):
        return [
            True,
            corrcoef(data_a[intersection_keys],
                     data_b[intersection_keys])[0][1]
        ]
    else:
        return [False, 0]


def evaluate(stock_main, stock_result, date_first, date_last):
    evaluation_result = []

    main_prices = get_price(stock_main, date_first, date_last)
    for stock in stock_result:
        stock_prices = get_price(stock, date_first, date_last)

        [valid, correlation_value] = get_correlation_value(
            main_prices, stock_prices)
        if valid:
            evaluation_result.append(
                {"stock": stock, "correlation": correlation_value}
            )
    evaluation_result = sorted(
        evaluation_result, key=lambda k: abs(k['correlation'])
    )
    return evaluation_result

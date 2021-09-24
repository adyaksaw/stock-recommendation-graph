from math import log
import yfinance as yf
from numpy import corrcoef
from constant import THRESHOLD_VALUE_EVALUATION_SIMILARITY
import pickle

dump_file = open("data/stock_price.obj", "rb")
price_list = pickle.load(dump_file)
price_list = {idx: gp.xs(idx, level=0, axis=1).dropna()
              for idx, gp in price_list.groupby(level=0, axis=1)}

dump_corr = open("data/correlation.obj", "rb")
corr_list = pickle.load(dump_corr)

precalc = {}
precalc_time_start = "20170101"
precalc_time_end = "20201231"


def fill_precalc():
    for st in price_list:
        precalc[st] = (price_list[st][precalc_time_start:precalc_time_end].Close -
                       price_list[st][precalc_time_start:precalc_time_end].Open) / 100


def get_price(stock_id, date_first, date_last):
    # if(date_first == precalc_time_start and date_last == precalc_time_end):
    #    return precalc[f'{stock_id}.JK']
    temp = price_list[f'{stock_id}.JK'][date_first:date_last].Close / \
        price_list[f'{stock_id}.JK'][date_first:date_last].Open
    temp = temp.apply(lambda x: log(x))
    return temp


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
        if date_first == precalc_time_start and date_last == precalc_time_end:
            if(stock in corr_list[stock_main]):
                correlation_value = corr_list[stock_main][stock]
                if(correlation_value is not None):
                    evaluation_result.append(correlation_value)
        else:
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


if __name__ == '__main__':
    print(evaluate('AALI', ['ACST', 'ACES', 'ADES',
                            'ADHI', 'ADMF'], '20170101', '20201231'))

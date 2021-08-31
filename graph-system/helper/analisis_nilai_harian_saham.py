import pickle
import numpy as np
from datetime import datetime
import csv


def convert_timestamp(string_time):
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


def import_stock_time_data():
    stock_time_data = dict()
    with open('../data/listing_date.csv', 'r') as file:
        reader = csv.reader(file, delimiter='|')
        for row in reader:
            row[2] = convert_timestamp(row[2])
            stock_time_data[row[0]] = row[2]
    return stock_time_data


if __name__ == '__main__':
    stock_time_data = import_stock_time_data()
    dump_file = open("../data/stock_price.obj", "rb")
    price_list = pickle.load(dump_file)
    price_list = {idx: gp.xs(idx, level=0, axis=1).dropna()
                  for idx, gp in price_list.groupby(level=0, axis=1)}
    time_start = "20170101"
    time_end = "20210101"
    l = []
    total = 0
    valid = 0
    for (k, v) in price_list.items():
        if(stock_time_data[k.split('.')[0]] >= "20200101"):
            continue
        val = len(v[time_start:time_end].Close)
        l.append(val)
        total += 1
        if val > 751/2:
            valid += 1
        if val < 10:
            print(k)

    l = sorted(l)
    l = np.array(l)
    print(np.median(l))
    print(np.mean(l))
    print(l[len(l)//10 * 2])
    print(valid/total)
    print(l)

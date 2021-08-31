import yfinance as yf
import csv
import pickle

if __name__ == '__main__':
    stocks = ""
    with open('data/entity.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            stocks += f"{row[0]}.JK "
    data = yf.download(stocks, start="2016-01-01",
                       end="2020-12-31", group_by="ticker")
    dump_file = open("data/stock_price.obj", "wb")
    pickle.dump(data, dump_file)

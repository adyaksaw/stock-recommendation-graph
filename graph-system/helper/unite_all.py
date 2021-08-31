import os
import pandas as pd
import numpy as np
from tqdm import tqdm

if __name__ == '__main__':
    foldername = 'output/output_all_noval'
    is_first = True
    total = 0
    invalid = []
    count_stock = [0 for i in range(5)]
    count_total = [0 for i in range(5)]
    avg = [0 for i in range(5)]
    for filename in tqdm(os.listdir(f'../{foldername}/')):
        if filename.endswith('.csv'):
            df = pd.read_csv(os.path.join(
                f'../{foldername}/', filename), index_col=0)
            total += 1
            if(df.loc[1, 'max'] == 0 or df.loc[1].isnull().values.any()):
                invalid.append(filename.split('.')[0])
                continue
            if(is_first):
                df_overall = df
                is_first = False
            else:
                # print(filename, df.loc[1, 'max'])
                for index, row in df.iterrows():
                    if(df.loc[index, 'max'] != 0 and not df.loc[index].isnull().values.any()):
                        count_stock[index] += 1
                        df_overall.loc[index] += df.loc[index]
                        avg[index] += df.loc[index, 'avg'] * \
                            df.loc[index, 'count']
                        count_total[index] += df.loc[index, 'count']
                # print(filename, df_overall)
    for index, row in df_overall.iterrows():
        df_overall.loc[index] /= count_stock[index]
        if count_total[index] != 0:
            avg[index] /= count_total[index]
            print(index, avg[index])
    df_overall.to_csv(f'../{foldername}.csv')

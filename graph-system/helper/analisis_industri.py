import csv
import pprint
from operator import sub

if __name__ == '__main__':
    industri_perusahaan = {}
    subindustri_perusahaan = {}
    with open('../data/relation.csv', 'r') as file:
        reader = csv.reader(file, delimiter='|')
        for row in reader:
            if(row[1] == 'industri'):
                industri_perusahaan[row[0]] = row[2]
            elif(row[1] == 'sub industri'):
                subindustri_perusahaan[row[0]] = row[2]

    print("industri length:", len(industri_perusahaan))
    print("Sub industri length:", len(subindustri_perusahaan))

    industri_subindustri = dict()
    subindustri_industri = dict()

    for (k, v) in industri_perusahaan.items():
        if v not in industri_subindustri:
            industri_subindustri[v] = [subindustri_perusahaan[k]]
        else:
            industri_subindustri[v].append(subindustri_perusahaan[k])

    for (k, v) in subindustri_perusahaan.items():
        if v not in subindustri_industri:
            subindustri_industri[v] = [industri_perusahaan[k]]
        else:
            subindustri_industri[v].append(industri_perusahaan[k])

    for (k, v) in industri_subindustri.items():
        industri_subindustri[k] = list(set(v))

    for (k, v) in subindustri_industri.items():
        subindustri_industri[k] = list(set(v))

    pp = pprint.PrettyPrinter(indent=4)

    pp.pprint(industri_subindustri)
    pp.pprint(subindustri_industri)

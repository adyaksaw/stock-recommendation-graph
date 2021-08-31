import csv
import pprint
from operator import sub

if __name__ == '__main__':
    sektor_perusahaan = {}
    subsektor_perusahaan = {}
    with open('../data/relation.csv', 'r') as file:
        reader = csv.reader(file, delimiter='|')
        for row in reader:
            if(row[1] == 'sektor'):
                sektor_perusahaan[row[0]] = row[2]
            elif(row[1] == 'sub sektor'):
                subsektor_perusahaan[row[0]] = row[2]

    print("Sektor length:", len(sektor_perusahaan))
    print("Sub sektor length:", len(subsektor_perusahaan))

    sektor_subsektor = dict()
    subsektor_sektor = dict()

    for (k, v) in sektor_perusahaan.items():
        if v not in sektor_subsektor:
            sektor_subsektor[v] = [subsektor_perusahaan[k]]
        else:
            sektor_subsektor[v].append(subsektor_perusahaan[k])

    for (k, v) in subsektor_perusahaan.items():
        if v not in subsektor_sektor:
            subsektor_sektor[v] = [sektor_perusahaan[k]]
        else:
            subsektor_sektor[v].append(sektor_perusahaan[k])

    for (k, v) in sektor_subsektor.items():
        sektor_subsektor[k] = list(set(v))

    for (k, v) in subsektor_sektor.items():
        subsektor_sektor[k] = list(set(v))

    pp = pprint.PrettyPrinter(indent=4)

    pp.pprint(sektor_subsektor)
    pp.pprint(subsektor_sektor)

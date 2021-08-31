import csv
import pprint
from operator import sub

if __name__ == '__main__':
    industri_perusahaan = {}
    sektor_perusahaan = {}
    with open('../data/relation.csv', 'r') as file:
        reader = csv.reader(file, delimiter='|')
        for row in reader:
            if(row[1] == 'industri'):
                industri_perusahaan[row[0]] = row[2]
            elif(row[1] == 'sub sektor'):
                sektor_perusahaan[row[0]] = row[2]

    print("sub industri length:", len(industri_perusahaan))
    print("Sub sektor length:", len(sektor_perusahaan))

    industri_sektor = dict()
    sektor_industri = dict()

    for (k, v) in industri_perusahaan.items():
        if v not in industri_sektor:
            industri_sektor[v] = [sektor_perusahaan[k]]
        else:
            industri_sektor[v].append(sektor_perusahaan[k])

    for (k, v) in sektor_perusahaan.items():
        if v not in sektor_industri:
            sektor_industri[v] = [industri_perusahaan[k]]
        else:
            sektor_industri[v].append(industri_perusahaan[k])

    for (k, v) in industri_sektor.items():
        industri_sektor[k] = list(set(v))

    for (k, v) in sektor_industri.items():
        sektor_industri[k] = list(set(v))

    pp = pprint.PrettyPrinter(indent=4)

    pp.pprint(industri_sektor)
    pp.pprint(sektor_industri)

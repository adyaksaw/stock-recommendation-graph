from selenium import webdriver
from ProfilePerusahaanTercatat import ProfilePerusahaanTercatat
import csv


def print_to_file(array, file_name):
    with open(file_name, "w") as txt_file:
        for line in array:
            txt_file.write("".join(line) + "\n")


if __name__ == "__main__":
    browser = webdriver.Chrome(
        executable_path=r"C:\\Users\\adyak\\Project\\TA\\scrapper\\chromedriver_win32\\chromedriver.exe"
    )
    # anggotaBursa = ProfileAnggotaBursa(browser, "idx.co.id")
    # anggotaBursa.fetch_data()
    perusahaan_tercatat = ProfilePerusahaanTercatat(browser, "idx.co.id")
    stock_names = []
    with open("delisted_company.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            stock_names.append([row[0], row[1], row[2]])
    fetched_data = []
    for stock_data in stock_names:
        [stock, enlisting_date, delisting_date] = stock_data
        temp = perusahaan_tercatat.fetch_company(
            f"https://www.idx.co.id/perusahaan-tercatat/profil-perusahaan-tercatat/detail-profile-perusahaan-tercatat/?kodeEmiten={stock}", stock, fetched_data)
        perusahaan_tercatat.insert_relation(
            stock, 'Tanggal Pencatatan', enlisting_date)
        perusahaan_tercatat.insert_relation(
            stock, 'Delisting Date', delisting_date)

    perusahaan_relation, perusahaan_entity = perusahaan_tercatat.relation_list, perusahaan_tercatat.main_entity_list
    print_to_file(perusahaan_relation, "relation_raw.csv")
    print_to_file(perusahaan_entity, "entity.csv")

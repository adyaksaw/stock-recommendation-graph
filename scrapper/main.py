from selenium import webdriver
from ProfileAnggotaBursa import ProfileAnggotaBursa
from ProfilePerusahaanTercatat import ProfilePerusahaanTercatat


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
    perusahaanTercatat = ProfilePerusahaanTercatat(browser, "idx.co.id")
    perusahaan_relation, perusahaan_entity = perusahaanTercatat.fetch_data()
    print_to_file(perusahaan_relation, "relation_raw.csv")
    print_to_file(perusahaan_entity, "entity.csv")

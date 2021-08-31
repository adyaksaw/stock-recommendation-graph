from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Profile import Profile


class ProfilePerusahaanTercatat(Profile):
    def __init__(self, browser, base_url):
        target_url = (
            f"https://{base_url}/perusahaan-tercatat/profil-perusahaan-tercatat/"
        )
        table_num_info = "companyTable_info"

        self.target_attributes = [
            "Sektor",
            "Sub Sektor",
            "Industri",
            "Sub Industri",
            "Tanggal Pencatatan"
        ]

        Profile.__init__(self, browser, target_url, table_num_info)

    def prepare_browser(self, link):
        browser = self.browser
        browser.execute_script("window.open('');")
        browser.switch_to.window(browser.window_handles[1])
        browser.get(link)
        return browser

    def fetch_company(self, link, company_name, fetched_data):
        browser = self.prepare_browser(link)
        data = {}
        try:
            company_profile = browser.find_element(By.TAG_NAME, "dl")
            # WebDriverWait(browser, 20).until(
            #    lambda wd: company_profile.find_element(By.TAG_NAME, "dd")
            #    .find_element(By.TAG_NAME, "span")
            #    .text
            #    != ""
            # )
        except Exception:
            browser.close()
            browser.switch_to.window(browser.window_handles[0])
            return self.fetch_company(link, company_name, fetched_data)

        kode_perusahaan = None

        profile_title = company_profile.find_elements(By.TAG_NAME, "dt")
        profile_description = company_profile.find_elements(By.TAG_NAME, "dd")
        for i in range(len(profile_title)):
            data[profile_title[i].text] = profile_description[i].text
            if profile_title[i].text == "Kode":
                kode_perusahaan = profile_description[i].text

        if kode_perusahaan == "":
            kode_perusahaan = company_name

        self.insert_entity(kode_perusahaan)

        for i in range(len(profile_title)):
            data[profile_title[i].text] = profile_description[i].text
            if profile_title[i].text in self.target_attributes:
                self.insert_relation(
                    kode_perusahaan, profile_title[i].text, profile_description[i].text
                )

        table_list = browser.find_elements(By.TAG_NAME, "tbody")
        for idx, table in enumerate(table_list):
            row_list = table.find_elements(By.TAG_NAME, "tr")
            pemegang_saham = []
            for _, row in enumerate(row_list):
                col_list = row.find_elements(By.TAG_NAME, "td")
                if idx == 0:
                    self.insert_relation(
                        kode_perusahaan, "Sekretaris Perusahaan", col_list[0].text
                    )
                elif idx == 1 or idx == 3:
                    self.insert_relation(
                        kode_perusahaan, col_list[1].text, col_list[0].text
                    )
                elif idx == 2:
                    self.insert_relation(
                        kode_perusahaan, col_list[1].text, col_list[0].text,
                        col_list[2].text.lower()
                    )
                elif idx == 4:
                    if (
                        col_list[1].text != "Lebih dari 5%"
                        or col_list[0].text in pemegang_saham
                    ):
                        continue
                    pemegang_saham.append(col_list[0].text)
                    self.insert_relation(
                        kode_perusahaan, "Pemegang Saham", col_list[0].text
                    )
            if idx >= 5:
                break
        browser.close()
        browser.switch_to.window(browser.window_handles[0])
        return data

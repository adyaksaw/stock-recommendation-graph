from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Profile import Profile


class ProfileAnggotaBursa(Profile):
    def __init__(self, browser, base_url):
        target_url = (
            f"https://{base_url}/anggota-bursa-dan-partisipan/profil-anggota-bursa/"
        )
        table_num_info = "exchangeMemberTable_info"
        Profile.__init__(self, browser, target_url, table_num_info)

    def fetch_company(self, link, company_name, fetched_data):
        browser = self.browser
        browser.execute_script("window.open('');")
        browser.switch_to.window(browser.window_handles[1])
        browser.get(link)
        company_profile = browser.find_element(By.TAG_NAME, "dl")
        data = {}
        try:
            WebDriverWait(browser, 20).until(
                lambda wd: company_profile.find_element(By.TAG_NAME, "dd")
                .find_element(By.TAG_NAME, "span")
                .text
                != ""
            )
        except Exception:
            browser.close()
            browser.switch_to.window(browser.window_handles[0])
            return self.fetch_company(link, company_name, fetched_data)

        profile_title = company_profile.find_elements(By.TAG_NAME, "dt")
        profile_description = company_profile.find_elements(By.TAG_NAME, "dd")
        for i in range(len(profile_title)):
            data[profile_title[i].text] = profile_description[i].text
        browser.close()
        browser.switch_to.window(browser.window_handles[0])
        return data
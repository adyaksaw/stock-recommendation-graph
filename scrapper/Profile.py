from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Profile:
    def __init__(self, browser, target_url, table_num_info):
        self.browser = browser
        self.target_url = target_url
        self.table_num_info = table_num_info
        self.relation_list = []
        self.main_entity_list = []

    def click_feedback_button_if_exist(self):
        browser = self.browser
        feedback_panel = browser.find_elements_by_class_name("feedback_panel")
        if(len(feedback_panel) > 0):
            close_button = feedback_panel[0].find_element(
                By.TAG_NAME, "button")
            disabled_button = close_button.get_attribute("disabled")
            if(disabled_button == None):
                ActionChains(browser).click(close_button).perform()
                return True
            else:
                return False

    def fetch_company(self, link, company_name, fetched_data):
        return fetched_data

    def fetch_row(self, row, fetched_data):
        cells = row.find_elements(By.TAG_NAME, "td")
        company_name = cells[2].find_element(By.TAG_NAME, "a")
        print(f"Collecting company {company_name.text}")
        link = company_name.get_attribute("href")
        fetched_data[company_name.text] = self.fetch_company(
            link, company_name, fetched_data
        )

    def fetch_page(self, page, fetched_data):
        browser = self.browser

        table = browser.find_element(By.TAG_NAME, "tbody")
        table_data = table.find_elements(By.TAG_NAME, "tr")
        print(f"Start fetching page {page}")
        for _, row in enumerate(table_data):
            self.fetch_row(row, fetched_data)

    def fetch_data(self):
        target_url = self.target_url
        browser = self.browser
        browser.get(target_url)
        browser.add_cookie({"name": "skipFeedback", "value": "1"})
        current_last_entry = max_entry = None
        fetched_data = {}
        WebDriverWait(browser, 20).until(
            lambda wd: self._is_page_changed(current_last_entry, max_entry)
        )
        current_last_entry, max_entry = self._fetch_current_entry()
        current_page = 1
        while current_last_entry != max_entry:
            self.fetch_page(current_page, fetched_data)
            try:
                browser.find_element(By.CLASS_NAME, "next").click()
            except Exception:
                self.click_feedback_button_if_exist()
                browser.find_element(By.CLASS_NAME, "next").click()
            current_page += 1
            WebDriverWait(browser, 20).until(
                lambda wd: self._is_page_changed(current_last_entry, max_entry)
            )
            current_last_entry, max_entry = self._fetch_current_entry()
        self.fetch_page(current_page, fetched_data)
        return self.relation_list, self.main_entity_list

    def _is_page_changed(self, current_last_entry, max_entry):
        new_current_last_entry, _ = self._fetch_current_entry()
        return new_current_last_entry != current_last_entry

    def _fetch_current_entry(self):
        try:
            browser = self.browser
            self.click_feedback_button_if_exist()
            table_info = browser.find_element(By.ID, self.table_num_info).text
            table_info = table_info.split(" ")
            current_last_entry = table_info[3]
            max_entry = table_info[5]
            return current_last_entry, max_entry
        except IndexError:
            return None, None

    def insert_relation(self, entity1, relationship, entity2, extra="-"):
        if(entity1 != None and entity1 != "" and entity2 != None and entity2 != ""):
            self.relation_list.append(
                f"{entity1},{relationship},{entity2},{extra}")

    def insert_entity(self, entity):
        self.main_entity_list.append(entity)

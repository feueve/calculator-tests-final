from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage


class DateCalculatorPage(BasePage):
    URL = "https://www.calculator.net/date-calculator.html"

    DIFF_START_MONTH = (By.ID, "today_Month_ID")
    DIFF_START_DAY = (By.ID, "today_Day_ID")
    DIFF_START_YEAR = (By.ID, "today_Year_ID")

    DIFF_END_MONTH = (By.ID, "ageat_Month_ID")
    DIFF_END_DAY = (By.ID, "ageat_Day_ID")
    DIFF_END_YEAR = (By.ID, "ageat_Year_ID")

    DIFF_CALC_BTN = (By.XPATH, "//form[@name='calcf']//input[@value='Calculate']")
    DIFF_RESULT = (By.CSS_SELECTOR, "div.bigtext")

    ADD_START_MONTH = (By.ID, "today2_Month_ID")
    ADD_START_DAY = (By.ID, "today2_Day_ID")
    ADD_START_YEAR = (By.ID, "today2_Year_ID")

    ADD_OP_SELECT = (By.ID, "c2op")
    ADD_YEARS = (By.ID, "c2year")
    ADD_MONTHS = (By.ID, "c2month")
    ADD_WEEKS = (By.ID, "c2week")
    ADD_DAYS = (By.ID, "c2day")

    ADD_CALC_BTN = (By.XPATH, "//form[@name='calcf2']//input[@value='Calculate']")
    ADD_RESULT = (By.XPATH, "//span[contains(@class, 'verybigtext')]")
    ERROR_MSG = (By.XPATH, "//font[@color='red']")

    def open(self):
        self.driver.get(self.URL)
        return self

    def _fill_date(self, month_loc, day_loc, year_loc, month, day, year):
        Select(self.wait.until(EC.visibility_of_element_located(month_loc))).select_by_visible_text(month)
        Select(self.driver.find_element(*day_loc)).select_by_visible_text(str(day))

        year_field = self.wait.until(EC.visibility_of_element_located(year_loc))
        year_field.send_keys(Keys.CONTROL, "a")
        year_field.send_keys(Keys.BACKSPACE)
        year_field.send_keys(str(year))

        self.driver.execute_script("arguments[0].onblur();", year_field)

    def _fill_amount(self, locator, value):
        field = self.wait.until(EC.visibility_of_element_located(locator))
        field.click()
        field.send_keys(Keys.CONTROL, "a")
        field.send_keys(Keys.BACKSPACE)
        field.send_keys(str(value))

    def enter_diff_start_date(self, month, day, year):
        self._fill_date(self.DIFF_START_MONTH, self.DIFF_START_DAY, self.DIFF_START_YEAR, month, day, year)
        return self

    def enter_diff_end_date(self, month, day, year):
        self._fill_date(self.DIFF_END_MONTH, self.DIFF_END_DAY, self.DIFF_END_YEAR, month, day, year)
        return self

    def click_diff_calculate(self):
        self.wait.until(EC.element_to_be_clickable(self.DIFF_CALC_BTN)).click()
        return self

    def get_diff_result(self):
        el = self.wait.until(EC.visibility_of_element_located(self.DIFF_RESULT))
        return el.text.strip()

    def enter_add_start_date(self, month, day, year):
        self._fill_date(self.ADD_START_MONTH, self.ADD_START_DAY, self.ADD_START_YEAR, month, day, year)
        return self

    def set_add_operation(self, operation):
        select = Select(self.wait.until(EC.visibility_of_element_located(self.ADD_OP_SELECT)))
        select.select_by_value(operation)
        return self

    def enter_add_amounts(self, years, months, weeks, days):
        fields = {
            self.ADD_YEARS: years,
            self.ADD_MONTHS: months,
            self.ADD_WEEKS: weeks,
            self.ADD_DAYS: days
        }
        for locator, value in fields.items():
            self._fill_amount(locator, value)
        return self

    def click_add_calculate(self):
        self.wait.until(EC.element_to_be_clickable(self.ADD_CALC_BTN)).click()
        return self

    def get_add_result(self):
        el = self.wait.until(EC.visibility_of_element_located(self.ADD_RESULT))
        return el.text.strip()

    def get_error_message(self):
        el = self.wait.until(EC.visibility_of_element_located(self.ERROR_MSG))
        return el.text.strip()

    def get_diff_start_year_value(self):
        return self.driver.find_element(*self.DIFF_START_YEAR).get_attribute("value")

    def get_add_month_value(self):
        return self.driver.find_element(*self.ADD_MONTHS).get_attribute("value")
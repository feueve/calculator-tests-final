import pytest
import json
from pages.date_calculator_page import DateCalculatorPage

with open("data/date_cases.json", "r") as f:
    DATA = json.load(f)


@pytest.mark.parametrize("case", DATA["diff_cases"])
def test_days_between_two_dates_correct(driver, case):
    page = DateCalculatorPage(driver).open()
    page.enter_diff_start_date(*case["start"])
    page.enter_diff_end_date(*case["end"])
    page.click_diff_calculate()

    result = page.get_diff_result()
    assert case["expected"] in result


def test_days_between_boundary_values(driver):
    page = DateCalculatorPage(driver).open()
    page.enter_diff_start_date("Jan", 1, 1000)
    page.enter_diff_end_date("Dec", 31, 9999)
    page.click_diff_calculate()

    result = page.get_diff_result()
    assert "calendar days" in result


def test_days_between_year_truncation(driver):
    page = DateCalculatorPage(driver).open()
    page.enter_diff_start_date("Jan", 1, 999999)

    page.click_diff_calculate()
    val = page.get_diff_start_year_value()
    assert val == "9999"


@pytest.mark.parametrize("case", DATA["add_cases"])
def test_add_subtract_date_correct(driver, case):
    page = DateCalculatorPage(driver).open()
    page.enter_add_start_date(*case["start"])
    page.set_add_operation(case["op"])
    page.enter_add_amounts(*case["amounts"])
    page.click_add_calculate()

    result = page.get_add_result()
    assert case["expected"] in result


def test_add_subtract_empty_fields_default_to_zero(driver):
    page = DateCalculatorPage(driver).open()
    page.enter_add_start_date("Jan", 1, 2025)
    page.enter_add_amounts("", "", "", "")
    page.click_add_calculate()

    result = page.get_add_result()
    assert "Jan 1, 2025" in result


def test_add_subtract_invalid_input_letters(driver):
    page = DateCalculatorPage(driver).open()
    page.enter_add_start_date("Jan", 1, 2025)
    page.enter_add_amounts(0, "abc", 0, 0)
    page.click_add_calculate()

    error = page.get_error_message()
    assert error == "Please provide a valid month."


def test_add_subtract_too_long_number(driver):
    page = DateCalculatorPage(driver).open()
    page.enter_add_start_date("Jan", 1, 2025)
    page.enter_add_amounts(0, 9999999999999, 0, 0)
    page.click_add_calculate()

    error = page.get_error_message()
    assert "out of range" in error


def test_form_clear_behavior(driver):
    page = DateCalculatorPage(driver).open()
    page.enter_add_start_date("Jan", 1, 2025)
    page.enter_add_amounts(1, 1, 1, 1)
    page.click_add_calculate()

    result_before = page.get_add_result()
    assert "Feb 9, 2026" in result_before

    page.enter_add_amounts(0, 0, 0, 0)
    page.click_add_calculate()
    assert "Jan 1, 2025" in page.get_add_result()
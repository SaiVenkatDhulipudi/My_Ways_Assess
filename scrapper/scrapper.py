import json
import os

from parsel import Selector
from selenium import webdriver
from utils import FindAllLocations

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
final_result = []

DETAILS_DICT = {"address": "Address: ", "website": "Website: ", "phone": "Phone: "}


def parse_place(selector: Selector):
    def aria_with_label(label):
        """gets aria element as is"""
        return selector.css(f"*[aria-label*='{label}']::attr(aria-label)")

    def aria_no_label(label):
        """gets aria element as text with label stripped off"""
        text = aria_with_label(label).get("")
        return text.split(label, 1)[1].strip()

    try:
        result = {"name": "".join(selector.css("h1 ::text").getall()).strip()}
    except Exception:
        result = {"name": None}
    for key, value in DETAILS_DICT.items():
        try:
            result |= {key: aria_no_label(value)}
        except Exception:
            result |= {key: None}
    return result


def FindLocation(company_name: str):
    url = "https://www.google.com/maps/search/{}".format(company_name)
    urls = FindAllLocations(url)
    if not urls:
        urls = [url]
    for url in urls:
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        browser = webdriver.Chrome()
        browser.get(url)
        page_content = browser.page_source
        browser.close()
        response = Selector(page_content)
        try:
            """
            if the details not found then it throws an Exception
            """
            final_result.append(parse_place(response))
        except Exception:
            pass


if __name__ == "__main__":
    company_name = input("enter company name : ")
    try:
        FindLocation(company_name)
    except Exception:
        pass
    with open(PROJECT_PATH + "/data.json", "w") as file:
        file.write(json.dumps(final_result, indent=4))

import json
import os

from parsel import Selector
from selenium import webdriver
from utils import FindAllLocations

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
final_result = []


def parse_place(selector: Selector):
    def aria_with_label(label):
        """gets aria element as is"""
        return selector.css(f"*[aria-label*='{label}']::attr(aria-label)")

    def aria_no_label(label):
        """gets aria element as text with label stripped off"""
        text = aria_with_label(label).get("")
        return text.split(label, 1)[1].strip()

    result = {
        "name": "".join(selector.css("h1 ::text").getall()).strip(),
        "address": aria_no_label("Address: "),
        "website": aria_no_label("Website: "),
        "phone": aria_no_label("Phone: "),
    }
    return result


def FindLocation(company_name: str, location=None | str):
    urls = ["https://www.google.com/maps/search/{}".format(company_name)]
    if location:
        urls[0] += f"+{location}"
    else:
        urls += FindAllLocations(*urls)
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
    location = input("enter location : ")
    try:
        FindLocation(company_name, location)
    except Exception:
        pass
    with open(PROJECT_PATH + "/data.json", "w") as file:
        file.write(json.dumps(final_result, indent=4))

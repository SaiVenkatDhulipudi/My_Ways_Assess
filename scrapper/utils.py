from parsel import Selector
from selenium import webdriver


def FindAllLocations(url):
    """
    A function to get all the urls associated with the url
    """
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    browser = webdriver.Chrome()
    browser.get(url)
    page_content = browser.page_source
    response = Selector(page_content)
    browser.close()
    results = []
    for el in response.xpath(
        '//div[contains(@aria-label, "Results for")]/div/div[./a]'
    ):
        results.append(el.xpath("./a/@href").extract_first(""))
    return results

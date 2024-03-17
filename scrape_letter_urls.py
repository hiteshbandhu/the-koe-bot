from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import json
import time

options = webdriver.ChromeOptions()
options.headless = True

# instantiate driver
driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()), options=options
)

# load website
url = "https://thedankoe.com/letters/"

# get the entire website content
driver.get(url)


def scroll_till_end():
    while True:
        try:
            load_more_button = driver.find_element(
                By.CLASS_NAME, "elementor-button-link"
            )
            load_more_button.click()
            time.sleep(3.5)
        except:
            break


scroll_till_end()


def get_letters():
    elements = driver.find_elements(By.CLASS_NAME, "elementor-post__title")
    links_arr = []
    i = 1
    for title in elements:
        link = title.find_element(By.TAG_NAME, "a").get_attribute("href")
        heading = title.find_element(By.TAG_NAME, "a").text
        info = {"id": i, "link": link, "heading": heading}
        links_arr.append(info)
        i += 1

    with open("scraped/links.json", "w") as file:
        json_text = json.dumps(links_arr, indent=4)
        file.write(json_text)

    return json_text


get_letters()

driver.quit()

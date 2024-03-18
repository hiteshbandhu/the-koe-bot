from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import json
from tqdm import tqdm
import time

# instantiate options
options = webdriver.ChromeOptions()

# run browser in headless mode
options.headless = True

# instantiate driver
driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()), options=options
)

with open("scraped/links.json", "r") as file:
    letter_links = json.loads(file.read())
    file.close()


letters = []


def get_letter_content_and_append(url, id, heading):
    driver.get(url)
    content_div = driver.find_elements(By.CLASS_NAME, "elementor-widget-container")
    letter_scraped = content_div[14].text

    letter_content = {
        "id": id,
        "heading": heading,
        "content": letter_scraped,
    }

    return letter_content


for link in tqdm(letter_links):
    url = str(link["link"])
    id = link["id"]
    heading = link["heading"]
    letter_content = get_letter_content_and_append(url, id, heading)
    letters.append(letter_content)
    time.sleep(1)


with open("scraped/content.json", "w") as file:
    json_letters = json.dumps(letters, indent=4)
    file.write(json_letters)


driver.quit()

import codecs
import os
import random
import time

import unidecode
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

NAME = "IMPORTER"


def do_import(code):
    chrome_bin = os.getenv('GOOGLE_CHROME_SHIM')

    if chrome_bin:
        opts = Options()
        opts.binary_location = chrome_bin
        driver = webdriver.Chrome(options=opts)
    else:
        driver = webdriver.Chrome(ChromeDriverManager().install())

    wait = WebDriverWait(driver, 10)

    driver.get("https://jackbox.tv/")
    time.sleep(2)

    driver.find_element_by_id("roomcode").send_keys(code)
    driver.find_element_by_id("username").send_keys(NAME)
    wait.until(EC.element_to_be_clickable((By.ID, "button-join")))
    driver.find_element_by_id("button-join").click()

    wait.until(EC.element_to_be_clickable((By.ID, "ugc-new-button")))
    driver.find_element_by_id("ugc-new-button").click()

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".ugc-action-title textarea,  #ugc-title-input")))
    driver.find_element_by_css_selector(".ugc-action-title textarea,  #ugc-title-input").send_keys("Best episode so far")
    driver.find_element_by_css_selector(".ugc-action-title button, #ugc-title-button").click()

    file1 = codecs.open('lines.txt', 'r', encoding="utf-8")
    lines = file1.readlines()
    chosen_files = random.sample(lines, 64)

    for line in chosen_files:
        fixed_line = unidecode.unidecode(line)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".ugc-action-add button, #ugc-add-button")))
        driver.find_element_by_css_selector(".ugc-action-add textarea, #ugc-add-input").send_keys(fixed_line)
        driver.find_element_by_css_selector(".ugc-action-add button, #ugc-add-button").click()

    driver.find_element_by_css_selector(".ugc-action-done button, #ugc-save-button").click()

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".ugc-action-play button, #ugc-play-button")))
    driver.find_element_by_css_selector(".ugc-action-play button, #ugc-play-button").click()

    driver.quit()

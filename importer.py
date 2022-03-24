import codecs
import os
import random
import time

import unidecode
from flask_socketio import emit
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class Importer:
    EPISODE = "Best episode so far"
    NAME = "IMPORTER"
    step = 0
    
    def __init__(self, logger):
        self.logger = logger

    def do_import(self, code):

        bundled = os.getenv("BUNDLED")
        self.logger.info(bundled)

        if bundled is not None:
            opts = webdriver.ChromeOptions()
            opts.add_argument('--no-sandbox')
            opts.add_argument('--headless')
            opts.add_argument('--disable-gpu')
            opts.add_argument('--disable-dev-shm-usage')
            opts.add_argument("--window-size=1920,1080")
            driver = webdriver.Chrome(options=opts)
        else:
            driver = webdriver.Chrome(ChromeDriverManager().install())
        self.update_progress()

        try:
            wait = WebDriverWait(driver, 10)

            driver.get("https://jackbox.tv/")
            time.sleep(2)
            self.update_progress()

            driver.find_element_by_id("roomcode").send_keys(code)
            driver.find_element_by_id("username").send_keys(self.NAME)
            wait.until(EC.element_to_be_clickable((By.ID, "button-join")))
            driver.find_element_by_id("button-join").click()
            self.update_progress()

            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".ugc-action-new button, #ugc-new-button")))
            driver.find_element_by_css_selector(".ugc-action-new button, #ugc-new-button").click()
            self.update_progress()

            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".ugc-action-title textarea,  #ugc-title-input")))
            driver.find_element_by_css_selector(".ugc-action-title textarea,  #ugc-title-input").send_keys(self.EPISODE)
            driver.find_element_by_css_selector(".ugc-action-title button, #ugc-title-button").click()
            self.update_progress()

            file1 = codecs.open("lines.txt", "r", encoding="utf-8")
            lines = file1.readlines()
            chosen_files = random.sample(lines, 64)

            for line in chosen_files:
                fixed_line = unidecode.unidecode(line)
                wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".ugc-action-add button, #ugc-add-button")))
                driver.find_element_by_css_selector(".ugc-action-add textarea, #ugc-add-input").send_keys(fixed_line)
                driver.find_element_by_css_selector(".ugc-action-add button, #ugc-add-button").click()
                self.update_progress()

            driver.find_element_by_css_selector(".ugc-action-done button, #ugc-save-button").click()
            self.update_progress()

            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".ugc-action-play button, #ugc-play-button")))
            driver.find_element_by_css_selector(".ugc-action-play button, #ugc-play-button").click()
            self.update_progress()
        except TimeoutException:
            emit("error", "Room with password {} not found".format(code))
        except Exception as e:
            print(e)
            emit("error", "Unknown error occurred")

        driver.quit()

    def update_progress(self):
        self.step += 1
        emit("progress", {"step": self.step})

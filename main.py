import os
import time
import urllib.request

from dotenv import load_dotenv
from pushbullet import Pushbullet
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from config import IDS, JOB_TYPE,show_notification
from scheduler import WAIT_TIME_BEFORE_SCRAPPING,WAIT_TIME_AFTER_SCRAPING

load_dotenv(".env")

PB_KEY = os.getenv('PB_KEY')
pb = Pushbullet(PB_KEY)


def is_connected():
    try:
        urllib.request.urlopen("http://www.google.com", timeout=1)
        return True
    except urllib.error.URLError:
        pass
    return False


service = Service("./chromedriver-win64/chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service=service)


def getPythonjobs():
    while True:
        if is_connected():
            for index, id in enumerate(IDS):
                driver.get(f"https://www.upwork.com/nx/jobs/search/?ontology_skill_uid={id}&sort=recency")
                time.sleep(WAIT_TIME_BEFORE_SCRAPPING)
                element = driver.find_element(By.CSS_SELECTOR, '[data-test="job-tile-list"]')
                span_ele = element.find_element(By.TAG_NAME, 'small')
                print(span_ele.text)
                i = span_ele.text.find("Posted")
                posted = span_ele.text[i:].split()
                posted_time = posted[1] + posted[2]
                if "minute" in posted_time or "second" in posted_time:
                    show_notification(title=f"New {JOB_TYPE[index]} Project",
                                      message="New project Posted about " + posted_time,
                                      duration=10)
                    pb.push_note(f"New {JOB_TYPE[index]} Project", "New project Posted about " + posted_time)
                time.sleep(WAIT_TIME_AFTER_SCRAPING)

        else:
            print("Wifi Not Connected")


getPythonjobs()
driver.quit()

import os
import time
import urllib.request
from pushbullet import Pushbullet
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from win10toast import ToastNotifier
from dotenv import load_dotenv

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


def show_notification(title, message, duration):
    toaster = ToastNotifier()
    start_time = time.time()

    while time.time() - start_time < duration:
        toaster.show_toast(title, message, duration=5)
        time.sleep(5)


service = Service("./chromedriver-win64/chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service=service)

ids=['996364628025274386','1031626732309299200']
job_type = ["Python", "Django"]


def getPythonjobs():
    while True:
        if is_connected():
            for index, id in enumerate(ids):
                driver.get(f"https://www.upwork.com/nx/jobs/search/?ontology_skill_uid={id}&sort=recency")
                time.sleep(90)
                element = driver.find_element(By.CSS_SELECTOR, '[data-test="job-tile-list"]')
                span_ele = element.find_element(By.TAG_NAME, 'small')
                print(span_ele.text)
                i = span_ele.text.find("Posted")
                posted = span_ele.text[i:].split()
                posted_time = posted[1] + posted[2]
                if "minute" in posted_time or "second" in posted_time:
                    show_notification(title=f"New {job_type[index]} Project",
                                      message="New project Posted about " + posted_time,
                                      duration=20)

                pb.push_note(f"New {job_type[index]} Project", "New project Posted about " + posted_time)
                time.sleep(200)

        else:
            print("Wifi Not Connected")


getPythonjobs()
driver.quit()

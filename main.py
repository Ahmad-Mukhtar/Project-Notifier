import os
import time
import urllib.request
import cloudscraper
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from pushbullet import Pushbullet
from config import JOB_TYPE_TO_CONSIDER, IDS_TO_CONSIDER

load_dotenv(".env")
PB_KEY = os.getenv('PB_KEY')
WAIT_TIME_AFTER_SCRAPING = float(os.getenv("WAIT_TIME_AFTER_SCRAPING"))

pb = Pushbullet(PB_KEY)


def is_connected():
    try:
        urllib.request.urlopen("http://www.google.com", timeout=1)
        return True
    except urllib.error.URLError:
        pass
    return False


def getJobs():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(HTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    }
    scraper = cloudscraper.create_scraper()
    while True:
        if is_connected():
            for index, project_id in enumerate(IDS_TO_CONSIDER):
                response = scraper.get(
                    f"https://www.upwork.com/nx/jobs/search/?ontology_skill_uid={project_id}&sort=recency",
                    headers=headers)
                soup = BeautifulSoup(response.content, "html.parser")
                try:
                    print(f"Soup is {soup.text}")
                    jobs_section = soup.find("section")
                    print(f"Jobs_section {jobs_section}")
                    jobs_headers = jobs_section.findAll("div", {"class": "job-tile-header"})
                    latest_posted_job = None
                    for job in jobs_headers:
                        posted_time = job.text.split()
                        posted_time = posted_time[1] + " " + posted_time[2] + " " + posted_time[3]
                        if "day" in posted_time:
                            print(f"Premium job{job.text} ")
                        else:
                            latest_posted_job = job
                            break
                    posted_job_list = latest_posted_job.text.split()
                    print(f"New {JOB_TYPE_TO_CONSIDER[index]} Project")
                    print(str(posted_job_list))
                    posted_time = posted_job_list[1] + " " + posted_job_list[2] + " " + posted_job_list[3]
                    print(f"Posted Time is : {posted_time}")
                    if "minute" in posted_time or "second" in posted_time:
                        pb.push_note(f"New {JOB_TYPE_TO_CONSIDER[index]} Project", latest_posted_job.text)
                        print("Notification Sent")
                except Exception as e:
                    print(f"Some Exception Occurred  {e}")
                finally:
                    print("WAIT_TIME_AFTER_SCRAPING")
                    time.sleep(WAIT_TIME_AFTER_SCRAPING)
            print("Sleeping for 5 minutes")
            time.sleep(300)
        else:
            print("Wifi Not Connected")


if __name__ == '__main__':
    getJobs()

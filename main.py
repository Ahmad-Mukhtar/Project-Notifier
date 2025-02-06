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
WAIT_TIME_AFTER_SCRAPING_ALL = float(os.getenv("WAIT_TIME_AFTER_SCRAPING_ALL"))
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
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en",
        "Connection": "keep-alive",
        "cache-control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "no-cache, must-revalidate",
        "Cookie": "visitor_id=124.29.253.188.1738837186273000; "
                  "UniversalSearchNuxt_vt=oauth2v2_7730e08c20cc7c795e5c713b05a451eb; country_code=PK; cookie_prefix=; "
                  "cookie_domain=.upwork.com; __cf_bm=gsJP_o5hzaSwsrZaS4CR3L2ocTvz8487cVZ6X.s0Qsg-1738837187-1.0.1.1"
                  "-YWnuKJ03TNaqxcipN9qsLPTFhGg7v1eM2iMGEFSwVW_PFX8qM4JLna0dcQukHOm3HzFat5mRg.RyqY2EAbZHBA; "
                  "__cflb=02DiuEXPXZVk436fJfSVuuwDqLqkhavJbLmKcUahjLpvo; "
                  "_cfuvid=3iKUUErkTXClvAwQ1rQk4ITGX6ZjIyNQlleFQgiS5F0-1738837187020-0.0.1.1-604800000; umq=1536; "
                  "cf_clearance=mkOmWwytpOBGYIm41sgP6dC7aQk86K60UAZ03N3sdU4-1738837191-1.2.1.1"
                  "-cO8wSpfdmS4t4mS34os5SGVjM6Bi22Eujrzj.vm.uXdM1JpagNjPbHm"
                  ".n8j91bJcQYNiZoEXFdBqAQjZojqIe_zr1f8iQiTmR2NorV_"
                  ".OipsIiT4RTGmyKSbxUkpRrg7wdoa5pIrknazysXyR91kUj7Ih0u2U1dcAicc9j_XPFJccW5J"
                  "..VQPc460kAeBiwCswhPxiFQ_2Ca0hI0e0MWvw48rxs4qDYJkeFzU0QfqaWgrvjmY_Y"
                  ".IvgRxa6SKXIcvUd6fxUpjY2Wk6FhnWRAcStEPiyeXHVXOqauksouzQc; _upw_ses.5831=*; "
                  "_cq_duid=1.1738837189.8ewSmo4uwHNdut7W; _cq_suid=1.1738837189.8XU13qXGCfgFSgWH; "
                  "spt=84f63550-f7c6-40ac-b8c1-dc537fb2c801; "
                  "forterToken=d740de34c1844d1dac16516328cfadd8_1738837189367__UDF43-m4_23ck_4cpBkGZFakw%3D-1262-v2; "
                  "forterToken=d740de34c1844d1dac16516328cfadd8_1738837189367__UDF43-m4_23ck_4cpBkGZFakw%3D-1262-v2; "
                  "_gcl_au=1.1.1193907192.1738837192; __pdst=0940e5970b754b4398516e8018c88a93; "
                  "_fbp=fb.1.1738837192938.424357279871502829; _ga_KSM221PNDX=GS1.1.1738837193.1.0.1738837193.0.0.0; "
                  "_ga=GA1.1.1683867288.1738837193; _rdt_uuid=1738837193119.9c97d9a9-d9b5-4df6-8021-da45857d8d8f; "
                  "IR_gbd=upwork.com; IR_13634=1738837192712%7C4746153%7C1738837192712%7C%7C; "
                  "_uetsid=e7fbde80e47311ef9fbd75c88890fdef; _uetvid=e7fc0ad0e47311efb556bb84ccbaedd3; "
                  "AWSALBTG=J0OPLN2KHZhKKgYg1DJkR1ElLFOBOzzHfxfrG687WQbUpQZtv4KuAajNLzU8Bi1XGfT9XjaLtIQwe+aiFUK"
                  "/8zszGK3AZ2zURRjp68MzDjZ01NdY6WwK3/ttM0Ig3QxYPHJSTcJAd1ICW46L7UX0iHdZro1+BQmBVbXkl2yxHZOk; "
                  "AWSALBTGCORS=J0OPLN2KHZhKKgYg1DJkR1ElLFOBOzzHfxfrG687WQbUpQZtv4KuAajNLzU8Bi1XGfT9XjaLtIQwe+aiFUK"
                  "/8zszGK3AZ2zURRjp68MzDjZ01NdY6WwK3/ttM0Ig3QxYPHJSTcJAd1ICW46L7UX0iHdZro1+BQmBVbXkl2yxHZOk; "
                  "IR_PI=e975adde-e473-11ef-a48b-67ace7810d36%7C1738837192712; _tt_enable_cookie=1; "
                  "_ttp=DF6raRWEZyXnB0c0b_jvRGGMa-0.tt.1; enabled_ff=i18nOn,!RMTAir3Talent,!RMTAir3Offers,"
                  "!RMTAir3Hired,!RMTAir3Offer,!i18nGA,!CI10857Air3Dot0,!air2Dot76Qt,air2Dot76,"
                  "!CI12577UniversalSearch,!RMTAir3Home,OTBnrOn,!CI10270Air2Dot5QTAllocations,TONB2256Air3Migration,"
                  "!MP16400Air3Migration,CI11132Air2Dot75,CI17409DarkModeUI,JPAir3,SSINavUserBpa,!SSINavUser,"
                  "CI9570Air2Dot5; OptanonAlertBoxClosed=2025-02-06T10:20:56.525Z; "
                  "OptanonConsent=isGpcEnabled=0&datestamp=Thu+Feb+06+2025+15%3A20%3A56+GMT%2B0500+("
                  "Pakistan+Standard+Time)&version=202305.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId"
                  "=529d481f-2794-4796-a8ed-c87f58a5b388&interactionCount=1&landingPath=NotLandingPage&groups=C0001"
                  "%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1; "
                  "_upw_id.5831=27d69ec1-1178-4315-a437-6959a37d9c8e.1738837190.1.1738837257..2c3c5c3a-edf5-42e2-a9f2"
                  "-24131368b4bf..82c2a41c-80df-4489-90e0-53a44d2b0e81.1738837189534.10; "
                  "AWSALB=7CdHrJSpJeEAmzmOhcFo0QOsp9nNfutKzIc1DvICoJFQq4xuWdnC60cHKDaTTYSb/8Wiuw1LzDIxbIIbg"
                  "/2R2wL9UHpF0bT5EO4Ilq0EidNdm+bG1k69D5CKIEP4; "
                  "AWSALBCORS=7CdHrJSpJeEAmzmOhcFo0QOsp9nNfutKzIc1DvICoJFQq4xuWdnC60cHKDaTTYSb/8Wiuw1LzDIxbIIbg"
                  "/2R2wL9UHpF0bT5EO4Ilq0EidNdm+bG1k69D5CKIEP4"
    }
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'firefox',
            'platform': 'windows',
            'mobile': False
        }
    )
    # Set your desired time
    # Convert the UTC time to your desired time zone
    while True:
        if is_connected():
            for index, project_id in enumerate(IDS_TO_CONSIDER):
                job_url = f"https://www.upwork.com/nx/jobs/search/?ontology_skill_uid={project_id}&sort=recency"
                response = scraper.get(job_url, headers=headers)
                soup = BeautifulSoup(response.content, "html.parser")
                try:
                    jobs_section = soup.find("section")
                    jobs_headers = jobs_section.findAll("div", {"class": "job-tile-header"})
                    latest_posted_job = None
                    for job in jobs_headers:
                        posted_time = job.text.split()
                        posted_time = posted_time[1] + " " + posted_time[2] + " " + posted_time[3]
                        if "day" in posted_time:
                            print(f"Premium job {job.text} ")
                        else:
                            latest_posted_job = job
                            break
                    posted_job_list = latest_posted_job.text.split()
                    print(f"New {JOB_TYPE_TO_CONSIDER[index]} Project")
                    print(str(posted_job_list))
                    posted_time = posted_job_list[1] + " " + posted_job_list[2] + " " + posted_job_list[3]
                    print(f"Posted Time is : {posted_time}")
                    if "minute" in posted_time or "second" in posted_time:
                        pb.push_note(f"New {JOB_TYPE_TO_CONSIDER[index]} Project",
                                     latest_posted_job.text + " job Link:  " + job_url)
                        print("Notification Sent")
                except Exception as e:
                    print(f"Some Exception Occurred  {e}")
                finally:
                    print("WAIT_TIME_AFTER_SCRAPING")
                    time.sleep(WAIT_TIME_AFTER_SCRAPING)
            print("Sleeping for 5 minutes")
            time.sleep(WAIT_TIME_AFTER_SCRAPING_ALL)
        else:
            print("Wifi Not Connected")


if __name__ == '__main__':
    getJobs()

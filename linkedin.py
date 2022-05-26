from selenium import webdriver
import time
import csv
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.options import Options as CO
from selenium.webdriver.firefox.options import Options as FO

file = open('results_linkedin.csv', 'w', encoding='utf-8')
writer = csv.writer(file)
writer.writerow(['Job_url', 'Job_title', 'Company_logo', 'Company_name', 'Posted_time', 'Participant_num', 'Description', 'Seniority_level', 'Employment_type', 'Job_function', 'Industries', 'Find_a_referral', 'Recruiter_info', 'Apply_on_company_website'])

options_firefox = FO()
options_chrome = CO()
options_chrome.headless = True
options_firefox.headless = True
chrome_driver = webdriver.Chrome(ChromeDriverManager().install(), options=options_chrome)
firefox_driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options_firefox)
firefox_wait = WebDriverWait(firefox_driver, 10)
chrome_driver.get("https://www.linkedin.com/jobs/search?keywords=&location=Australia&geoId=101452733&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0")
for link in [x.get_attribute("href") for x in chrome_driver.find_elements_by_css_selector(".base-card__full-link")]:
    pass

SCROLL_PAUSE_TIME = 3

# Get scroll height
last_height = chrome_driver.execute_script("return document.body.scrollHeight")
used_links = []
while True:
    for link in [x.get_attribute("href") for x in chrome_driver.find_elements_by_css_selector(".base-card__full-link")]:
        if link not in used_links:
            used_links.append(link)
            firefox_driver.get(link)
            item = {
            "job_url": link,
            'job_title': '',
            'company_logo': '',
            'company_name': '',
            'posted_time': '',
            'participant_num': '',
            'description': '',
            'seniority_level': '',
            'employment_type': '',
            'job_function': '',
            'industries': '',
            'find_a_referral': '',
            'recruiter_info': '',
            'apply_on_company_website': ''
            }
            try:
                item["job_title"] = firefox_wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".top-card-layout__title.topcard__title"))).text
            except TimeoutException:
                pass
            try:
                item["company_logo"] = firefox_wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".artdeco-entity-image.artdeco-entity-image--square-5"))).get_attribute("src")
            except TimeoutException:
                pass
            try:
                item["company_name"] = firefox_wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".topcard__org-name-link"))).text + " - " + firefox_wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".topcard__flavor.topcard__flavor--bullet"))).text
            except TimeoutException:
                pass
            try:
                item["posted_time"] = firefox_wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".posted-time-ago__text"))).text
            except TimeoutException:
                pass
            try:
                item["participant_num"] = firefox_wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".num-applicants__caption"))).text
            except TimeoutException:
                pass
            try:
                item["description"] = firefox_wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".show-more-less-html__markup"))).text
            except TimeoutException:
                pass
            for i in range(1, 5):
                try:
                    if "Seniority level" in firefox_wait.until(EC.element_to_be_clickable(
                            (By.CSS_SELECTOR, f".description__job-criteria-list li:nth-child({i})  h3"))).text:
                        item["seniority_level"] = firefox_wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f".description__job-criteria-list li:nth-child({i})  .description__job-criteria-text.description__job-criteria-text--criteria"))).text
                except TimeoutException:
                    pass
                try:
                    if "Employment type" in firefox_wait.until(EC.element_to_be_clickable(
                            (By.CSS_SELECTOR, f".description__job-criteria-list li:nth-child({i})  h3"))).text:
                        item["employment_type"] = firefox_wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f".description__job-criteria-list li:nth-child({i})  .description__job-criteria-text.description__job-criteria-text--criteria"))).text
                except TimeoutException:
                    pass
                try:
                    if "Job function" in firefox_wait.until(EC.element_to_be_clickable(
                            (By.CSS_SELECTOR, f".description__job-criteria-list li:nth-child({i})  h3"))).text:
                        item["job_function"] = firefox_wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f".description__job-criteria-list li:nth-child({i})  .description__job-criteria-text.description__job-criteria-text--criteria"))).text
                except TimeoutException:
                    pass
                try:
                    if "Industries" in firefox_wait.until(EC.element_to_be_clickable(
                            (By.CSS_SELECTOR, f".description__job-criteria-list li:nth-child({i})  h3"))).text:
                        item["industries"] = firefox_wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f".description__job-criteria-list li:nth-child({i})  .description__job-criteria-text.description__job-criteria-text--criteria"))).text
                except TimeoutException:
                    pass
            try:
                item["find_a_referral"] = firefox_wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".find-a-referral__cta-container p"))).text
            except TimeoutException:
                pass
            try:
                item["recruiter_info"] = "Name: " + firefox_wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".message-the-recruiter .base-main-card__title"))).text + "\nTitle: " + firefox_wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".message-the-recruiter .base-main-card__subtitle"))).text
            except TimeoutException:
                pass
            try:
                item["apply_on_company_website"] = firefox_wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".top-card-layout__cta-container .apply-button"))).get_attribute("href")
            except TimeoutException:
                pass
            print(item)
            writer.writerow([item['job_url'], item['job_title'], item['company_logo'], item['company_name'], item['posted_time'], item['participant_num'], item['description'], item['seniority_level'], item['employment_type'], item['job_function'], item['industries'], item['find_a_referral'], item['recruiter_info'], item['apply_on_company_website']])


    # Scroll down to bottom
    chrome_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = chrome_driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height


import requests
from bs4 import BeautifulSoup
import csv

results = []
file = open('results_seek.csv', 'w', encoding='utf-8')
writer = csv.writer(file)
writer.writerou" + job_link.attrs['href'],
            'job-title': '',
            'company-name': '',
            'company-link': '',
            'job-location': '',
            'job-fields': '',
            'job-hours': '',
            'job-rating': '',
            'no-of-reviews': '',
            'job-description': ''
        }
        try:
            item["job-title"] = job_response.select_one('h1[data-automation="job-detail-title"]').text
        except AttributeError:
            pass
        try:
            item["company-name"] = job_response.select_one('[data-automation="advertiser-name"] a').text
        except AttributeError:
            pass
        try:
            item["company-link"] = "https://www.seek.com.au" + job_response.select_one('[data-automation="advertiser-name"] a').attrs["href"]
        except AttributeError:
            pass
        try:
            item["job-location"] = " - ".join([x.text for x in job_response.select(".yvsb870 ._14uh99496:nth-child(1) > span > div > div")])
        except AttributeError:
            pass
        try:
            item["job-fields"] = " - ".join([x.text for x in job_response.select(".yvsb870 ._14uh99496:nth-child(2) > span > div > div")])
        except AttributeError:
            pass
        try:
            item["job-hours"] = " - ".join([x.text for x in job_response.select('[data-automation="job-detail-work-type"] div')])
        except AttributeError:
            pass
        try:
            item["job-rating"] = job_response.select_one("._14uh99486._14uh9942q._14uh994ce:nth-child(2) span").text + "/5"
        except AttributeError:
            pass
        try:
            item["no-of-reviews"] = job_response.select_one("._14uh99486._14uh9942q._14uh994ce:nth-child(4) span").text
        except AttributeError:
            pass
        try:
            item["job-description"] = job_response.select_one('[data-automation="jobAdDetails"]').text
        except AttributeError:
            pass
        next_page = page.select_one('[data-automation="page-next"]')

        writer.writerow([item['job-url'], item['job-title'], item['company-name'], item['company-link'], item['job-location'], item['job-fields'], item['job-hours'], item['job-rating'], item['no-of-reviews'], item['job-description']])

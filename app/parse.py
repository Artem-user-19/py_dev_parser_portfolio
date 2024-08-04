import re

import pandas as pd
import requests
from bs4 import BeautifulSoup

from parse_link import main_url


def parse_work_ua(base_url):
    jobs = []

    page_number = 1

    while True:
        url = f"{base_url}?page={page_number}"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')

        work_tags = soup.find_all("div", class_="card-hover")

        if not work_tags:
            break

        for work_tag in work_tags:
            title_tag = work_tag.find("h2")
            title = title_tag.get_text(strip=True) if title_tag else "N/A"

            company_tag = work_tag.find("span", class_="mr-xs")
            company = company_tag.get_text(strip=True)\
                if company_tag else "N/A"

            salary_tag = work_tag.find("span", class_="strong-600")
            salary = salary_tag.get_text(strip=True) if salary_tag else "N/A"

            if re.search(r'\d', salary):
                cleaned_salary = re.sub(
                    r'[\u202f\u2009\xa0]', ' ', salary
                ).strip()
            else:
                cleaned_salary = "N/A"

            link_tag = work_tag.find("a", href=True)
            link = f"https://www.work.ua{link_tag['href']}"\
                if link_tag else "N/A"

            jobs.append({
                'title': title,
                'company': company,
                'salary': cleaned_salary,
                'link': link
            })

        pagination = soup.find("ul", class_="pagination hidden-xs")
        if pagination:
            page_links = pagination.find_all("a", href=True)
            page_numbers = [int(a.get_text(strip=True))
                            for a in page_links
                            if a.get_text(strip=True).isdigit()]

            if page_numbers and page_number >= max(page_numbers):
                break

            page_number += 1
        else:
            break

    return jobs


if __name__ == '__main__':
    base_url = main_url
    job_data = parse_work_ua(base_url)

    df = pd.DataFrame(job_data)

    df.to_csv('job_data.csv', index=False, encoding='utf-8')

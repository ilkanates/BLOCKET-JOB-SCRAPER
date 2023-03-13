# selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

# other lib
import time
import os

# bs
from bs4 import BeautifulSoup as bs
import requests

# data
import pandas as pd
import re

# make clickable
from IPython.display import display, HTML

# translator
import uuid, json


def translate_text(text_to_translate):
    key = "a9250938ec9c46a392d89a01e99b78c8"
    endpoint = "https://api.cognitive.microsofttranslator.com"
    location = "eastus"
    path = '/translate'
    constructed_url = endpoint + path
    params = {
        'api-version': '3.0',
        'from': ['sv'],
        'to': ['en']
    }
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }
    body = [{
        'text': text_to_translate
    }]
    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()

    return response[0]['translations'][0]['text']


def job_search():
    url = "https://jobb.blocket.se/"
    while True:
        title = input("Enter job title: ")
        if title == '':
            print("Job title cannot be empty.")
        else:
            job_search = ""
            job_title_lst = title.split()
            job_search = [(job_search + i + "+")[:-1] for i in job_title_lst]
            break

    while True:
        address = input("Enter address: ")
        if address == '':
            print("Address cannot be empty.")
        else:
            break

    while True:
        search_range = input("How many pages do you want to search? (default is 10): ")
        if search_range == '':
            search_range = 10
            break
        try:
            search_range = int(search_range)
            if search_range > 0:
                break
            else:
                print("Search range must be a positive integer.")
        except ValueError:
            print("Invalid input. Please enter a positive integer.")

    skill_set_string = input("Enter your skills. Use comma to seperate it: ")
    skill_set = skill_set_string.lower().split(",")

    title_key = "a.header"
    corp_key = "a.corp.bold"
    date_key = "div.extra>span"
    link_key = "a.header"
    time_left_key = "table.ui.job-info.very.compact.borderless.fixed.table > tbody > tr> td:nth-child(2)"
    location_role_key = "div.column.no-padding>span>a"
    job_des_key = "body > div#page-flex-wrapper:nth-child(2) > div#body_content.white-bg:nth-child(4) > div.view:nth-child(4) > div.ui.container:nth-child(3) > div.ui.two.column.stackable.padded.grid > div.seven.wide.column.no-padding-mobile:nth-child(1) > div.ui.container.no-margin-mobile:nth-child(2) > div.ui.padded.grid > div#ad_text_column.ui.column.no-padding > div#job-description:nth-child(1)"
    agree_key = "button.InfoPage__SchibstedButton-sc-3ewdh5-13.InfoPage__AcceptButton-sc-3ewdh5-15.gCzPOF"
    title_search_key = "div.ui.left.icon.fluid.large.input.search.category > input.prompt"
    location_search_key = "div>input.search"
    search_button_key = "div>a.ui.primary.button.fluid"

    driver = webdriver.Chrome("C:\Program Files (x86)\chromedriver.exe")  # create a driver
    driver.get(url)  # bring us to the webpage
    time.sleep(2.5)  # wait a bit

    # click I agree

    agree = driver.find_element(By.CSS_SELECTOR, agree_key)
    agree.click()

    # find the search bar and enter keywords
    title_search = driver.find_element(By.CSS_SELECTOR, title_search_key)
    title_search.send_keys(title)

    # find the search bar and enter keywords

    location_search = driver.find_element(By.CSS_SELECTOR, location_search_key)
    location_search.send_keys(address)

    # click the search button
    search_button = driver.find_element(By.CSS_SELECTOR, search_button_key)
    search_button.click()

    title_lst = []
    corp_lst = []
    date_lst = []
    link_lst = []
    id_lst = []
    time_left_lst = []
    location_lst = []
    role_lst = []
    job_des_lst = []
    match_lst = []

    # Get the page source and create a soup
    soup = bs(driver.page_source, "lxml")
    containers = soup.select("div.ui.divided.items.unstackable.jobitems > div.item.job-item")

    for x in range(0, search_range):
        url = f"https://jobb.blocket.se/lediga-jobb-i-{address}/sida{x}/?ks=freetext.{job_search}"
        html = requests.get(url).content
        soup = bs(html, "lxml")
        containers = soup.select("div.ui.divided.items.unstackable.jobitems>div.item.job-item")

        for i in containers:
            # get title
            title = [j.text.strip() for j in i.select(title_key)]
            corp = [j.text.strip() for j in i.select(corp_key)]
            date = [j.text.strip() for j in i.select(date_key)]
            link = [i['href'] for i in soup.select(link_key)]

            if title:
                # title = translate_text(title)
                title_lst.append(title)
            else:
                title_lst.append(np.nan)

            if corp:
                corp_lst.append(corp)
            else:
                corp_lst.append(np.nan)

            if date:
                date_lst.append(date[0])
            else:
                date_lst.append(np.nan)

        if link:
            for i in link:
                link_lst.append(i)
        else:
            link_lst.append(np.nan)

        if link:
            for i in link:
                id = re.search(r'(\d+#\d+)', i)
                i = id.group(1)
                id_lst.append(i)
        else:
            id_lst.append(np.nan)

        for i in link:
            url = i
            html = requests.get(url).content
            soup = bs(html)
            time_left = [i.text for i in soup.select(time_left_key)][-1]
            location = [i.text for i in soup.select(location_role_key)[1]]
            role = [i.text for i in soup.select(location_role_key)[2]]
            job_des = [i.text.lower() for i in soup.select(job_des_key)]
            # job_des   = translate_text(job_des[0]).lower()

            if time_left:
                time_left_lst.append(time_left)
            else:
                time_left_lst.append(np.nan)

            if location:
                location_lst.append(location)
            else:
                location_lst.append(np.nan)

            if role:
                role_lst.append(role)
            else:
                role_lst.append(np.nan)

            if job_des:
                match = 0
                for skill in skill_set:
                    if job_des[0].split().count(skill):
                        match += 1
                match_lst.append(round(match / len(skill_set) * 100))
            else:
                job_des_lst.append(np.nan)

    new_job_lst = job_des[0].split()

    # df
    df = pd.DataFrame({
        "Id": id_lst,
        "Title": title_lst,
        "Corperation": corp_lst,
        "Created Date": date_lst,
        "Last Apply Date": time_left_lst,
        "Location": location_lst,
        "Role Area": role_lst,
        "Link": link_lst,
        "Match": match_lst
    })
    df = df.sort_values("Match", ascending=False)

    df = df.drop_duplicates(subset='Id', keep='first')
    df['Link'] = '<a href="' + df['Link'].astype(str) + '">Link</a>'
    df = df.reset_index(drop=True)
    df = display(HTML(df.to_html(escape=False)))

    return df
    print("Done!!!")
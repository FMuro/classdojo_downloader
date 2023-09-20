#!/usr/bin/env python3

import requests
import json
import os
import tempfile
from selenium import webdriver
import datetime
import exiftool

FEED_URL = 'https://home.classdojo.com/api/storyFeed?includePrivate=true'
LOGIN_URL = 'https://home.classdojo.com'
# make sure this directory exists in the same place as this script.
DESTINATION = tempfile.mkdtemp(dir='.') # a temporary directory will be created in the same directory as this script.


def from_date():
    print('\nPlease, enter the date from which you want to download the data or Enter to download everything.\n')

    while True:
        not_before = input('Date (YYYY-MM-DD) or Enter: ')
        date_format = '%Y-%m-%d'

        if not_before == '':
            not_before = datetime.datetime(1,1,1,0,0,0,0)
            break
        else: 
            try:
                # formatting the date using strptime() function
                dateObject = datetime.datetime.strptime(not_before, date_format)

            # If the date validation goes wrong
            except ValueError:
                # printing the appropriate text if ValueError occurs
                print("Incorrect data format, should be YYYY-MM-DD.")

            else:
                not_before = datetime.datetime.strptime(not_before, date_format)
                break

    return not_before


def get_cookies(login_url):
    print('Which of these browsers do you want to use?\n')
    print('\t1. Chrome')
    print('\t2. Firefox\n')

    while True:
        browser_choice = input('Please, enter 1 or 2: ')
        if browser_choice == '1':
            driver = webdriver.Chrome()
            break
        elif browser_choice == '2':
            driver = webdriver.Firefox()
            break

    driver.get(login_url)

    input('\nPlease, login to your account and then press Enter here.')

    cd_cookies = driver.get_cookies()

    for cookie in cd_cookies:
        if cookie['name'] == 'dojo_log_session_id':
            dojo_log_session_id = cookie['value']
        elif cookie['name'] == 'dojo_login.sid':
            dojo_login_sid = cookie['value']
        elif cookie['name'] == 'dojo_home_login.sid':
            dojo_home_login_sid = cookie['value']

    session_cookies = {
        'dojo_log_session_id': dojo_log_session_id,
        'dojo_login.sid': dojo_login_sid,
        'dojo_home_login.sid': dojo_home_login_sid
    }

    return session_cookies


def get_items(feed_url, session_cookies):
    print('Fetching items: %s ...' % feed_url)
    resp = requests.get(feed_url, cookies=session_cookies)
    data = resp.json()
    prev = data.get('_links', {}).get('prev', {}).get('href')

    return data['_items'], prev


def get_contents(feed_url, session_cookies, not_before):
    items, prev = get_items(feed_url, session_cookies)

    while prev and feed_url != prev:
        prev_urls, prev = get_items(prev, session_cookies)
        items.extend(prev_urls)

    # Save the JSON data for later/inspection.
    data_json = os.path.join(DESTINATION, 'text_files', 'data.json')
    os.makedirs(os.path.dirname(data_json), exist_ok=True)
    with open(data_json, 'w+') as fd:
        fd.write(json.dumps(items, indent=4))

    contents = []
    total = 0
    for item in items:
        data = item['contents']
        time = item['time']
        python_time = datetime.datetime.strptime(time,'%Y-%m-%dT%H:%M:%S.%fZ')
        entry = {
            'description': data.get('body'),
            'base_name': None,
            'time': None,
            'attachments': [],
        }
        attachments = data.get('attachments', {})
        if not attachments:
            continue

        for attachment in attachments:
            parts = attachment['path'].split('/')
            if parts[3] == 'api' or python_time < not_before:
                continue
            total += 1
            if not entry['base_name']:
                entry['base_name'] = parts[-4]
                entry['time'] = time
            entry['attachments'].append({'name': '_'.join(parts[-2:]),
                                         'url': attachment['path']})

        if entry['base_name']:
            contents.append(entry)

    return contents, total


def download_contents(contents, total, session_cookies):
    if contents == []:
        print('\nNo new data to download.')
    else:
        index = 0
        python_highest_time = datetime.datetime.strptime(contents[0]['time'],'%Y-%m-%dT%H:%M:%S.%fZ')
        highest_time = python_highest_time.strftime('%Y-%m-%d %H:%M:%S')
        for entry in contents:
            description_name = '{}_description.txt'.format(entry['base_name'])
            description_full_path = os.path.join(DESTINATION, 'text_files', description_name)
            os.makedirs(os.path.dirname(description_full_path), exist_ok=True)
            with open(description_full_path, 'w+t') as fd:
                fd.write(entry['description'])
            for item in entry['attachments']:
                index += 1
                python_time = datetime.datetime.strptime(entry['time'],'%Y-%m-%dT%H:%M:%S.%fZ')
                time = python_time.strftime('%Y-%m-%d %H:%M:%S')
                if python_time > python_highest_time:
                    highest_time = time
                url = item['url']
                filename = os.path.join(DESTINATION, 'images',
                                        '{}_{}'.format(entry['base_name'],
                                                       item['name']))
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                if os.path.exists(filename):
                    continue
                print('Downloading {}/{} on {}: {}'
                    .format(index, total, time, item['name']))
                with open(filename, 'w+b') as fd:
                    resp = requests.get(url, cookies=session_cookies)
                    fd.write(resp.content)
                with exiftool.ExifTool() as et:
                    print(format(time))
                    et.execute(
                        '-AllDates={}'.format(time),
                        '-overwrite_original',
                        filename,
                    )
        print('Last time of data download: {}'.format(highest_time))
        print('Done!')


if __name__ == '__main__':
    print('\nThis script will help you to download your pictures from ClassDojo.')
    print('You need to login to your account and then press Enter here.\n')
    session_cookies = get_cookies(LOGIN_URL)
    not_before = from_date()
    contents, total = get_contents(FEED_URL, session_cookies, not_before)
    download_contents(contents, total, session_cookies)

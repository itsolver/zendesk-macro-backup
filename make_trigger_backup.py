import os
import datetime
import csv
import re
import json
import requests
import getpass

session = requests.Session()
zendesk_subdomain = input('Zendesk subdomain: ')
zendesk_user = input('Zendesk username+"/token" or username: ')
zendesk_secret = input("Zendesk token or password: ")
session.auth = (zendesk_user, zendesk_secret)
zendesk = 'https://' + zendesk_subdomain + '.zendesk.com'

date = datetime.date.today()
active_backup_path = os.path.join(str(date))
if not os.path.exists(active_backup_path):
    os.makedirs(active_backup_path)
inactive_backup_path = os.path.join(active_backup_path, "inactive/")
if not os.path.exists(inactive_backup_path):
    os.makedirs(inactive_backup_path)
log = []

endpoint = zendesk + '/api/v2/triggers.json'
while endpoint:
    response = session.get(endpoint)
    if response.status_code != 200:
        print('Failed to retrieve triggers with error {}'.format(response.status_code))
        exit()
    data = response.json()

    for trigger in data['triggers']:
        url = trigger['url']
        id = trigger['id']
        title = trigger['title']
        safe_title = re.sub('[/:\*\?\>\<\|\s_—]', '_', title)
        active = trigger['active']
        if active:
            backup_path = active_backup_path
        else: 
            backup_path = inactive_backup_path
        filename = safe_title + '.json'
        created = trigger['created_at']
        updated = trigger['updated_at']
        content = json.dumps(trigger, indent=2)
        with open(os.path.join(backup_path, filename), mode='w', encoding='utf-8') as f:
           f.write(content) 
        print(filename + ' - copied!')
        log.append((filename, title, created, updated))

    endpoint = data['next_page']

with open(os.path.join(backup_path, '_log.csv'), mode='wt', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow( ('File', 'Title', 'Date Created', 'Date Updated') )
    for trigger in log:
        writer.writerow(trigger)

import os
import datetime
import csv
import re
import json
import requests
import getpass

pw = getpass.getpass()
credentials = 'angus@itsolver.net', pw
session = requests.Session()
session.auth = credentials

zendesk = 'https://itsolver.zendesk.com'

date = datetime.date.today()
backup_path = os.path.join(str(date))
if not os.path.exists(backup_path):
    os.makedirs(backup_path)

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

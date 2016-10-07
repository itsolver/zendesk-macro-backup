import os
import datetime
import csv
import re
import json
import requests

credentials = '{your_zendesk_email}`', '{your_zendesk_password}'
session = requests.Session()
session.auth = credentials

zendesk = 'https://{your_zendesk_url}.zendesk.com'

date = datetime.date.today()
backup_path = os.path.join(str(date))
if not os.path.exists(backup_path):
    os.makedirs(backup_path)

log = []

endpoint = zendesk + '/api/v2/macros/active.json'
while endpoint:
    response = session.get(endpoint)
    if response.status_code != 200:
        print('Failed to retrieve macros with error {}'.format(response.status_code))
        exit()
    data = response.json()

    for macro in data['macros']:
        title = macro['title']
        safe_title = re.sub('[/:\*\?\>\<\|\s_—]', '_', title)
        filename = safe_title + '.json'
        created = macro['created_at']
        updated = macro['updated_at']
        content = json.dumps(macro['actions'], indent=4)
        with open(os.path.join(backup_path, filename), mode='w', encoding='utf-8') as f:
            f.write(content)
        print(filename + ' - copied!')

        log.append((filename, title, created, updated))

    endpoint = data['next_page']

with open(os.path.join(backup_path, '_log.csv'), mode='wt', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow( ('File', 'Title', 'Date Created', 'Date Updated') )
    for macro in log:
        writer.writerow(macro)
